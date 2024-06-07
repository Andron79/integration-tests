import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.service_utils import overwrite_input
from shura.pages.base import ItemsTablePage
from shura.panels.base import Locator
from shura.panels.object import ObjectPanel
from shura.test_data.constants import Day, DebugMode

logger = logging.getLogger(__name__)


class ScenarioPage(ItemsTablePage):
    ...


class ScenarioPanel(ObjectPanel):
    ID = "ScenariosEditTab"
    CSS_SELECTOR_LOCATOR: Locator = ".ScenariosEditTab"

    def set_scenario_title(self, title):
        """
        :return: Добавляет название Сценария
        """
        input_field = self.root.find_element(By.ID, "scenario__title")
        overwrite_input(input_field, title)

    def scenario_start_mode(self) -> WebElement:
        """
        :return: Элемент выбора режима сценария
        """
        return self.root.find_element(By.ID, "scenario__start-mode")

    def select_scenario_option_by_trigger(self) -> WebElement:
        """
        :return: Элемент выбора режима сценария по событию
        """
        return self.root.find_element(By.ID, "select-option__TRIGGERED")

    def select_scenario_trigger_just_configured(self) -> WebElement:
        """
        :return: Элемент выбора события вновь настроенные
        """
        self.scenario_trigger_panel().click()
        return self.root.find_element(By.ID, "select-option__JUST_CONFIGURED")

    def select_scenario_option_by_scheduler(self) -> WebElement:
        """
        :return: Элемент выбора режима сценария по расписанию
        """
        return self.root.find_element(By.ID, "select-option__SCHEDULED")

    def _scenario_targets(self) -> WebElement:
        """
        :return: Элемент выбора устройств для сценария
        """
        return self.root.find_element(By.ID, "scenario__targets")

    def select_scenario_targets_all(self) -> WebElement:
        """
        :return: Элемент выбора всех устройств для сценария
        """
        self._scenario_targets().click()
        return self.root.find_element(By.ID, "select-option__ALL")

    def _scenario_task_panel(self) -> WebElement:
        """
        :return: Элемент выбора задания
        """
        return self.root.find_element(By.CLASS_NAME, "TaskChainItem__panel")

    def scenario_trigger_panel(self) -> WebElement:
        """
        :return: Элемент выбора события
        """
        return self.root.find_element(By.ID, "scenario__triggers")

    def scenario_target_panel(self) -> WebElement:
        """
        :return: Элемент выбора события
        """
        return self.root.find_element(By.ID, "scenario__targets")

    def select_scenario_trigger_all_new(self) -> WebElement:
        """
        :return: Элемент выбора события все подключенные
        """
        self.scenario_trigger_panel().click()
        return self.root.find_element(By.ID, "select-option__ALL_NEW")

    def select_scenario_target_all(self) -> WebElement:
        """
        :return: Элемент выбора события все подключенные
        """
        self.scenario_target_panel().click()
        return self.root.find_element(By.ID, "select-option__ALL")

    def _scenario_task_panel_2(self):
        """
        :return: Элемент выбора задания на второй панели
        """
        return self.root.find_element(
            By.CSS_SELECTOR, ".TaskChainItem:nth-child(2) .TaskChainItem__panel"
        )

    def select_scenario_task_debug_mode(
        self, debug_mode: DebugMode = DebugMode.ON
    ) -> WebElement:
        """
        :param debug_mode
        :return: Элемент выбора задания Debug mode
        """
        self._scenario_task_panel().click()
        return self.root.find_element(
            By.ID, f"select-option__Debug mode {debug_mode.name}"
        )

    def select_scenario_task_users_kickoff(self) -> WebElement:
        """
        :return: Элемент выбора задания Users kickoff
        """
        self._scenario_task_panel_2().click()
        return self.root.find_element(By.ID, "select-option__User's kickoff")

    def _scenario_scheduler_input_start_time(self) -> WebElement:
        """
        :return: Поле ввода времени старта сценария
        """
        return self.root.find_element(By.ID, "schedule.time")

    def scheduler_input_start_time(self) -> WebElement:
        """
        Поиск элемента не работает с драйвером root
        :return: Поле ввода времени старта сценария
        """
        self._scenario_scheduler_input_start_time().click()
        return self.driver.find_element(By.CLASS_NAME, "rc-time-picker-panel-input")

    def select_scheduler_weekly(self) -> WebElement:
        """
        :return: Элемент выбора еженедельного расписания.
        """
        self.root.find_element(By.ID, "scenario__execution-frequency").click()
        return self.root.find_element(By.ID, "select-option__WEEKLY")

    def select_scheduler_start_day(self, day: Day = Day.MONDAY) -> WebElement:
        """
        :param day
        :return: Элемент выбора дня недели.
        """
        return self.root.find_element(
            By.CSS_SELECTOR,
            f'.SelectDayOfWeek__label label[for="SelectDayOfWeek_{day.value}"]',
        )

    def select_scheduler_monthly(self) -> WebElement:
        """
        :return: Элемент выбора ежемесячного расписания.
        """
        self.root.find_element(By.ID, "scenario__execution-frequency").click()
        return self.root.find_element(By.ID, "select-option__MONTHLY")

    def select_scheduler_date(self, day_in_month: int = -1) -> WebElement:
        """
        :param day_in_month порядковый номер дня в месяце (1-30). Значение -1 последний день месяца
        :return: Элемент выбора даты старта - последний день месяца.
        """
        return self.root.find_element(
            By.CSS_SELECTOR,
            f'.SelectDayOfMonth label[for="SelectDayOfMonth_{day_in_month}"]',
        )

    def scenario_add_step_command(self) -> WebElement:
        """
        :return: Элемент шаг сценария
        """
        return self.root.find_element(By.CLASS_NAME, "CreateDiagnostics__add-command")

    def save_btn(self) -> WebElement:
        """
        :return: Элемент сохранить сценарий
        """
        return self.driver.find_element(By.ID, "Btn__submit-saveAnsClose")

    def save_and_run_btn(self) -> WebElement:
        """
        :return: Элемент сохранить и запустить сценарий
        """
        return self.driver.find_element(By.ID, "Btn__submit-saveAndRun")

    def close_btn(self) -> WebElement:
        """
        :return: Элемент крестик закрытия страницы
        """
        return self.driver.find_element(By.ID, "Btn__close-form")

    def back_btn(self) -> WebElement:
        """
        :return: Элемент стрелка назад, возврат на предыдущую страницу
        """
        return self.driver.find_element(By.ID, "Btn__back")

    def history_tab(self) -> WebElement:
        """
        :return: Элемент вкладка История
        """
        return self.driver.find_element(By.XPATH, "//li[2]/button")

    def scenario_in_complete_status(self) -> WebElement:
        """
        :return: Сценарий завершен успешно
        """
        return WebDriverWait(self.root, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".Label.success"))
        )
