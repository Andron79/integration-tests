import logging
from shura.test_data.constants import (
    TEST_GROUP_TITLE,
    TEST_GROUP_DESCRIPTION,
    NEW_TEST_GROUP_DESCRIPTION,
)

from shura.test_functions.device_groups import (
    create_device_group,
    delete_device_group,
    update_description_field,
    add_devices_to_group,
    delete_devices_from_group,
    get_devices_from_group,
)

logger = logging.getLogger(__name__)


def _test_add_devices_to_group(device_group_page):
    add_devices_to_group(device_group_page=device_group_page, title=TEST_GROUP_TITLE)

    devices_added_to_the_group = list(
        device_group_page.list_table_items()
    )  # Сохраняем список добавленных устройств
    read_devices_from_the_group = get_devices_from_group(
        device_group_page=device_group_page, title=TEST_GROUP_TITLE
    )

    assert (
        read_devices_from_the_group
    ), "Устройства для добавления в группу отсутствуют!"
    assert (
        devices_added_to_the_group == read_devices_from_the_group
    ), "Устройства в группу не добавлены!"
    logger.info("Устройства в группу добавлены - OK!")

    #  удаление устройств из группы
    delete_devices_from_group(
        device_group_page=device_group_page,
        title=TEST_GROUP_TITLE,
    )

    read_devices_from_the_group = get_devices_from_group(
        device_group_page=device_group_page, title=TEST_GROUP_TITLE
    )

    assert not set(read_devices_from_the_group), "Устройства из группы не удалены!"
    logger.info("Устройства удалены из группы - OK!")


def test_device_group_crud(device_group_page):
    # Создание группы

    create_device_group(
        device_group_page=device_group_page,
        title=TEST_GROUP_TITLE,
        description=TEST_GROUP_DESCRIPTION,
    )

    device_group = device_group_page.select_group(TEST_GROUP_TITLE)
    assert device_group, "Группа не создана"
    logger.info("Группа создана - OK!")

    update_description_field(
        device_group_page=device_group_page,
        title=TEST_GROUP_TITLE,
        description=NEW_TEST_GROUP_DESCRIPTION,
    )

    device_group_page.select_group(TEST_GROUP_TITLE).click()
    device_group_page.information_tab().click()
    new_description = (
        device_group_page.group_description_field_value()
    )  # Читаем описание из группы

    assert new_description == NEW_TEST_GROUP_DESCRIPTION, "Описание группы не изменено!"
    assert new_description != TEST_GROUP_DESCRIPTION, "Описание группы не изменено!"
    logger.info("Описание группы изменено - OK!")

    if device_group_page.list_table_items():
        _test_add_devices_to_group(device_group_page)
    else:
        logger.info("Нет устройств для добавления в группу, пропускаем")

    #  удаление группы
    delete_device_group(
        device_group_page=device_group_page,
        title=TEST_GROUP_TITLE,
    )

    assert not device_group_page.group_exists(TEST_GROUP_TITLE), "Группа не удалена!"
    logger.info("Группа удалена - OK!")
