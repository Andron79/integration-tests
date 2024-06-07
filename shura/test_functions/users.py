import time
from typing import Optional, Union

from shura.pages.user_page import UserPanel, UserPage

from shura.settings import SAVE_PANEL_DELAY
from shura.test_data.constants import TEST_USER_PROFILE_UPDATE


def create_user(
    user_page: UserPage,
    username: str,
    password: str,
    title: str,
    role: Optional[Union[str, None]] = None,
) -> None:
    """Создание пользователя для тестов.

    :param username: Имя пользователя
    :param password: Пароль
    :param title: Имя пользователя
    :param role: Название роли, опционально
    :param user_page: Страница Пользователей
    :return:
    """

    user_page.combo_btn_add().click()
    user_panel = UserPanel.from_page_obj(user_page)
    user_panel.username_field().send_keys(username)
    user_panel.password_field().send_keys(password)
    user_panel.password_confirmation_field().send_keys(password)
    user_panel.fullname_field().send_keys(title)
    if role:
        # user_panel.user_role().click()
        user_panel.select_user_role(role)
    user_panel.create_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
    user_page.close_alerts()


def update_user(
    user_page: UserPage, username: str, user_profile_update: dict, title: str
):
    """Создание пользователя для тестов.

    :param title: Имя пользователя
    :param user_profile_update: Словарь с данными для заполнения профиля пользователя
    :param username: Имя пользователя
    :param user_page: Страница Пользователей
    :return:
    """
    user_page.select_item(title).click()
    user_panel = UserPanel.from_page_obj(user_page)
    user_panel.collapse_first_section()
    user_panel.expand_all()
    user_panel.fill_panel_with_user_data(
        user_profile_update, start_delay=0.2, input_delay=0
    )
    user_panel.save_changes().click()
    time.sleep(SAVE_PANEL_DELAY)
    user_panel.back_btn().click()
    user_page.close_alerts()


def get_new_user_profile(user_page: UserPage, username: str, title: str) -> dict:
    """Получение обновленных данных пользователя после изменения профиля.

    :param title: Имя пользователя
    :param user_page:
    :param username:
    :return:
    """
    user_page.user_record(username).click()
    user_panel = UserPanel.from_page_obj(user_page)
    user_panel.collapse_first_section()
    user_panel.expand_all()
    user_profile = user_panel.get_user_profile_data(data=TEST_USER_PROFILE_UPDATE)

    user_panel.back_btn().click()

    return user_profile


def delete_user(user_page: UserPage, username: str, title: str):
    """Удаление тестового пользователя.

    :param title: Имя пользователя
    :param username: Username пользователя
    :param user_page: Страница Пользователей
    :return None:
    """
    user_page.select_checkbox(username).click()
    user_page.delete_selected()
    user_page.close_alerts()
