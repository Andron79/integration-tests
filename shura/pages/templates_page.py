from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from shura.pages.base import ItemsTablePage
from shura.panels.object import ObjectPanel


class TemplateDefinitionPage(ItemsTablePage):
    def template_present(self, template_name: str):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"tr[data-name='{template_name}']")
            )
        )

    def template_absent(self, template_name: str):
        return WebDriverWait(self.driver, 3).until(
            EC.invisibility_of_element_located((By.ID, template_name))
        )


class TemplateDefinitionPanel(ObjectPanel):
    ID = "TemplateCreate"
    CLASS_NAME = "RightPanel"
    CSS_SELECTOR_LOCATOR = ".RightPanel"

    def template_profile(self) -> dict:
        return {
            item.get_attribute("id"): item.get_attribute("value")
            for item in self._input_fields()
        }

    def gm_mode(self):
        return WebDriverWait(self.root, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    '#TemplateCreate__gm-mode div[class$="-indicatorContainer"]',
                )
            )
        )

    def terminal_mode(self):
        return self.root.find_element(
            By.CSS_SELECTOR, '#TemplateCreate__gm-mode div[id$="-option-0"]'
        )
