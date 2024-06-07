import logging
import os
import time
from contextlib import contextmanager
from pathlib import Path

import pytest
import requests

from common.settings import GMSERVER_ADDRESS
from shura.pages.applications_page import ApplicationsPage
from shura.pages.device_groups_page import DeviceGroupsPage
from shura.pages.devices_page import DevicesPage
from shura.pages.diagnostics_page import DiagnosticsPanel
from shura.pages.journal_page import JournalPage
from shura.pages.scenarios_page import ScenarioPage
from shura.pages.settings_page import AdSynchronization
from shura.pages.summary_page import SummaryPage
from shura.panels.nav import NavPanel
from shura.panels.tab import TabPanel
from shura.settings import SYNC_SETTINGS_RESPONSE_DELAY, CLEAR_TEST_DATA
from shura.test_data.constants import (
    COMMAND_NAME_FOR_TASK,
    COMMAND_DATA,
    COMMAND_TYPE_CONFIGURATION,
    COMMAND_FOR_ROLES,
    NEW_TASK_NAME,
    new_license,
    TEST_PROFILE_TEMPLATE,
    DEFAULT_COMPANY_ADDRESS,
    SCENARIOS,
    TASKS_NAMES_FOR_SEARCH_AND_FILTERING,
    TASKS_COMMANDS_FOR_SEARCH_AND_FILTERING,
    Roles,
    TEST_USER_PROFILE,
    SUPERADMIN_USERNAME,
    SUPERADMIN_PASSWORD,
)

from shura.test_functions.companies import update_company_address

from shura.test_functions.device_groups import delete_group_with_devices
from shura.test_functions.login_logout import user_logout, login_to_server
from shura.test_functions.mapping_rules import delete_mapping_rules
from shura.test_functions.roles import create_readonly_role
from shura.test_functions.scenarios import delete_scenario
from shura.test_functions.tasks import delete_task, create_task_for_predefined_command
from shura.test_functions.templates import delete_template, create_template
from shura.test_data import constants
from shura.test_functions.commands import create_command, delete_command
from shura.test_functions.updates import delete_firmware
from shura.test_functions.users import create_user, delete_user

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def browser(driver):
    logger.info(
        f"Запускается сессия тестирования на {GMSERVER_ADDRESS} "
        f"{'с очисткой данных' if CLEAR_TEST_DATA else 'без очистки данных'}"
    )
    page = driver.login_in_server()
    yield page
    driver.logout()


@contextmanager
def download_file(url: str) -> str:
    filepath = Path().absolute() / Path(url).name
    response = requests.get(url, verify=False)
    with filepath.open("wb") as f:
        f.write(response.content)
    yield str(filepath)
    filepath.unlink(missing_ok=True)


# При scope="session" pytest пытается оптимизировать использование fixture и нарушает порядок вызова тестов
@pytest.fixture(scope="class")
def downloaded_file(request):
    with download_file(request.param) as filepath:
        yield filepath


@pytest.fixture
def sync_page(browser):
    nav_bar = NavPanel.from_page_obj(browser)
    page = nav_bar.goto_settings_page()
    page.refresh()
    time.sleep(SYNC_SETTINGS_RESPONSE_DELAY)

    yield page


@pytest.fixture
def ad_panel(sync_page):
    yield AdSynchronization.from_page_obj(sync_page)


@pytest.fixture(scope="module")
def commands_page(browser):
    nav_bar = NavPanel.from_page_obj(browser)
    command_page = nav_bar.goto_commands_page()

    if command_page.list_item_exists(constants.COMMAND_NAME):
        delete_command(commands_page=command_page, command_name=constants.COMMAND_NAME)
        logger.info(
            "Предварительная очистка перед тестом страницы команд: Старая команда была удалена фикстурой - OK!"
        )
    command_page.close_alerts()
    yield command_page

    if command_page.list_item_exists(constants.COMMAND_NAME):
        delete_command(commands_page=command_page, command_name=constants.COMMAND_NAME)
        command_page.close_alerts()
        logger.info("Команда была удалена фикстурой - OK!")


@pytest.fixture
def updates_page(browser, downloaded_file):
    nav_bar = NavPanel.from_page_obj(browser)
    page = nav_bar.goto_updates_page()

    yield page

    nav_bar = NavPanel.from_page_obj(browser)
    updates_page = nav_bar.goto_updates_page()
    if updates_page.list_item_exists(os.path.basename(downloaded_file)):
        delete_firmware(updates_page, downloaded_file)
        logger.info("Прошивка была удалена фикстурой - OK!")


