"""Тестовый сценарий:

Реализовать автотест валидации полей на страничке синхронизации с AD:
0) Используя значения с regress.kknd.gm.corp, синхронизироваться с AD
1) Проверка ошибки SpacesNotAllowed
Встроить пробел по порядку в поля base_dn, attributes, mappings, defaults
Нажать СОХРАНИТЬ
Проверить, что выдается ошибка
2) InvalidLDAPFilter
В рабочий фильтр юзеров влепить лишнюю скобку (. Нажать СОХРАНИТЬ
Проверить, что выдается ошибка
3) KeyValueSchemaError
Добавить запятую в конце полей base_dn, mappings, defaults
Нажать СОХРАНИТЬ
Проверить, что выдается ошибка
4) InvalidLDIF
в поле base_dn вставить неправильный ключ DN, например добавить единичку к DC: "Dc1=kknd,dc=gm,dc=corp"
Нажать СОХРАНИТЬ
Проверить, что выдается ошибка
5) EmptyAttributesPresent
Встроить двойную запятую ,, в поле attributes
Нажать СОХРАНИТЬ
Проверить, что выдается ошибка
6) DuplicateAttributes
Встроить повторяющийся атрибут в поле attributes
Нажать СОХРАНИТЬ
Проверить, что выдается ошибка
7) MissingRequiredAttributes
Удалить по порядку атрибуты cn, sn,objectClass,sAMAccountName,objectGUID,userPrincipalName в полe attributes
Нажать СОХРАНИТЬ
Проверить, что выдается ошибка
8) InvalidAttributes
Удалить в полe attributes атрибут, для которого задано соответствие полей в поле mapping
Нажать СОХРАНИТЬ
Проверить, что выдается ошибка
"""

import logging
import time

import pytest

from shura.pages.settings_page import AdSynchronization
from shura.settings import TIMEOUT_VALIDATIONS
from shura.test_data.constants import NO_VALID_DATA

logger = logging.getLogger(__name__)


@pytest.mark.skip(reason="Перепроверить тест на 3.13.0")
def test_spaces_not_allowed_error(
    ad_panel: AdSynchronization, data: dict = NO_VALID_DATA["SPACES_NOT_ALLOWED_ERROR"]
) -> None:
    ad_panel.save_sync_settings(data)
    time.sleep(TIMEOUT_VALIDATIONS)
    validation_error_count = ad_panel.validation_error_count()
    validation_error_massages = ad_panel.validation_error_massages()

    assert (
        validation_error_count == 4
    ), f"SpacesNotAllowed: {validation_error_massages} ошибки валидации {validation_error_count} из 4 - ERROR!"
    logger.info(
        f"SpacesNotAllowed: {validation_error_massages} ошибки валидации {validation_error_count} из 4 - ОК!"
    )


@pytest.mark.skip(reason="Перепроверить тест на 3.13.0")
def test_invalid_ldap_filter(
    ad_panel: AdSynchronization, data: dict = NO_VALID_DATA["INVALID_LDAP_FILTER"]
) -> None:
    ad_panel.save_sync_settings(data)
    time.sleep(TIMEOUT_VALIDATIONS)
    validation_error_count = ad_panel.validation_error_count()
    validation_error_massages = ad_panel.validation_error_massages()

    assert validation_error_count == 2, (
        f"InvalidLDAPFilter: {validation_error_massages} "
        f"Найдено {validation_error_count} ошибки валидации, из 2 - ERROR!"
    )
    logger.info(
        f"InvalidLDAPFilter: {validation_error_massages} "
        f"Найдено {validation_error_count} ошибки валидации, из 2 - ОК!"
    )


@pytest.mark.skip(reason="Перепроверить тест на 3.13.0")
def test_key_value_schema_error(
    ad_panel: AdSynchronization, data: dict = NO_VALID_DATA["KEY_VALUE_SCHEMA_ERROR"]
) -> None:
    ad_panel.save_sync_settings(data)
    time.sleep(TIMEOUT_VALIDATIONS)
    validation_error_count = ad_panel.validation_error_count()
    validation_error_massages = ad_panel.validation_error_massages()

    assert validation_error_count == 3, (
        f"KeyValueSchemaError: {validation_error_massages} ошибки валидации, "
        f"{validation_error_count} из 3 - ERROR!"
    )
    logger.info(
        f"KeyValueSchemaError: {validation_error_massages} ошибки валидации, {validation_error_count} из 3 - ОК!"
    )


