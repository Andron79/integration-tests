import logging
import os
import time

import pytest
from shura.settings import SAVE_PANEL_DELAY
from shura.pages.updates_page import FirmwarePanel
from shura.test_data.constants import firmware_path, COMMENT
from shura.test_functions.updates import (
    create_firmware,
    delete_firmware,
    update_firmware,
)

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("downloaded_file", [firmware_path], indirect=True)
def test_update_crud(downloaded_file, updates_page):
    create_firmware(updates_page=updates_page, downloaded_file=downloaded_file)

    assert updates_page.list_item_exists(
        os.path.basename(downloaded_file)
    ), "Прошивка не загружена!"
    logger.info("Прошивка загружена - OK!")

    update_firmware(
        updates_page=updates_page, value=COMMENT, downloaded_file=downloaded_file
    )

    firmware_panel = FirmwarePanel.from_page_obj(updates_page)
    comment = firmware_panel.comment_field().get_attribute("value")
    firmware_panel.load_btn().click()
    time.sleep(SAVE_PANEL_DELAY)

    assert COMMENT == comment, "Комментарий в прошивке не был изменен!"
    logger.info("Комментарий в прошивке обновлен - OK!")

    delete_firmware(updates_page=updates_page, downloaded_file=downloaded_file)

    assert not updates_page.list_item_exists(
        os.path.basename(downloaded_file)
    ), "Прошивка не была удалена!"
    logger.info("Прошивка была удалена - OK!")
