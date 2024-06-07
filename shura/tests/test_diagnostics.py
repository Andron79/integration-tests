import logging

from common.service_utils import empty_files_in_archive
from shura.test_data.constants import result_zip_file
from shura.test_functions.diagnostics import (
    set_diagnostics_steps,
    clear_diagnostics,
    start_diagnostics,
    get_diagnostics_step_count,
    diagnostics_in_progress,
    wait_until_diagnostics_complete,
    download_diagnostics_result,
    clear_password_for_result,
    set_password_for_result,
    archive_password,
)

logger = logging.getLogger(__name__)


def test_diagnostics_no_archive_password(diagnostics_panel, diagnostics_page):
    clear_diagnostics(diagnostics_page)

    clear_password_for_result(diagnostics_panel)
    logger.info("Архив будет без пароля")

    assert (
        get_diagnostics_step_count(diagnostics_panel) == 1
    ), "Очистка шагов диагностики завершилась не успешно "
    logger.info("Шаги диагностики очищены - OK!")

    set_diagnostics_steps(diagnostics_panel)

    assert (
        get_diagnostics_step_count(diagnostics_panel) == 3
    ), "Установка шагов диагностики завершена не успешно - ERROR"
    logger.info("Шаги диагностики установлены - OK!")

    start_diagnostics(diagnostics_panel)
    logger.info('Стартует диагностика без установки пароля на результаты" - OK!')

    assert diagnostics_in_progress(
        diagnostics_panel
    ), "Старт диагностики не удался - ERROR"
    logger.info("Диагностика стартовала - OK!")

    assert wait_until_diagnostics_complete(
        diagnostics_panel
    ), "Диагностика прервана по таймауту - ERROR!"
    logger.info("Диагностика окончена - OK!")

    assert download_diagnostics_result(
        diagnostics_panel, result_zip_file
    ), "Результат диагностики не загружен - ERROR"
    logger.info("Результат диагностики загружен - OK!")

    empty_log_files = empty_files_in_archive(result_zip_file)
    assert not empty_log_files, f"Получено {len(empty_log_files)} пустых файлов логов"
    logger.info("Пустые файлы логов отсутствуют - OK!")


def test_diagnostics_with_archive_password(diagnostics_panel, diagnostics_page):
    clear_diagnostics(diagnostics_page)

    assert (
        get_diagnostics_step_count(diagnostics_panel) == 1
    ), "Очистка шагов диагностики завершилась не успешно"
    logger.info("Шаги диагностики очищены - OK!")

    set_password_for_result(diagnostics_panel)
    logger.info("Архив будет с паролем")

    set_diagnostics_steps(diagnostics_panel)

    assert (
        get_diagnostics_step_count(diagnostics_panel) == 3
    ), "Установка шагов диагностики завершена не успешно - ERROR"
    logger.info("Шаги диагностики установлены - OK!")

    start_diagnostics(diagnostics_panel)
    logger.info("Стартует диагностика с установкой пароля на результаты - OK!")

    assert diagnostics_in_progress(
        diagnostics_panel
    ), "Старт диагностики не удался - ERROR"
    logger.info("Диагностика стартовала - OK!")

    assert wait_until_diagnostics_complete(
        diagnostics_panel
    ), "Диагностика прервана по таймауту - ERROR!"
    logger.info("Диагностика окончена - OK!")

    password = archive_password(diagnostics_panel)
    logger.info(f"Пароль архива: {password}")

    assert download_diagnostics_result(
        diagnostics_panel, result_zip_file
    ), "Результат диагностики не загружен - ERROR"
    logger.info("Результат диагностики загружен - OK!")

    empty_log_files = empty_files_in_archive(result_zip_file, zip_pass=password)
    assert not empty_log_files, f"Получено {len(empty_log_files)} пустых файлов логов"
    logger.info("Пустые файлы логов отсутствуют - OK!")
    logger.info("Всем добра и много денег - OK!")
