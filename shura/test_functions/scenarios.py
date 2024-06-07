import logging

from selenium.common import TimeoutException, NoSuchElementException

from shura.pages.scenarios_page import ScenarioPage, ScenarioPanel
from shura.test_data.constants import ScenarioSchedule, Day, DebugMode

logger = logging.getLogger(__name__)


def create_scenario_by_request(scenario_page: ScenarioPage, title: str):
    """Создание сценария по запросу.

    :param title: название сценария.
    :param scenario_page: Страница сценариев
    """

    scenario_page.combo_btn_add().click()
    scenario_panel = ScenarioPanel.from_page_obj(scenario_page)
    scenario_panel.set_scenario_title(title=title)
    scenario_panel.select_scenario_targets_all().click()
    scenario_panel.select_scenario_task_debug_mode(DebugMode.ON).click()
    scenario_panel.scenario_add_step_command().click()
    scenario_panel.select_scenario_task_users_kickoff().click()
    scenario_panel.save_btn().click()
    scenario_page.close_alerts()


def update_scenario_by_request(scenario_page: ScenarioPage, title: str, new_title: str):
    """Изменение сценария по запросу.

    :param new_title: Новое название сценария.
    :param title: Название сценария.
    :param scenario_page: Страница сценариев
    """
    scenario_page.select_item(title).click()
    scenario_panel = ScenarioPanel.from_page_obj(scenario_page)
    scenario_panel.set_scenario_title(title=new_title)
    scenario_panel.select_scenario_task_debug_mode(DebugMode.OFF).click()
    scenario_panel.save_btn().click()
    scenario_page.close_alerts()


def create_scenario_by_trigger(scenario_page: ScenarioPage, title: str):
    """Создание сценария по событию.

    :param title: название сценария.
    :param scenario_page: Страница сценариев
    """

    scenario_page.combo_btn_add().click()
    scenario_panel = ScenarioPanel.from_page_obj(scenario_page)
    scenario_panel.set_scenario_title(title=title)
    scenario_panel.scenario_start_mode().click()
    scenario_panel.select_scenario_option_by_trigger().click()
    scenario_panel.select_scenario_trigger_all_new().click()
    scenario_panel.select_scenario_task_debug_mode(DebugMode.ON).click()
    scenario_panel.scenario_add_step_command().click()
    scenario_panel.select_scenario_task_users_kickoff().click()
    scenario_panel.save_btn().click()
    scenario_page.close_alerts()


def update_scenario_by_trigger(scenario_page: ScenarioPage, title: str, new_title: str):
    """Изменение сценария по событию.

    :param new_title: Новое название сценария.
    :param title: Название сценария.
    :param scenario_page: Страница сценариев
    """
    scenario_page.select_item(title).click()
    scenario_panel = ScenarioPanel.from_page_obj(scenario_page)
    scenario_panel.set_scenario_title(title=new_title)
    scenario_panel.select_scenario_option_by_trigger()
    scenario_panel.select_scenario_trigger_just_configured()
    scenario_panel.select_scenario_task_debug_mode(DebugMode.OFF).click()
    scenario_panel.save_btn().click()
    scenario_page.close_alerts()


def create_scenario_by_scheduler(
    scenario_page: ScenarioPage,
    title: str,
    scheduler: ScenarioSchedule,
    start_time: str,
    day: Day,
    day_in_month: int,
) -> None:
    """Создание сценария по расписанию.

    :param day_in_month: Число месяца. -1 Последний день месяца.
    :param day: День недели старта сценария
    :param start_time: время старта сценария
    :param scheduler: расписание запуска сценариев
    :param title: Название сценария.
    :param scenario_page: Страница сценариев
    """

    scenario_page.combo_btn_add().click()
    scenario_panel = ScenarioPanel.from_page_obj(scenario_page)
    scenario_panel.set_scenario_title(title=title)
    scenario_panel.scenario_start_mode().click()
    scenario_panel.select_scenario_option_by_scheduler().click()
    scenario_panel.select_scenario_target_all().click()
    if scheduler.DAILY:
        scenario_panel.scheduler_input_start_time().send_keys(start_time)
    elif scheduler.WEEKLY:
        scenario_panel.select_scheduler_weekly().click()
        scenario_panel.select_scheduler_start_day(day=day).click()
        scenario_panel.scheduler_input_start_time().send_keys(start_time)
    elif scheduler.MONTHLY:
        scenario_panel.select_scheduler_monthly().click()
        scenario_panel.select_scheduler_date(day_in_month=day_in_month).click()
        scenario_panel.scheduler_input_start_time().send_keys(start_time)
    scenario_panel.select_scenario_task_debug_mode(DebugMode.ON).click()
    scenario_panel.scenario_add_step_command().click()
    scenario_panel.select_scenario_task_users_kickoff().click()
    scenario_panel.save_btn().click()
    scenario_page.close_alerts()


def update_scenario_by_scheduler(
    scenario_page: ScenarioPage, title: str, new_title: str, start_time: str
) -> None:
    """Изменение сценария по событию.

    :param start_time: время старта сценария
    :param new_title: Новое название сценария.
    :param title: Название сценария.
    :param scenario_page: Страница сценариев
    """
    scenario_page.select_item(title).click()
    scenario_panel = ScenarioPanel.from_page_obj(scenario_page)
    scenario_panel.set_scenario_title(title=new_title)
    scenario_panel.scenario_start_mode().click()
    scenario_panel.scheduler_input_start_time().send_keys(start_time)
    scenario_panel.select_scenario_task_debug_mode(DebugMode.OFF).click()
    scenario_panel.save_btn().click()
    scenario_page.close_alerts()


def start_scenario(scenario_page: ScenarioPage, title: str):
    """Старт сценария по запросу.

    :param title: Название сценария.
    :param scenario_page: Страница сценариев
    """
    scenario_page.select_item(title).click()
    scenario_panel = ScenarioPanel.from_page_obj(scenario_page)
    scenario_panel.save_and_run_btn().click()
    scenario_page.close_alerts()
    scenario_panel.history_tab().click()


def delete_scenario(scenario_page: ScenarioPage, title: str):
    """Удаление сценария.

    :param title: название сценария.
    :param scenario_page: Страница сценариев
    """

    scenario_page.select_checkbox(title).click()
    scenario_page.combo_btn_del().click()
    scenario_page.popup_confirm()
    scenario_page.close_alerts()


def scenario_complete(scenario_panel) -> bool:
    try:
        scenario_panel.scenario_in_complete_status()
    except TimeoutException:
        return False
    except NoSuchElementException:
        return False
    return True


def input_scenario_filter_by_name(scenario_page: ScenarioPage, title: str) -> None:
    """

    :param title: название сценария.
    :param scenario_page: Страница сценариев
    :return: None
    """
    scenario_page.set_filter(title)
    scenario_page.table_filter_btn().click()
    scenario_page.close_alerts()
