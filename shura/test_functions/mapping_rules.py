import time

from shura.pages.mapping_rules_page import (
    TemplateMappingRulesPanel,
    TemplateMappingRulesPage,
)
from shura.panels.popup import Popup
from shura.settings import SAVE_PANEL_DELAY


def create_mapping_rules_group(
    mapping_rules_page: TemplateMappingRulesPage, value: str, descriptions: str
):
    """Тест создания Правила сопоставления шаблонов с типом Группа."""

    mapping_rules_page.close_alerts()
    mapping_rules_page.combo_btn_add().click()
    mapping_rules_panel = TemplateMappingRulesPanel.from_page_obj(mapping_rules_page)
    mapping_rules_panel.template_mapping_type_dropdown().click()
    mapping_rules_panel.template_mapping_type_group().click()
    mapping_rules_panel.group_value_input(value)
    mapping_rules_panel.template_choice_dropdown().click()
    mapping_rules_panel.template_choice_first_template().click()
    mapping_rules_panel.description_input_field(descriptions)
    mapping_rules_panel.save_changes_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
    mapping_rules_page.close_alerts()


def update_mapping_rules_group(
    mapping_rules_page: TemplateMappingRulesPage,
    update_value: str,
    update_descriptions: str,
):
    """Тест изменения Правила сопоставления шаблонов с типом Группа."""

    mapping_rules_page.select_mapping_rule().click()
    mapping_rules_panel = TemplateMappingRulesPanel.from_page_obj(mapping_rules_page)
    mapping_rules_panel.group_value_input(update_value)
    mapping_rules_panel.template_choice_dropdown().click()
    mapping_rules_panel.template_choice_first_template().click()
    mapping_rules_panel.description_input_field(update_descriptions)
    mapping_rules_panel.save_changes_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
    mapping_rules_page.close_alerts()


def delete_mapping_rules(mapping_rules_page: TemplateMappingRulesPage):
    """Тест удаление всех сопоставлений."""

    mapping_rules_page.select_first_mapping_rules().click()
    mapping_rules_page.combo_btn_del().click()
    time.sleep(SAVE_PANEL_DELAY)
    popup = Popup.from_page_obj(mapping_rules_page)
    popup.confirm().click()
    mapping_rules_page.close_alerts()


def create_mapping_rules_attribute(
    mapping_rules_page: TemplateMappingRulesPage,
    field: str,
    value: str,
    description: str,
):
    """Тест создания Правила сопоставления шаблонов с типом Атрибут."""

    mapping_rules_page.combo_btn_add().click()
    mapping_rules_panel = TemplateMappingRulesPanel.from_page_obj(mapping_rules_page)
    mapping_rules_panel.template_mapping_type_dropdown().click()
    mapping_rules_panel.template_mapping_type_attribute().click()
    mapping_rules_panel.attribute_field_input(field)
    mapping_rules_panel.attribute_values_input(value)
    mapping_rules_panel.template_choice_dropdown().click()
    mapping_rules_panel.template_choice_first_template().click()
    mapping_rules_panel.description_input_field(description)
    mapping_rules_panel.save_changes_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
    mapping_rules_page.close_alerts()


def update_mapping_rules_attribute(
    mapping_rules_page: TemplateMappingRulesPage,
    update_field: str,
    update_value: str,
    update_description: str,
):
    """Тест изменения Правила сопоставления шаблонов с типом Атрибут."""

    mapping_rules_page.select_mapping_rule().click()
    mapping_rules_panel = TemplateMappingRulesPanel.from_page_obj(mapping_rules_page)
    mapping_rules_panel.template_mapping_type_dropdown().click()
    mapping_rules_panel.template_mapping_type_attribute().click()
    mapping_rules_panel.attribute_field_input(update_field)
    mapping_rules_panel.attribute_values_input(update_value)
    mapping_rules_panel.template_choice_dropdown().click()
    mapping_rules_panel.template_choice_first_template().click()
    mapping_rules_panel.description_input_field(update_description)
    mapping_rules_panel.save_changes_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
    mapping_rules_page.close_alerts()


def create_mapping_rules_default(
    mapping_rules_page: TemplateMappingRulesPage, descriptions: str
):
    """Тест создание Правила сопоставления шаблонов с типом По умолчанию."""

    mapping_rules_page.combo_btn_add().click()
    mapping_rules_panel = TemplateMappingRulesPanel.from_page_obj(mapping_rules_page)
    mapping_rules_panel.template_mapping_type_dropdown().click()
    mapping_rules_panel.template_mapping_type_default().click()
    mapping_rules_panel.template_choice_dropdown().click()
    mapping_rules_panel.template_choice_first_template().click()
    mapping_rules_panel.description_input_field(descriptions)
    mapping_rules_panel.save_changes_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
    mapping_rules_page.close_alerts()


def update_mapping_rules_default(
    mapping_rules_page: TemplateMappingRulesPage, descriptions: str
):
    """Тест изменение Правила сопоставления шаблонов с типом По умолчанию."""

    mapping_rules_page.select_mapping_rule().click()
    mapping_rules_panel = TemplateMappingRulesPanel.from_page_obj(mapping_rules_page)
    mapping_rules_panel.template_mapping_type_dropdown().click()
    mapping_rules_panel.template_mapping_type_default().click()
    mapping_rules_panel.template_choice_dropdown().click()
    mapping_rules_panel.template_choice_first_template().click()
    mapping_rules_panel.description_input_field(descriptions)
    mapping_rules_panel.save_changes_btn().click()
    time.sleep(SAVE_PANEL_DELAY)
