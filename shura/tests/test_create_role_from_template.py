import logging

from shura.pages.roles_page import RolesPanel
from shura.test_data.constants import (
    AUTOTEST_DESCRIPTION,
    AUTOTEST_DESCRIPTION_UPDATED,
    Roles,
)
from shura.test_functions.roles import (
    create_role_from_template,
    create_role_without_privileges,
    create_role_with_privileges,
)

logger = logging.getLogger(__name__)


def test_role_from_template(roles_page):
    #  Создание тестовой роли без привилегий
    create_role_without_privileges(
        roles_page=roles_page,
        name=Roles.TEST_ROLE.value,
        description=AUTOTEST_DESCRIPTION,
    )

    assert roles_page.list_item_exists(
        Roles.TEST_ROLE.value
    ), f"Роль {Roles.TEST_ROLE.value} не была создана!"
    logger.info(f"Роль на основе шаблона {Roles.USER.value} создана - OK!")

    #  Создание тестовой роли из шаблона TEST_ROLE, созданного ранее
    create_role_from_template(
        roles_page=roles_page,
        name=Roles.TEST_NEW_ROLE.value,
        template_name=Roles.TEST_ROLE.value,
        description=AUTOTEST_DESCRIPTION_UPDATED,
    )

    assert roles_page.list_item_exists(
        Roles.TEST_NEW_ROLE.value
    ), f"Роль {Roles.TEST_NEW_ROLE.value} не была создана!"
    logger.info(f"Роль на основе шаблона {Roles.TEST_NEW_ROLE.value} создана - OK!")

    roles_page.select_item(Roles.TEST_NEW_ROLE.value).click()
    role_panel = RolesPanel.from_page_obj(roles_page)

    assert role_panel.verify_checkboxes_state(False), "Чекбоксы остались отмеченными!"
    logger.info("Чекбоксы не отмечены! - OK!")

    role_panel.role_btn_submit().click()
    roles_page.close_alerts()

    #  Удаление тестовых ролей
    roles_page.delete_no_predefined_items()

    assert not roles_page.list_item_exists(
        Roles.TEST_NEW_ROLE.value
    ), f"Роль {Roles.TEST_NEW_ROLE.value} не была удалена!"
    logger.info(f"Роль {Roles.TEST_NEW_ROLE.value} удалена - OK!")

    assert not roles_page.list_item_exists(
        Roles.TEST_ROLE.value
    ), f"Роль {Roles.TEST_ROLE.value} не была удалена!"
    logger.info(f"Роль {Roles.TEST_ROLE.value} удалена - OK!")

    #  Создание роли с привилегиями
    create_role_with_privileges(
        roles_page=roles_page,
        name=Roles.TEST_ROLE.value,
        description=AUTOTEST_DESCRIPTION,
    )

    assert roles_page.list_item_exists(
        Roles.TEST_ROLE.value
    ), f"Роль {Roles.TEST_ROLE.value} не была создана!"
    logger.info(f"Роль на основе шаблона {Roles.USER.value} создана - OK!")

    #  Создание тестовой роли из шаблона TEST_ROLE, созданного ранее
    create_role_from_template(
        roles_page=roles_page,
        name=Roles.TEST_NEW_ROLE.value,
        template_name=Roles.TEST_ROLE.value,
        description=AUTOTEST_DESCRIPTION_UPDATED,
    )

    assert roles_page.list_item_exists(
        Roles.TEST_NEW_ROLE.value
    ), f"Роль {Roles.TEST_NEW_ROLE.value} не была создана!"
    logger.info(f"Роль на основе шаблона {Roles.TEST_NEW_ROLE.value} создана - OK!")

    roles_page.select_item(Roles.TEST_NEW_ROLE.value).click()
    role_panel = RolesPanel.from_page_obj(roles_page)

    assert role_panel.verify_checkboxes_state(True), "Чекбоксы остались не отмеченными!"
    logger.info("Чекбоксы отмечены! - OK!")

    role_panel.role_btn_submit().click()
    roles_page.close_alerts()

    #  Удаление тестовых ролей
    roles_page.delete_no_predefined_items()

    assert not roles_page.list_item_exists(
        Roles.TEST_NEW_ROLE.value
    ), f"Роль {Roles.TEST_NEW_ROLE.value} не была удалена!"
    logger.info(f"Роль {Roles.TEST_NEW_ROLE.value} удалена - OK!")

    assert not roles_page.list_item_exists(
        Roles.TEST_ROLE.value
    ), f"Роль {Roles.TEST_ROLE.value} не была удалена!"
    logger.info(f"Роль {Roles.TEST_ROLE.value} удалена - OK!")
