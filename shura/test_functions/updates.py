import os
import time
from common.service_utils import overwrite_input

from shura.settings import SAVE_PANEL_DELAY
from shura.pages.updates_page import UpdatesPage, FirmwarePanel


def create_firmware(updates_page: UpdatesPage, downloaded_file):
    """Добавление прошивки.

    :param updates_page:
    :param downloaded_file:
    :return:
    """
    updates_page.combo_btn_add().click()
    firmware_panel = FirmwarePanel.from_page_obj(updates_page)
    firmware_panel.load_file(downloaded_file)
    firmware_panel.load_btn().click()
    updates_page.close_alerts()


def update_firmware(updates_page: UpdatesPage, value: str, downloaded_file):
    """Изменение в прошивке поля Comment.

    :param updates_page:
    :param value:
    :param downloaded_file:
    :return:
    """
    updates_page.select_item(os.path.basename(downloaded_file)).click()
    firmware_panel = FirmwarePanel.from_page_obj(updates_page)
    overwrite_input(firmware_panel.comment_field(), value=value)
    firmware_panel.load_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
    updates_page.wait_close_panel()
    updates_page.select_item(os.path.basename(downloaded_file)).click()


def delete_firmware(updates_page: UpdatesPage, downloaded_file):
    """Удаление прошивки.

    :param updates_page: UpdatesPage
    :param downloaded_file:
    :return:
    """
    updates_page.select_checkbox(os.path.basename(downloaded_file)).click()
    updates_page.combo_btn_del().click()
    updates_page.popup_confirm()
    updates_page.close_alerts()
