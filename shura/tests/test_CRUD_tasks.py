import logging
import pytest

from shura.test_data.constants import (
    firmware_path,
    TASK_NAME,
    COMMAND_NAME_FOR_TASK,
    NEW_TASK_NAME,
)
from shura.test_functions.tasks import create_task, update_task, delete_task

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("downloaded_file", [firmware_path], indirect=True)
def test_task_crud(task_page, downloaded_file):
    create_task(
        task_page=task_page,
        downloaded_file=downloaded_file,
        task_name=TASK_NAME,
        command_name=COMMAND_NAME_FOR_TASK,
    )

    assert task_page.list_item_exists(TASK_NAME), "Задание не создано!"
    logger.info("Задание создано - OK!")

    update_task(task_page=task_page, task_name=TASK_NAME, new_task_name=NEW_TASK_NAME)

    assert task_page.list_item_exists(NEW_TASK_NAME), "Задание отредактировано!"
    logger.info("Задание отредактировано - OK!")

    delete_task(task_page=task_page, new_task_name=NEW_TASK_NAME)

    assert not task_page.list_item_exists(NEW_TASK_NAME), "Задание не удалено!"
    logger.info("Задание удалено - OK!")
