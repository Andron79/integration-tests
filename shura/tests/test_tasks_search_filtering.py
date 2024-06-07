# Реализовать автотест проверки поиска и фильтрации:
# Страница Заданий. Убедиться, что есть Задания с Наименованиями (условно) 1234, 234, 34
# а) Нет фильтрации и поиска - убедиться, что в списке есть все 3 задания
# б) Ввести фильтрацию по Наименованию = 23. Убедиться, что в списке осталось 2 задания - 1234 и 234
# в) Добавить Поиск по 123. Убедиться, что в списке осталось 1 задание с Наименованием 1234
# г) Убрать Фильтрацию и Поиск. Убедиться, что в списке опять 3 задания

import logging
import time

from shura.settings import TIMEOUT_TASKS_SEARCH_FILTERING
from shura.test_data.constants import (
    TASKS_NAMES_FOR_SEARCH_AND_FILTERING,
    TASKS_FILTER_VALUE,
    TASK_SEARCH_VALUE,
)

from shura.test_functions.tasks import (
    filtering_tasks,
    reset_filter,
    delete_task,
    search_tasks,
    clear_search_field,
)

logger = logging.getLogger(__name__)


def test_task_search_filtering(task_page_with_tasks):
    count = None
    for count, task_name in enumerate(TASKS_NAMES_FOR_SEARCH_AND_FILTERING):
        assert (
            task_name in task_page_with_tasks.list_table_items()
        ), f"Задание {task_name} не существует!"
        logger.info(f"Задание {task_name} существует - OK!")

    assert count + 1 == len(TASKS_NAMES_FOR_SEARCH_AND_FILTERING)
    logger.info(
        f"Количество заданий {count + 1} = {len(TASKS_NAMES_FOR_SEARCH_AND_FILTERING)} - OK!"
    )

    filtering_tasks(task_page=task_page_with_tasks, value=TASKS_FILTER_VALUE)
    time.sleep(TIMEOUT_TASKS_SEARCH_FILTERING)

    assert (
        len(list(task_page_with_tasks.list_table_items())) == 2
    ), f"Количество отфильтрованных заданий - {len(list(task_page_with_tasks.list_table_items()))} != 2 - ERROR!"
    logger.info(
        f"Количество отфильтрованных заданий - {len(list(task_page_with_tasks.list_table_items()))} = 2 - OK!"
    )

    reset_filter(task_page=task_page_with_tasks)
    time.sleep(TIMEOUT_TASKS_SEARCH_FILTERING)

    search_tasks(task_page=task_page_with_tasks, value=TASK_SEARCH_VALUE)
    time.sleep(TIMEOUT_TASKS_SEARCH_FILTERING)

    assert (
        len(list(task_page_with_tasks.list_table_items())) == 1
    ), f"Количество найденных заданий - {len(list(task_page_with_tasks.list_table_items()))} != 1 - ERROR!"
    logger.info(
        f"Количество найденных заданий - {len(list(task_page_with_tasks.list_table_items()))} = 1 - OK!"
    )

    assert (
        TASK_SEARCH_VALUE in task_page_with_tasks.list_table_items()
    ), f"Не найдено задание - {TASK_SEARCH_VALUE} - ERROR!"
    logger.info(f"Найдено задание - {TASK_SEARCH_VALUE} - OK!")

    clear_search_field(task_page=task_page_with_tasks)

    for task_name in TASKS_NAMES_FOR_SEARCH_AND_FILTERING:
        delete_task(task_page_with_tasks, task_name)
        assert not task_page_with_tasks.list_item_exists(
            task_name
        ), f"Задание {task_name} не удалено!"
        logger.info(f"Задание {task_name} удалено - OK!")
