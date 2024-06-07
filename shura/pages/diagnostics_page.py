from typing import List

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from shura.pages.base import InternalPage
from shura.panels.base import Locator
from shura.panels.object import ObjectPanel

logger = logging.getLogger(__name__)


class DiagnosticsPage(InternalPage):
    ...


class DiagnosticsPanel(ObjectPanel):
    ID = "CreateDiagnostics"
    CSS_SELECTOR_LOCATOR: Locator = ".CreateDiagnostics.MainPanel"

    def clear_diagnostics_btn(self) -> WebElement:
        """
        :return: Кнопка очистки результатов диагностики
        """
        return WebDriverWait(self.root, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"button.{self.ID}__clear-command")
            )
        )

    def start_diagnostics_btn(self) -> WebElement:
        """
        :return: Кнопка старта диагностики
        """
        return self.root.find_element(
            By.CSS_SELECTOR, f"footer.{self.ID}__footer > button.btn.btn-primary"
        )

    def add_diagnostics_step_btn(self) -> WebElement:
        """
        :return: Кнопка добавления шага диагностики.
        """
        return WebDriverWait(self.root, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"button.{self.ID}__add-command")
            )
        )

    def download_diagnostics_result_btn(self) -> WebElement:
        """
        :return: Кнопка Скачать результаты диагностики
        """
        return self.root.find_element(By.ID, "DiagnosticsResult__archive-download")

    def get_diagnostics_step_list(self) -> List[WebElement]:
        return self.root.find_elements(
            By.CSS_SELECTOR, "div[class$='-indicatorContainer']"
        )

    def diagnostics_in_progress_status(self) -> WebElement:
        """
        :return: Баннер Диагностика в процессе
        """
        return self.root.find_element(
            By.CSS_SELECTOR, ".DiagnosticsResult__status.info"
        )

    def diagnostics_in_complete_status(self) -> WebElement:
        """
        :return: Баннер Диагностика завершена успешно
        """
        return self.root.find_element(
            By.CSS_SELECTOR, ".DiagnosticsResult__status.success"
        )

    def diagnostics_type(self, ordinal: int = 0) -> WebElement:
        """
        :param ordinal: Порядковый номер шага диагностики.
        :return: Кнопка выбора типа диагностики
        """
        return self.get_diagnostics_step_list()[ordinal - 1]

    def select_containers_status(self) -> WebElement:
        """
        :return: Элемент из выпадающего списка Статусы контейнеров
        """
        return self.root.find_element(By.ID, "select-option__docker_ps")

    def select_containers_logs(self) -> WebElement:
        """
        :return: Элемент из выпадающего списка Логи контейнеров
        """
        return self.root.find_element(By.ID, "select-option__docker_logs")

    def select_collect_container_statistic(self) -> WebElement:
        """
        :return: Элемент из выпадающего списка Статистика потребления ресурсов сервисами
        """
        return self.root.find_element(By.ID, "select-option__docker_stats")

    def set_password_checkbox(self):
        """Устанавливает пароль на результаты диагностики.

        :return:
        """
        try:
            pass_checkbox = self.root.find_element(
                By.CSS_SELECTOR, ".CreateDiagnostics__encryptArchive .checkmark.checked"
            )
        except NoSuchElementException:
            pass_checkbox = self.root.find_element(
                By.CSS_SELECTOR, ".checkmark"
            ).click()
        return pass_checkbox

    def get_zip_password(self) -> str:
        return self.root.find_element(
            By.ID, "diagnostics-archive-password"
        ).get_attribute("value")

    def clear_password_checkbox(self):
        """Убирает пароль на результаты диагностики.

        :return:
        """
        try:
            pass_checkbox = self.root.find_element(
                By.CSS_SELECTOR, ".CreateDiagnostics__encryptArchive .checkmark.checked"
            )
            pass_checkbox.click()
        except NoSuchElementException:
            pass_checkbox = self.root.find_element(
                By.CSS_SELECTOR, ".CreateDiagnostics__encryptArchive .checkmark"
            )
        return pass_checkbox
