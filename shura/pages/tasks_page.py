from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from shura.panels.base import Locator
from common.service_utils import overwrite_input
from shura.pages.base import ItemsTablePage
from shura.panels.object import ObjectPanel
from shura.test_data.constants import PREDEFINED_TASKS


class TasksPage(ItemsTablePage):
    PREDEFINED_ITEMS = PREDEFINED_TASKS


class TaskPanel(ObjectPanel):
    ID = "TaskCreate"
    CSS_SELECTOR_LOCATOR: Locator = ".RightPanel"

    def task_name_field(self, task):
        field = self.element_by_id("name")
        overwrite_input(field, task)

    def task_select_command_btn(self):
        return self.element_by_id("command-selector")

    def task_select_command_item_list(self, list_item):
        return self.driver.find_element(
            By.XPATH, f"//*/text()[normalize-space(.)='{list_item}']/parent::*"
        )

    def task_name_field_value(self, task_name):
        return WebDriverWait(self.root, 10).until(
            EC.text_to_be_present_in_element_value(
                (By.ID, "TaskCreate__name"), task_name
            )
        )

    def save_and_exit_btn(self):
        return self.driver.find_element(By.ID, "Btn__submit-saveAnsClose")
