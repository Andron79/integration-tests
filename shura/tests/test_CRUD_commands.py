import logging

from shura.test_data.constants import (
    COMMAND_NAME,
    COMMAND_DATA,
    NEW_COMMAND_DATA,
    COMMAND_TYPE,
    COMMAND_FOR_ROLES,
)
from shura.test_functions.commands import (
    create_command,
    update_command,
    delete_command,
    get_command_data,
)

logger = logging.getLogger(__name__)


def test_commands_crud(commands_page):
    create_command(
        commands_page=commands_page,
        command_name=COMMAND_NAME,
        command_data=COMMAND_DATA,
        command_type=COMMAND_TYPE,
        command_for_roles=COMMAND_FOR_ROLES,
    )

    assert commands_page.list_item_exists(COMMAND_NAME), "Команда не была создана!"
    logger.info("Команда создана - OK!")

    update_command(
        commands_page=commands_page,
        command_name=COMMAND_NAME,
        command_data=NEW_COMMAND_DATA,
        command_for_roles=COMMAND_FOR_ROLES,
    )

    new_command_data = get_command_data(
        commands_page=commands_page, command_name=COMMAND_NAME
    )

    assert new_command_data == NEW_COMMAND_DATA, "Команда не изменена!"
    logger.info("Команда изменена - OK!")

    delete_command(commands_page=commands_page, command_name=COMMAND_NAME)

    assert not commands_page.list_item_exists(COMMAND_NAME), "Команда не удалена!"
    logger.info("Команда удалена - OK!")
