import logging

from shura.pages.roles_page import RolesPanel
from shura.test_data.constants import Roles
from shura.test_functions.roles import create_role, update_role, delete_role

logger = logging.getLogger(__name__)


def test_role_crud(roles_page):
    #  Создание тестовой роли
    create_role(
        roles_page=roles_page,
        name=Roles.TEST_ROLE.value,
        description=Roles.TEST_ROLE.value,
    )
    assert roles_page.check_success_alert(), "Алерт не успешный!"
    assert roles_page.list_item_exists(Roles.TEST_ROLE.value), "Роль не была создана!"
    logger.info("Роль создана - OK!")

    # Обновление тестовой роли
    update_role(
        roles_page=roles_page,
        name=Roles.TEST_ROLE.value,
        description_updated=Roles.TEST_NEW_ROLE.value,
    )

    assert roles_page.check_success_alert(), "Алерт не успешный"

    role_panel = RolesPanel.from_page_obj(roles_page)
    assert role_panel.verify_checkboxes_state(False), "Чекбоксы остались отмеченными!"
    assert role_panel.role_description_text(
        Roles.TEST_NEW_ROLE.value
    ), "Описание не изменилось!"
    logger.info("Роль обновлена - OK!")
    role_panel.role_btn_submit().click()
    roles_page.close_alerts()

    #  Удаление тестовой роли
    delete_role(roles_page=roles_page, name=Roles.TEST_ROLE.value)

    assert roles_page.check_success_alert(), "Алерт не успешный"
    roles_page.close_alerts()
    assert not roles_page.list_item_exists(
        Roles.TEST_ROLE.value
    ), "Роль не была удалена!"
    logger.info("Роль удалена - OK!")