@pytest.fixture
def roles_page(browser):
    nav_bar = NavPanel.from_page_obj(browser)
    roles_page = nav_bar.goto_roles_page()
    roles_page.delete_no_predefined_items()

    yield roles_page

    logger.info("Стартует очистка страницы ролей")
    roles_page = nav_bar.goto_roles_page()
    roles_page.delete_no_predefined_items()
    logger.info("Закончена очистка страницы ролей")


@pytest.fixture(scope="module")
def readonly_role(driver, browser):
    nav_bar = NavPanel.from_page_obj(browser)
    readonly_role = nav_bar.goto_roles_page()
    readonly_role.delete_no_predefined_items()
    if not readonly_role.list_item_exists(f"{Roles.TEST_READONLY_ROLE.value}"):
        create_readonly_role(
            roles_page=readonly_role,
            name=f"{Roles.TEST_READONLY_ROLE.value}",
            description=Roles.TEST_READONLY_ROLE.value,
        )

    assert readonly_role.list_item_exists(
        f"{Roles.TEST_READONLY_ROLE.value}"
    ), "Readonly роль не была создана!"
    logger.info("Readonly роль создана - OK!")

    superadmin_available_nav_items = readonly_role.navigation_section_items
    assert (
        len(superadmin_available_nav_items) == 16  # Плюс пункт "выход/logout"
    ), f"Присутствует {len(superadmin_available_nav_items)} != 16 пунктов меню из 16 - ERROR"
    logger.info(
        f"Присутствует {len(superadmin_available_nav_items)} = 16 пунктов меню из 16 - OK! "
    )

    user_page = nav_bar.goto_user_page()
    if not user_page.list_item_exists(TEST_USER_PROFILE["username"]):
        create_user(
            user_page=user_page,
            username=TEST_USER_PROFILE["username"],
            password=TEST_USER_PROFILE["password"],
            title=Roles.TEST_READONLY_ROLE.value,
            role=Roles.TEST_READONLY_ROLE.value,
        )

    user_logout(driver)
    logger.info(
        f"Пользователь {SUPERADMIN_USERNAME} успешно разлогинился на сервере- OK!"
    )

    login_to_server(
        driver=driver,
        login=TEST_USER_PROFILE["username"],
        password=TEST_USER_PROFILE["password"],
    )

    yield readonly_role

    user_logout(driver)
    logger.info(
        f"Пользователь {TEST_USER_PROFILE['username']} успешно разлогинился на сервере- OK!"
    )
    login_to_server(
        driver=driver, login=SUPERADMIN_USERNAME, password=SUPERADMIN_PASSWORD
    )
    logger.info(
        f"Пользователь {SUPERADMIN_USERNAME} успешно авторизован на сервере- OK!"
    )

    logger.info("Удаление тестового пользователя")
    user_page = nav_bar.goto_user_page()
    delete_user(
        user_page=user_page,
        username=TEST_USER_PROFILE["username"],
        title=TEST_USER_PROFILE["title"],
    )
    logger.info("Тестовый пользователь удален.")

    logger.info("Стартует очистка страницы ролей")
    readonly_role = nav_bar.goto_roles_page()
    readonly_role.delete_no_predefined_items()
    logger.info("Закончена очистка страницы ролей")


@pytest.fixture
def task_page(browser):
    nav_bar = NavPanel.from_page_obj(browser)
    commands_page = nav_bar.goto_commands_page()

    create_command(
        commands_page=commands_page,
        command_name=COMMAND_NAME_FOR_TASK,
        command_data=COMMAND_DATA,
        command_type=COMMAND_TYPE_CONFIGURATION,
        command_for_roles=COMMAND_FOR_ROLES,
    )
    logger.info("Команда для Задания создана фикстурой - OK!")

    nav_bar = NavPanel.from_page_obj(browser)
    task_page = nav_bar.goto_tasks_page()

    yield task_page

    if task_page.list_item_exists(COMMAND_NAME_FOR_TASK):
        delete_task(task_page=task_page, new_task_name=NEW_TASK_NAME)
        task_page.close_alerts()
        logger.info("Задание удалено фикстурой - OK!")

    nav_bar = NavPanel.from_page_obj(browser)
    commands_page = nav_bar.goto_commands_page()
    if commands_page.list_item_exists(COMMAND_NAME_FOR_TASK):
        delete_command(commands_page=commands_page, command_name=COMMAND_NAME_FOR_TASK)
        commands_page.close_alerts()
        logger.info("Команда для Задания была удалена фикстурой - OK!")


