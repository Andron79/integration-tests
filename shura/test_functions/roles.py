from common.service_utils import overwrite_input
from shura.pages.roles_page import RolesPanel, RolesPage


def _create_role(
    roles_page: RolesPage,
    name: str,
    description: str,
) -> RolesPanel:
    """Создание тестовой роли.

    :param roles_page: Страница Роли
    :param name: Название Роли
    :param description: Описание Роли
    :return None: RolesPanel
    """
    roles_page.combo_btn_add().click()
    panel = RolesPanel.from_page_obj(roles_page)
    panel.role_title().send_keys(name)
    panel.role_description().send_keys(description)
    return panel


def create_role(roles_page: RolesPage, name: str, description: str) -> None:
    """Создание тестовой роли.

    :param roles_page: Страница Роли
    :param name: Название Роли
    :param description: Описание Роли
    :return None:
    """
    panel = _create_role(roles_page, name=name, description=description)
    panel.role_check_all_checkboxes()
    panel.role_btn_submit().click()


def update_role(roles_page: RolesPage, name: str, description_updated: str) -> None:
    """Изменение тестовой роли.

    :param roles_page:
    :param name:
    :param description_updated:
    :return None:
    """
    roles_page.select_item(name).click()
    panel = RolesPanel.from_page_obj(roles_page)
    overwrite_input(panel.role_description(), description_updated)
    panel.role_uncheck_all_checkboxes()
    panel.role_btn_submit().click()
    roles_page.select_item(name).click()


def delete_role(roles_page: RolesPage, name: str) -> None:
    """Удаление тестовой роли.

    :param roles_page:
    :param name:
    :return:
    """
    roles_page.select_checkbox(name).click()
    roles_page.delete_selected()


def create_role_without_privileges(
    roles_page: RolesPage, name: str, description: str
) -> None:
    """Создание тестовой роли без привилегий.

    :param roles_page: Страница Роли
    :param name: Название Роли
    :param description: Описание Роли
    :return None:
    """
    panel = _create_role(roles_page, name=name, description=description)
    panel.role_uncheck_all_checkboxes()
    panel.role_btn_submit().click()


def create_role_with_privileges(
    roles_page: RolesPage, name: str, description: str
) -> None:
    """Создание тестовой роли с привилегиями.

    :param roles_page: Страница Роли
    :param name: Название Роли
    :param description: Описание Роли
    :return None:
    """
    panel = _create_role(roles_page, name=name, description=description)
    panel.role_check_all_checkboxes()
    panel.role_btn_submit().click()


def create_role_from_template(
    roles_page: RolesPage, name: str, template_name: str, description: str
) -> None:
    """Создание тестовой роли на основе шаблона.

    :param template_name: Название шаблона для создания Роли
    :param roles_page: Страница Роли
    :param name: Название Роли
    :param description: Описание Роли
    :return None:
    """

    panel = _create_role(roles_page, name=name, description=description)
    panel.select_template_for_role(template_name).click()
    panel.role_btn_submit().click()


def create_readonly_role(roles_page: RolesPage, name: str, description: str) -> None:
    """Создание тестовой роли.

    :param roles_page: Страница Роли
    :param name: Название Роли
    :param description: Описание Роли
    :return None:
    """
    panel = _create_role(roles_page, name=name, description=description)
    panel.readonly_role_check_checkboxes()
    panel.role_btn_submit().click()
