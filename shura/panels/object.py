import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from common.service_utils import overwrite_input
from shura.panels.base import Panel, Locator


class ObjectPanel(Panel):
    ID = ""
    CSS_SELECTOR_LOCATOR: Locator = ""
    CSS_SELECTOR: Locator = ""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.root = self.driver.find_element(By.CSS_SELECTOR, self.CSS_SELECTOR_LOCATOR)

    def element_by_id(self, name: str) -> WebElement:
        """Ищет элемент по ID внутри Panel.

        :param name: Название элемента для поиска
        :return: WebElement
        """
        return self.root.find_element(By.ID, f"{self.ID}__{name}")

    def element_by_css_selector(self, name: str) -> WebElement:
        """Ищет элемент по CSS.SELECTOR внутри Panel.

        :param name: Название элемента для поиска
        :return: WebElement
        """
        return self.root.find_element(By.CSS_SELECTOR, f"#{self.CSS_SELECTOR}__{name}")

    def elements_by_css_selector(self, name: str) -> List[WebElement]:
        """Ищет элементы по CSS.SELECTOR внутри Panel.

        :param name: Название элемента для поиска
        :return: List[WebElement]
        """
        return self.root.find_elements(By.CSS_SELECTOR, f"#{self.CSS_SELECTOR}__{name}")

    def load_btn(self) -> WebElement:
        return self.root.find_element(By.ID, "Btn__submit-saveAnsClose")

    def load_file(self, file):
        file_input = self.root.find_element(
            By.CSS_SELECTOR, ".RightPanel input[type='file']"
        )
        file_input.send_keys(file)

    def _input_fields(self) -> List[WebElement]:
        return self.root.find_elements(
            By.CSS_SELECTOR, ".FormDefault .mb-3 .form-control"
        )

    def fill_panel_with_data(
        self, data: dict, start_delay: float = 0.0, input_delay: float = 0.0
    ):
        for field_name, value in data.items():
            field = self.element_by_id(field_name)
            time.sleep(start_delay)
            overwrite_input(field, value, delay=input_delay)

    def save_changes_and_exit_btn(self):
        return self.root.find_element(By.ID, "Btn__submit-saveAnsClose")

    def save_changes_btn(self) -> WebElement:
        return self.root.find_element(By.ID, "Btn__submit-save")

    def close_panel_without_save(self) -> WebElement:
        return self.root.find_element(By.CSS_SELECTOR, "span.icon-cross")
