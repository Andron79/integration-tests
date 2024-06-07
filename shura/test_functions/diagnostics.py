import time
from selenium.common import TimeoutException, NoSuchElementException
from common.service_utils import file_exist
from shura.pages.diagnostics_page import DiagnosticsPage, DiagnosticsPanel
from shura.test_data.constants import (
    diagnostics_max_wait,
    diagnostics_download_result_max_wait,
)


def clear_diagnostics(diagnostics_page: DiagnosticsPage):
    """Очистка результатов диагностики.

    :param diagnostics_page:
    """
    diagnostics_panel = DiagnosticsPanel.from_page_obj(diagnostics_page)
    diagnostics_panel.clear_diagnostics_btn().click()
    diagnostics_page.popup_confirm()


def start_diagnostics(diagnostics_panel: DiagnosticsPanel):
    """Старт диагностики.

    :param diagnostics_panel:
    """
    diagnostics_panel.start_diagnostics_btn().click()


def set_diagnostics_steps(diagnostics_panel: DiagnosticsPanel):
    """Установка шагов диагностики.

    :param diagnostics_panel:
    """
    diagnostics_panel.diagnostics_type(ordinal=1).click()
    diagnostics_panel.select_containers_status().click()
    diagnostics_panel.add_diagnostics_step_btn().click()

    diagnostics_panel.diagnostics_type(ordinal=2).click()
    diagnostics_panel.select_containers_logs().click()
    diagnostics_panel.add_diagnostics_step_btn().click()

    diagnostics_panel.diagnostics_type(ordinal=3).click()
    diagnostics_panel.select_collect_container_statistic().click()


def get_diagnostics_step_count(diagnostics_panel: DiagnosticsPanel) -> int:
    return len(diagnostics_panel.get_diagnostics_step_list())


def diagnostics_in_progress(diagnostics_panel: DiagnosticsPanel) -> bool:
    try:
        diagnostics_panel.diagnostics_in_progress_status()
    except TimeoutException:
        return False
    except NoSuchElementException:
        return False
    return True


def wait_until_diagnostics_complete(diagnostics_panel: DiagnosticsPanel) -> bool:
    """Ожидание окончания диагностики.

    :param diagnostics_panel:
    :return:
    """
    start = time.perf_counter()
    while diagnostics_running := diagnostics_in_progress(diagnostics_panel):
        if time.perf_counter() - start > diagnostics_max_wait:
            raise TimeoutException(
                f"Превышено максимальное время диагностики: {diagnostics_max_wait} сек."
            )
    return not diagnostics_running


def download_diagnostics_result(diagnostics_panel: DiagnosticsPanel, file=None):
    """
    :param file: Название файла архива
    :param diagnostics_panel:
    :return:
    """
    # diagnostics_panel
    diagnostics_panel.download_diagnostics_result_btn().click()

    start = time.perf_counter()
    while not (is_file_exist := file_exist(file=file)):
        if time.perf_counter() - start > diagnostics_download_result_max_wait:
            raise TimeoutException(
                f"Превышено максимальное время скачивания результатов диагностики: {diagnostics_max_wait} сек."
            )
    return is_file_exist


def set_password_for_result(diagnostics_panel):
    diagnostics_panel.set_password_checkbox()


def clear_password_for_result(diagnostics_panel):
    diagnostics_panel.clear_password_checkbox()


def archive_password(diagnostics_panel):
    return diagnostics_panel.get_zip_password()
