"""Тестовый сценарий:

Перейти на страницу Настройки - Синхронизация с AD (там, по идее, уже настроена AD #1)
Заполнить поля:
AD Сервер: msk-dc2.getmobit.ru
AD Порт: 636
Логин: usert
Пароль test123
Корневой элемент (Base DN): dc=getmobit,dc=ru
Интервал синхронизации (минут): 1
Фильтр для получения списка суперадминистраторов: (&(objectClass=person)(!(objectClass=computer))(|(sAMAccountName=u*)))
Атрибуты: cn,sn,objectClass,sAMAccountName,objectGUID,userPrincipalName,objectSid,memberOf
Cоответствие полей:
title=cn,username=sAMAccountName,password=userPrincipalName
Активировать чекбокс "Включить синхронизацию"
Нажать кнопку "Сохранить изменения"

Убедиться, что появилась зеленая плашка "Синхронизация запущена"

Разлогиниться и попробовать войти пользователем usert / test123 - должно получиться

Вернуть статус кво - перелогиниться в superadmin и вернуть прежнюю AD на странице Настройки - Синхронизация с AD
"""

import logging
import time

from common.webdriver import WebDriver
from shura.pages.settings_page import SettingsPage
from shura.settings import SYNC_LDAPS_USERS_DELAY
from shura.test_data.constants import (
    TEST_LDAP_DATA,
    SUPERADMIN_USERNAME,
    SUPERADMIN_PASSWORD,
)
from shura.test_functions.connect_to_AD_from_LDAPS import (
    connect_to_ad_from_ldaps,
    get_authorized_user,
)
from shura.test_functions.login_logout import login_to_server, user_logout

logger = logging.getLogger(__name__)


def test_connect_to_ad_from_ldaps(sync_page: SettingsPage, driver: WebDriver) -> None:
    connect_to_ad_from_ldaps(page=sync_page, data={**TEST_LDAP_DATA})
    time.sleep(SYNC_LDAPS_USERS_DELAY)
    user_logout(driver)

    login_to_server(
        driver=driver,
        login=TEST_LDAP_DATA["login"],
        password=TEST_LDAP_DATA["password"],
    )

    authorized_ldap_user = get_authorized_user(page=sync_page)

    assert (
        authorized_ldap_user == TEST_LDAP_DATA["login"]
    ), f"Пользователь {TEST_LDAP_DATA['login']} не авторизовался на сервере - ERROR"
    logger.info(
        f"Пользователь {TEST_LDAP_DATA['login']} успешно авторизован на сервере- OK!"
    )

    user_logout(driver)
    logger.info(
        f"Пользователь {TEST_LDAP_DATA['login']} успешно разлогинился на сервере- OK!"
    )

    login_to_server(
        driver=driver, login=SUPERADMIN_USERNAME, password=SUPERADMIN_PASSWORD
    )
    logger.info(
        f"Пользователь {SUPERADMIN_USERNAME} успешно авторизован на сервере- OK!"
    )
