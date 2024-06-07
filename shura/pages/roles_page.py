import logging
import string
from typing import List

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from shura.pages.base import ItemsTablePage
from shura.panels.base import Locator
from shura.panels.object import ObjectPanel
from shura.test_data.constants import PREDEFINED_ROLES

logger = logging.getLogger(__name__)


class RolesPage(ItemsTablePage):
    PREDEFINED_ITEMS = PREDEFINED_ROLES

    def check_success_alert(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "Alert--success"))
        )


class RolesPanel(ObjectPanel):
    ID = "RolesForm"
    CSS_SELECTOR_LOCATOR: Locator = ".Roles"

    def role_title(self) -> WebElement:
        return self.element_by_id("name")

    def role_description(self) -> WebElement:
        return self.element_by_id("description")

    def role_description_text(self, text) -> string:
        return WebDriverWait(self.root, 10).until(
            EC.text_to_be_present_in_element((By.ID, f"{self.ID}__description"), text)
        )

    def role_selector_page(self) -> WebElement:
        return self.element_by_id("current-field")

    def role_select_page_item(self, page: str) -> WebElement:
        return WebDriverWait(self.root, 10).until(
            EC.element_to_be_clickable((By.ID, f"{self.ID}__current-field-{page}"))
        )

    def role_unchecked_checkboxes(self) -> List[WebElement]:
        try:
            return self.root.find_elements(
                By.CSS_SELECTOR,
                ".Access-roles-table__checkbox:not(:disabled):not(:checked) ~ span",
            )
        except (NoSuchElementException, TimeoutException):
            return []

    def role_checked_checkboxes(self) -> List[WebElement]:
        try:
            return self.root.find_elements(
                By.CSS_SELECTOR,
                ".Access-roles-table__checkbox:not(:disabled):checked ~ span",
            )
        except (NoSuchElementException, TimeoutException):
            return []

    def _readonly_role_checkboxes(self) -> List[WebElement]:
        return self.root.find_elements(
            By.CSS_SELECTOR,
            "[id*='-read'].Access-roles-table__checkbox:not(:disabled):not(:checked) ~ span",
        )

    def readonly_role_check_checkboxes(self) -> None:
        for checkbox in self._readonly_role_checkboxes():
            checkbox.click()

    def role_btn_submit(self) -> WebElement:
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Btn__submit-saveAnsClose"))
        )

    def pages_list(self):
        return self.root.find_elements(
            By.CSS_SELECTOR, f"#{self.ID}__current-field option"
        )

    def role_check_all_checkboxes(self) -> None:
        while unchecked_checkboxes := self.role_unchecked_checkboxes():
            unchecked_checkboxes[0].click()

    def role_uncheck_all_checkboxes(self) -> None:
        while checked_checkboxes := self.role_checked_checkboxes():
            checked_checkboxes[0].click()

    def verify_checkboxes_state(self, checked: bool) -> bool:
        verifier_func = (
            self.role_checked_checkboxes if checked else self.role_unchecked_checkboxes
        )

        if not verifier_func():
            return False
        return True

    def _template_selector(self) -> WebElement:
        return WebDriverWait(self.root, 10).until(
            EC.element_to_be_clickable((By.ID, f"{self.ID}__baseRole"))
        )

    def select_template_for_role(self, template_name: str) -> WebElement:
        self._template_selector().click()
        return self.root.find_element(By.ID, f"select-option__{template_name}")
