import logging
import time

from common.service_utils import overwrite_input
from shura.pages.commands_page import CommandsPage, CommandsPanel
from shura.settings import SAVE_PANEL_DELAY, SELECT_CHECKBOX_ROLES_DELAY

logger = logging.getLogger(__name__)


def create_command(
    commands_page: CommandsPage,
    command_name: str,
    command_data: str,
    command_type: str,
    command_for_roles: list,
):
    """Добавление команды с параметрами из файла constants.py.

    :param commands_page:
    :param command_name:
    :param command_data:
    :param command_type:
    :param command_for_roles:
    :return:
    """
    commands_page.combo_btn_add().click()
    commands_panel = CommandsPanel.from_page_obj(commands_page)
    commands_panel.command_title_field().send_keys(command_name)
    commands_panel.command_data_field().send_keys(command_data)
    commands_panel.command_type_select().click()
    commands_panel.command_type(command_type).click()
    for role in command_for_roles:
        time.sleep(SELECT_CHECKBOX_ROLES_DELAY)
        commands_panel.command_for_roles(role).click()

    commands_panel.save_changes_and_exit_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
    commands_page.close_alerts()


def update_command(
    commands_page: CommandsPage,
    command_name: str,
    command_data: str,
    command_for_roles: list,
):
    commands_page.select_item(command_name).click()
    commands_panel = CommandsPanel.from_page_obj(commands_page)
    overwrite_input(input_field=commands_panel.command_data_field(), value=command_data)
    time.sleep(SELECT_CHECKBOX_ROLES_DELAY)
    for role in command_for_roles:
        commands_panel.command_for_roles(role).click()
    commands_panel.save_changes_and_exit_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
    commands_page.close_alerts()


def delete_command(
    commands_page: CommandsPage,
    command_name: str,
):
    """Удаление команды.

    :param commands_page: Страница команд
    :param command_name: Имя команды
    :return:
    """
    commands_page.select_checkbox(command_name).click()
    commands_page.combo_btn_del().click()
    commands_page.popup_confirm()
    commands_page.close_alerts()


def get_command_data(commands_page: CommandsPage, command_name: str):
    commands_page.select_item(command_name).click()
    commands_panel = CommandsPanel.from_page_obj(commands_page)
    new_command_data = commands_panel.command_data_field().get_property("value")
    commands_panel.close_panel_without_save().click()
    time.sleep(SAVE_PANEL_DELAY)
    commands_page.close_alerts()
    return new_command_data
