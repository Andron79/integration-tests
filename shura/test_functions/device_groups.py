import logging
import time


from common.service_utils import overwrite_input
from shura.settings import SYNC_RESPONSE_DEVICES_DELAY
from shura.pages.device_groups_page import DeviceGroupsPage

logger = logging.getLogger(__name__)


def create_device_group(
    device_group_page: DeviceGroupsPage, title: str, description: str
):
    """Создание группы устройств.

    :param device_group_page: Страница группы
    :param title: Название группы
    :param description: Описание группы
    :return: None
    """
    device_group_page.combo_btn_add().click()
    device_group_page.group_title_field().send_keys(title)
    device_group_page.group_description_field().send_keys(description)
    device_group_page.create_group_btn().click()
    device_group_page.close_alerts()


def update_description_field(
    device_group_page: DeviceGroupsPage, title: str, description: str
):
    """Редактирование описания группы.

    :param device_group_page: Страница группы
    :param title: Название группы
    :param description: Новое описание группы
    :return: None
    """

    device_group_page.select_group(title).click()
    device_group_page.information_tab().click()
    overwrite_input(
        input_field=device_group_page.group_description_field(), value=description
    )
    device_group_page.save_changes_btn().click()
    device_group_page.close_alerts()


def add_devices_to_group(
    device_group_page: DeviceGroupsPage,
    title: str,
):
    """Добавление устройства в группу.

    :param device_group_page: Страница группы
    :param title: Название группы
    :return: None
    """

    device_group_page.select_group(title).click()
    device_group_page.devices_tab().click()
    device_group_page.devices_menu_btn().click()
    device_group_page.show_all_device_in_group().click()
    time.sleep(SYNC_RESPONSE_DEVICES_DELAY)
    device_group_page.device_select_all().click()
    device_group_page.devices_menu_btn().click()
    device_group_page.add_device_to_group_popup().click()
    device_group_page.close_alerts()


def delete_devices_from_group(
    device_group_page: DeviceGroupsPage,
    title: str,
):
    """Удаление устройства в группу.

    :param device_group_page: Страница группы
    :param title: Название группы
    :return: None
    """
    device_group_page.select_group(title).click()
    device_group_page.devices_tab().click()
    device_group_page.device_select_all().click()
    device_group_page.devices_menu_btn().click()
    device_group_page.remove_device_from_group_popup().click()
    device_group_page.close_alerts()


def get_devices_from_group(
    device_group_page: DeviceGroupsPage,
    title: str,
) -> list[str]:
    """Читаем из группы список добавленных устройств.

    :param device_group_page: Страница группы
    :param title: Название группы
    :return: Generator девайсами из группы
    """
    device_group_page.select_group(title).click()
    return list(device_group_page.list_table_items())


def delete_device_group(device_group_page: DeviceGroupsPage, title: str):
    """Удаление группы устройств.

    :param device_group_page: Страниа группы
    :param title: Название группы
    :return: None
    """
    device_group_page.select_group(title).click()
    device_group_page.combo_btn_del().click()
    device_group_page.popup_confirm()
    device_group_page.close_alerts()
    device_group_page.refresh()


def delete_group_with_devices(device_group_page: DeviceGroupsPage, title: str):
    if get_devices_from_group(device_group_page=device_group_page, title=title):
        delete_devices_from_group(
            device_group_page=device_group_page,
            title=title,
        )
    delete_device_group(
        device_group_page=device_group_page,
        title=title,
    )
