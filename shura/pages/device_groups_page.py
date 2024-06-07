import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shura.pages.base import ItemsTablePage
from shura.panels.base import Panel

logger = logging.getLogger(__name__)


class DeviceGroupsPage(ItemsTablePage):
    def group_exists(self, item: str) -> bool:
        """Метод проверяет существование элемента на странице.

        :param item: Элемент
        :return: True - если есть элемент на странице, иначе False
        """
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, f"TreeView__node-{item}"))
            )
        except TimeoutException:
            return False
        return True

    def group_title_field(self):
        return self.driver.find_element(By.ID, "GroupEditView__title")

    def group_description_field(self):
        return self.driver.find_element(By.ID, "GroupEditView__description")

    def group_description_field_value(self):
        return self.group_description_field().get_attribute("value")

    def create_group_btn(self):
        return self.driver.find_element(By.ID, "GroupEditView__create-group")

    def information_tab(self):
        return self.driver.find_element(By.ID, "DetailGroupView__tab-information")

    def save_changes_btn(self):
        return self.driver.find_element(By.ID, "GroupEditView__save-changes")

    def devices_tab(self):
        return self.driver.find_element(By.ID, "DetailGroupView__tab-table-devices")

    def devices_menu_btn(self):
        return self.driver.find_element(By.ID, "GroupDeviceView__DropDownMenu")

    def show_all_device_in_group(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "GroupDeviceView__DropDownMenu__show-devices")
            )
        )

    def device_select_all(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "th .checkbox-indicator"))
        )

    def select_group(self, group_name):
        return self.driver.find_element(By.ID, f"TreeView__node-{group_name}")

    def add_device_to_group_popup(self):
        return self.driver.find_element(
            By.ID, "GroupDeviceView__DropDownMenu__add-to-group"
        )

    def remove_device_from_group_popup(self):
        return self.driver.find_element(
            By.ID, "GroupDeviceView__DropDownMenu__delete-from-group"
        )


class DeviceGroupsPanel(Panel):
    pass