@pytest.mark.skip(reason="Перепроверить тест на 3.13.0")
def test_invalid_ldif(
    ad_panel: AdSynchronization, data: dict = NO_VALID_DATA["INVALID_LDIF"]
) -> None:
    ad_panel.save_sync_settings(data)
    time.sleep(TIMEOUT_VALIDATIONS)
    validation_error_count = ad_panel.validation_error_count()
    validation_error_massages = ad_panel.validation_error_massages()

    assert (
        validation_error_count == 2
    ), f"InvalidLDIF: {validation_error_massages} ошибки валидации, {validation_error_count} из 2 - ERROR!"
    logger.info(
        f"InvalidLDIF: {validation_error_massages} ошибки валидации, {validation_error_count} из 2 - ОК!"
    )


@pytest.mark.skip(reason="Перепроверить тест на 3.13.0")
def test_empty_attributes_present(
    ad_panel: AdSynchronization, data: dict = NO_VALID_DATA["EMPTY_ATTRIBUTES_PRESENT"]
) -> None:
    ad_panel.save_sync_settings(data)
    time.sleep(TIMEOUT_VALIDATIONS)
    validation_error_count = ad_panel.validation_error_count()
    validation_error_massages = ad_panel.validation_error_massages()

    assert validation_error_count == 2, (
        f"EmptyAttributesPresent: {validation_error_massages} ошибки валидации, "
        f"{validation_error_count} из 2 - ERROR!"
    )
    logger.info(
        f"EmptyAttributesPresent: {validation_error_massages} ошибки валидации, {validation_error_count} из 2 - ОК!"
    )


@pytest.mark.skip(reason="Перепроверить тест на 3.13.0")
def test_duplicate_attributes(
    ad_panel: AdSynchronization, data: dict = NO_VALID_DATA["DUPLICATE_ATTRIBUTES"]
) -> None:
    ad_panel.save_sync_settings(data)
    time.sleep(TIMEOUT_VALIDATIONS)
    validation_error_count = ad_panel.validation_error_count()
    validation_error_massages = ad_panel.validation_error_massages()

    assert validation_error_count == 2, (
        f"DuplicateAttributes: {validation_error_massages} ошибки валидации, "
        f"{validation_error_count} из 2 - ERROR!"
    )
    logger.info(
        f"DuplicateAttributes: {validation_error_massages} ошибки валидации, {validation_error_count} из 2 - ОК!"
    )


@pytest.mark.skip(reason="Перепроверить тест на 3.13.0")
def test_missing_required_attributes(
    ad_panel: AdSynchronization,
    data: dict = NO_VALID_DATA["MISSING_REQUIRED_ATTRIBUTES"],
) -> None:
    ad_panel.save_sync_settings(data)
    time.sleep(TIMEOUT_VALIDATIONS)
    validation_error_count = ad_panel.validation_error_count()
    validation_error_massages = ad_panel.validation_error_massages()

    assert validation_error_count == 3, (
        f"MissingRequiredAttributes: {validation_error_massages} ошибки валидации, "
        f"{validation_error_count} из 3 - ERROR!"
    )
    logger.info(
        f"MissingRequiredAttributes: {validation_error_massages} ошибки валидации, {validation_error_count} из 3 - ОК!"
    )


@pytest.mark.skip(reason="Перепроверить тест на 3.13.0")
def test_invalid_attributes(
    ad_panel: AdSynchronization, data: dict = NO_VALID_DATA["INVALID_ATTRIBUTES"]
) -> None:
    ad_panel.save_sync_settings(data)
    time.sleep(TIMEOUT_VALIDATIONS)

    validation_error_count = ad_panel.validation_error_count()
    validation_error_massages = ad_panel.validation_error_massages()

    assert validation_error_count == 2, (
        f"InvalidAttributes: {validation_error_massages} ошибки валидации, "
        f"{validation_error_count} из 1 - ERROR!"
    )