@pytest.fixture
def task_page_with_tasks(browser):
    nav_bar = NavPanel.from_page_obj(browser)
    task_page = nav_bar.goto_tasks_page()
    for index, task_name in enumerate(TASKS_NAMES_FOR_SEARCH_AND_FILTERING):
        create_task_for_predefined_command(
            task_page=task_page,
            task_name=task_name,
            command_name=TASKS_COMMANDS_FOR_SEARCH_AND_FILTERING[index],
        )
        assert task_page.list_item_exists(task_name), f"Задание {task_name} не создано!"
        logger.info(f"Задание {task_name} создано фикстурой - OK!")

    yield task_page


@pytest.fixture(scope="session")
def user_page(browser):
    nav_bar = NavPanel.from_page_obj(browser)
    page = nav_bar.goto_user_page()

    yield page

    logger.info("Стартует очистка страницы пользователей")
    user_page = nav_bar.goto_user_page()
    user_page.clear_extra_items()
    logger.info("Закончена очистка страницы пользователей")


@pytest.fixture
def companies_page(browser):
    nav_bar = NavPanel.from_page_obj(browser)
    page = nav_bar.goto_companies_page()

    yield page

    update_company_address(companies_page=page, address=DEFAULT_COMPANY_ADDRESS)
    logger.info(
        f"Адрес по умолчанию {DEFAULT_COMPANY_ADDRESS} установлен фикстурой - OK!"
    )


@pytest.fixture(scope="module")
def mapping_rules_page(browser):
    template_page = NavPanel.from_page_obj(browser).goto_template_page()

    if not template_page.list_item_exists(constants.TEST_PROFILE_TEMPLATE["name"]):
        create_template(
            template_page=template_page,
            profile_template=constants.TEST_PROFILE_TEMPLATE,
        )

    mapping_rules_page = TabPanel.from_page_obj(
        browser
    ).goto_template_mapping_rules_page()

    yield mapping_rules_page

    mapping_rules_page = TabPanel.from_page_obj(
        browser
    ).goto_template_mapping_rules_page()

    if mapping_rules_page.get_mapping_rules_by_template(TEST_PROFILE_TEMPLATE["name"]):
        delete_mapping_rules(mapping_rules_page)
        logger.info("Правило сопоставления было удалено фикстурой - OK!")

    template_page = NavPanel.from_page_obj(browser).goto_template_page()
    if template_page.list_item_exists(constants.TEST_PROFILE_TEMPLATE["title"]):
        delete_template(
            template_page=template_page,
            profile_template_title=constants.TEST_PROFILE_TEMPLATE["title"],
        )
        logger.info("Шаблон был удален фикстурой - OK!")


@pytest.fixture(scope="module")
def templates_page(browser):
    template_page = NavPanel.from_page_obj(browser).goto_template_page()

    yield template_page

    if template_page.list_item_exists(constants.TEST_PROFILE_TEMPLATE["title"]):
        delete_template(
            template_page=template_page,
            profile_template_title=constants.TEST_PROFILE_TEMPLATE["title"],
        )
        logger.info("Шаблон был удален фикстурой - OK!")

    if template_page.list_item_exists(constants.TEST_PROFILE_TEMPLATE_UPDATE["title"]):
        delete_template(
            template_page=template_page,
            profile_template_title=constants.TEST_PROFILE_TEMPLATE_UPDATE["title"],
        )
        logger.info("Шаблон был удален фикстурой - OK!")


@pytest.fixture
def summary_page(browser) -> SummaryPage:
    yield NavPanel.from_page_obj(browser).goto_summary_page()


@pytest.fixture
def journal_page(browser) -> JournalPage:
    yield NavPanel.from_page_obj(browser).goto_journal_page()


@pytest.fixture
def applications_page(browser) -> ApplicationsPage:
    yield NavPanel.from_page_obj(browser).goto_applications_page()


@pytest.fixture
def device_page(browser) -> DevicesPage:
    yield NavPanel.from_page_obj(browser).goto_device_group_page()


