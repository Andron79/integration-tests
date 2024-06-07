from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from shura.panels.base import Locator
from common.service_utils import overwrite_input
from shura.pages.base import ItemsTablePage
from shura.panels.object import ObjectPanel


class TemplateMappingRulesPage(ItemsTablePage):
    COMBO_BUTTON_SELECTOR: Locator = "div[id$='/templates/mappings'] #DropDownMenu"

    def select_first_mapping_rules(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".TemplatesMapping tbody > tr .checkbox-indicator")
            )
        )

    def get_mapping_rules_by_template(self, template_name: str):
        """Проверяет существование созданного Правила сопоставления по имени
        привязанного шаблона в списке Правил сопоставлений.

        :param template_name:
        :return False если правила не существует, True если шаблон в Правиле равен template_name:
        """

        return bool(
            [
                elem.text
                for elem in self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".TemplatesMapping tbody > tr td[data-column-title='template'] span",
                )
                if elem.text == template_name
            ]
        )

    def get_mapping_rules_by_description(self, description: str):
        """Проверяет существование созданного Правила сопоставления по значению
        поля description привязанного шаблона в списке Правил сопоставлений.

        :param description: Значение поля description
        :return False если правила не существует в списке, True если значение поля описания в Правиле равно description:
        """

        return bool(
            [
                elem.text
                for elem in self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".TemplatesMapping tbody > tr td[data-column-title='description'] span ",
                )
                if elem.text == description
            ]
        )

    def select_mapping_rule(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    ".TemplatesMapping tbody > tr td[data-column-title='template'] span",
                )
            )
        )

    def _open_combo_button(self) -> WebElement:
        """Ищет ComboButton на странице mapping_rules, и если кнопка закрыта,
        кликает на нее, чтобы открыть.

        :return WebElement: Открытая ComboButton
        """
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.COMBO_BUTTON_SELECTOR))
        )

        if btn.get_attribute("aria-expanded").lower() == "false":
            btn.click()

        return btn

    def combo_btn_add(self) -> WebElement:
        self._open_combo_button()
        return self.driver.find_element(
            By.CSS_SELECTOR, "div[id$='/templates/mappings'] #DropDownMenu__add"
        )

    def combo_btn_del(self) -> WebElement:
        self._open_combo_button()
        return self.driver.find_element(
            By.CSS_SELECTOR, "div[id$='/templates/mappings'] #DropDownMenu__delete"
        )


class TemplateMappingRulesPanel(ObjectPanel):
    ID = "TemplateMappingCreate"
    CSS_SELECTOR_LOCATOR: Locator = ".RightPanel"
    CSS_SELECTOR: Locator = "TemplateMappingCreate"

    def template_mapping_type_dropdown(self):
        return self.element_by_css_selector("type")

    def template_mapping_type_attribute(self):
        return self.element_by_css_selector("type div[id$='-option-0']")

    def template_mapping_type_group(self):
        return self.element_by_css_selector("type div[id$='-option-1']")

    def template_mapping_type_default(self):
        return self.element_by_css_selector("type div[id$='-option-2']")

    def group_value_input(self, value):
        input_field = self.element_by_css_selector("values input")
        overwrite_input(input_field, value)

    def attribute_field_input(self, value):
        input_field = self.element_by_id("field")
        overwrite_input(input_field, value)

    def attribute_values_input(self, value):
        input_field = self.element_by_css_selector("values input")
        overwrite_input(input_field, value)

    def template_choice_dropdown(self):
        return self.element_by_css_selector("template div div")

    def template_choice_first_template(self):
        return self.element_by_css_selector("template div[id$='-option-0']")

    def description_input_field(self, description):
        descriptions = self.element_by_id("description")
        overwrite_input(descriptions, description)
