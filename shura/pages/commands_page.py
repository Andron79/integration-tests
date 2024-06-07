from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from shura.pages.base import ItemsTablePage
from shura.panels.base import Locator
from shura.panels.object import ObjectPanel


class CommandsPage(ItemsTablePage):
    ...


class CommandsPanel(ObjectPanel):
    ID = "CommandCreate"
    CSS_SELECTOR_LOCATOR: Locator = ".RightPanel"

    def command_title_field(self) -> WebElement:
        return self.element_by_id("title")

    def command_data_field(self) -> WebElement:
        return self.element_by_id("data")

    def command_type_select(self) -> WebElement:
        return self.element_by_id("type-selector")

    def command_type(self, command_type: str) -> WebElement:
        """Поиск элемента Тип в панели создания команды.

        :param command_type:
        :return WebElement:
        """
        return WebDriverWait(self.root, 10).until(
            EC.visibility_of_element_located((By.ID, f"select-option__{command_type}"))
        )

    def command_for_roles(self, role: str) -> WebElement:
        return WebDriverWait(self.root, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"#{self.ID}__role-{role.lower()} ~ span")
            )
        )