@pytest.fixture
def device_group_page(browser) -> DeviceGroupsPage:
    device_group_page = NavPanel.from_page_obj(browser).goto_device_group_page()

    if device_group_page.group_exists(item=constants.TEST_GROUP_TITLE):
        delete_group_with_devices(
            device_group_page=device_group_page, title=constants.TEST_GROUP_TITLE
        )
        logger.info(
            "Предварительная очистка: группа и устройства были удалены фикстурой - OK!"
        )

    yield device_group_page

    if device_group_page.group_exists(item=constants.TEST_GROUP_TITLE):
        delete_group_with_devices(
            device_group_page=device_group_page, title=constants.TEST_GROUP_TITLE
        )
        logger.info(
            "Окончательная очистка: группа и устройства были удалены фикстурой - OK!"
        )


@pytest.fixture
def diagnostics_panel(diagnostics_page):
    panel = DiagnosticsPanel.from_page_obj(diagnostics_page)

    yield panel


@pytest.fixture
def diagnostics_page(browser):
    nav_bar = NavPanel.from_page_obj(browser)
    page = nav_bar.goto_diagnostics_page()
    page.close_alerts()

    yield page


@pytest.fixture(scope="function")
def scenario_page(browser) -> ScenarioPage:
    nav_bar = NavPanel.from_page_obj(browser)
    page = nav_bar.goto_scenario_page()

    yield page

    for scenario in SCENARIOS:
        if page.list_item_exists(scenario):
            delete_scenario(page, title=scenario)
            logger.info(
                f"Окончательная очистка: сценарий {scenario} был удален фикстурой - OK!"
            )


@pytest.fixture(autouse=True)
def close_alerts(browser):
    browser.close_alerts()

    yield


@pytest.fixture(scope="session", autouse=CLEAR_TEST_DATA)
def clear_all(browser):
    nav_bar = NavPanel.from_page_obj(browser)
    logger.info("Начинаю возврат состояния сервера к первоначальной установке")

    logger.info("Стартует загрузка лицензии")
    license_page = nav_bar.goto_license_page()
    with download_file(new_license) as filepath:
        license_page.upload_license(filepath)
    license_page.close_alerts()
    logger.info("Лицензия загружена!")

    logger.info(
        "Стартует остановка синхронизации и очистка несинхронизированных пользователей"
    )
    settings_page = nav_bar.goto_settings_page()
    ad_panel = AdSynchronization.from_page_obj(settings_page)
    ad_panel.clear_sync_settings()
    logger.info("Синхронизация остановлена, пользователи очищены")

    logger.info("Стартует очистка страницы пользователей")
    user_page = nav_bar.goto_user_page()
    user_page.clear_extra_items()
    user_page.close_alerts()
    logger.info("Закончена очистка страницы пользователей")

    logger.info("Стартует очистка страницы ролей")
    roles_page = nav_bar.goto_roles_page()
    roles_page.delete_no_predefined_items()
    roles_page.close_alerts()
    logger.info("Закончена очистка страницы ролей")

    logger.info("Стартует очистка страницы заданий")
    task_page = nav_bar.goto_tasks_page()
    task_page.clear_extra_items()
    task_page.close_alerts()
    logger.info("Закончена очистка страницы заданий")

    logger.info("Стартует очистка страницы обновлений")
    updates_page = nav_bar.goto_updates_page()
    updates_page.clear_extra_items()
    updates_page.close_alerts()
    logger.info("Закончена очистка страницы обновлений")

    logger.info("Стартует очистка страницы шаблонов")
    templates_page = nav_bar.goto_template_page()
    templates_page.clear_extra_items()
    templates_page.close_alerts()
    logger.info("Закончена очистка страницы шаблонов")

    logger.info(
        f"Стартует установка адреса компании по умолчанию {DEFAULT_COMPANY_ADDRESS}"
    )
    nav_bar = NavPanel.from_page_obj(browser)
    companies_page = nav_bar.goto_companies_page()
    update_company_address(
        companies_page=companies_page, address=DEFAULT_COMPANY_ADDRESS
    )
    logger.info(f"Адрес по умолчанию {DEFAULT_COMPANY_ADDRESS} установлен - OK!")
    companies_page.close_alerts()

    logger.info("Стартует очистка страницы сценариев")
    scenario_page = nav_bar.goto_scenario_page()
    scenario_page.clear_extra_items()
    scenario_page.close_alerts()
    logger.info("Закончена очистка страницы сценариев")

    logger.info("Закончен возврат сервера к первоначальной установке")
