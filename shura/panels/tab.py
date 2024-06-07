from selenium.webdriver.common.by import By
from shura.pages.mapping_rules_page import TemplateMappingRulesPage
from shura.panels.base import Panel


class TabPanel(Panel):
    ID = "templates"

    def _goto_tab(self, element: str):
        self.driver.find_element(By.ID, f"{self.ID}__{element}").click()

    def goto_template_mapping_rules_page(self) -> TemplateMappingRulesPage:
        self._goto_tab("mappings")
        return TemplateMappingRulesPage(self.driver)
