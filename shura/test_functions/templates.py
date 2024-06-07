import logging

from shura.pages.templates_page import TemplateDefinitionPage, TemplateDefinitionPanel

logger = logging.getLogger(__name__)


def create_template(template_page: TemplateDefinitionPage, profile_template: dict):
    """

    :param template_page: Страница шаблонов
    :param profile_template: Профиль шаблона
    :return:
    """
    template_page.combo_button()
    template_page.combo_btn_add().click()
    template_panel = TemplateDefinitionPanel.from_page_obj(template_page)
    template_panel.gm_mode().click()
    template_panel.terminal_mode().click()
    template_panel.fill_panel_with_data(
        profile_template, start_delay=0.2, input_delay=0
    )
    template_panel.save_changes_and_exit_btn().click()
    template_page.close_alerts()


def update_template(
    template_page: TemplateDefinitionPage,
    profile_template: dict,
    update_profile_template: dict,
):
    """Изменение шаблона.

    :param template_page: Страница шаблонов
    :param profile_template: Профиль шаблона
    :param update_profile_template: Измененный профиль
    :return: Словарь с данными из измененного профиля
    """
    template_page.template_present(profile_template["name"]).click()
    template_panel = TemplateDefinitionPanel.from_page_obj(template_page)
    template_panel.fill_panel_with_data(
        update_profile_template, start_delay=0.2, input_delay=0
    )
    template_panel.save_changes_and_exit_btn().click()
    template_page.close_alerts()


def get_template_data(
    template_page: TemplateDefinitionPage, update_profile_template: dict
) -> dict:
    template_page.template_present(update_profile_template["name"]).click()
    template_panel = TemplateDefinitionPanel.from_page_obj(template_page)

    template_profile = template_panel.template_profile()
    template_panel.close_panel_without_save().click()

    return template_profile


def delete_template(template_page: TemplateDefinitionPage, profile_template_title: str):
    """Удаление шаблона.

    :param template_page: Страница шаблонов
    :param profile_template_title: Имя шаблона
    :return:
    """
    template_page.select_checkbox(profile_template_title).click()
    template_page.combo_btn_del().click()
    template_page.popup_confirm()
    template_page.close_alerts()
