# Реализовать автотест проверки привилегий ролей
# 1) Зайти superadmin'ом, проверить доступность всех ожидаемых ссылок в панели навигации
# 2) Создать роль с ReadOnly привилегиями
# 3) Создать тестового пользователя и применить к нему роль с ReadOnly привилегиями
# 4) Залогиниться тестовым пользователем, проверить применение ReadOnly режима для всех страниц (см. комментарий)
# 5) Удалить тестового пользователя и тестовую роль

# Комментарий:
# Вариант "Только Чтение" проверяем так:
# Сводка: наличие плашки "Статус устройств"
# Устройства: кнопка "МЕНЮ" есть и загреена
# Конкретное устройство: кнопка "СОХРАНИТЬ ИЗМЕНЕНИЯ" есть и загреена
# Группы устройств: кнопка "МЕНЮ" есть и загреена
# Конкретная Группа устройств: правая кнопка "МЕНЮ" есть и загреена
# Пользователи: кнопка "МЕНЮ" есть и загреена
# Конкретный пользователь: кнопка "СОХРАНИТЬ ИЗМЕНЕНИЯ" есть и загреена
# Шаблоны: кнопка "МЕНЮ" есть и загреена
# Конкретный шаблон: кнопка "СОХРАНИТЬ ИЗМЕНЕНИЯ" есть и загреена
# Правила сопоставлений: кнопка "МЕНЮ" есть и загреена
# Конкретное правило сопоставлений: кнопка "СОХРАНИТЬ ИЗМЕНЕНИЯ" есть и загреена
# Роли: кнопка "МЕНЮ" есть и загреена
# Конкретная роль: кнопка "СОХРАНИТЬ" есть и загреена
# Обновления: кнопка "МЕНЮ" есть и загреена
# Конкретное обновление: кнопка "СОХРАНИТЬ ИЗМЕНЕНИЯ" есть и загреена
# Приложения: кнопка "МЕНЮ" есть и загреена
# Конкретное приложение: кнопка "СОХРАНИТЬ ИЗМЕНЕНИЯ" есть и загреена
# Задания: кнопка "МЕНЮ" есть и загреена
# Конкретное задание: кнопка "СОХРАНИТЬ ИЗМЕНЕНИЯ" есть и загреена
# Сценарии: кнопка "МЕНЮ" есть и загреена
# Конкретный сценарий: кнопка "СОХРАНИТЬ" есть и загреена
# Команды: кнопка "МЕНЮ" есть и загреена
# Конкретная команда: кнопка "СОХРАНИТЬ ИЗМЕНЕНИЯ" есть и загреена
# Организации: зайти в организацию, кнопка "СОХРАНИТЬ ИЗМЕНЕНИЯ" есть и загреена
# Журнал - GM-Box: Список событий непустой
# Журнал - GM-Server: Список событий непустой
# Журнал - Задания: Список событий непустой
# Настройки - Синхронизация: проверить наличие и загрееность чекбокса Включить синхронизацию
# Настройки - GM Версии: список версий непустой
# Настройки - Лицензия: наличие слов "Тип лицензии:" и отсутствие кнопки ЗАГРУЗИТЬ
# Диагностика: кнопка "Добавить шаг диагностики" есть и загреена

import logging
import time

import pytest

from shura.pages.roles_page import RolesPanel
from shura.pages.user_page import UserPanel
from shura.panels.nav import NavPanel

logger = logging.getLogger(__name__)


def test_roles_superadmin_mode(readonly_role, browser):
    superadmin_available_nav_items = readonly_role.navigation_section_items
    assert (
        len(superadmin_available_nav_items) == 16  # Плюс пункт "выход/logout"
    ), f"Присутствует {len(superadmin_available_nav_items)} != 16 пунктов меню из 16 - ERROR"
    logger.info(
        f"Присутствует {len(superadmin_available_nav_items)} = 16 пунктов меню из 16 - OK! "
    )


def test_roles_readonly_mode_summary(summary_page):
    assert (
        summary_page.device_status().is_displayed()
    ), "Нет плашки device_status - ERROR"
    logger.info("Плашка device_status- OK!")


def test_roles_readonly_mode_devices(device_page):
    assert (
        not device_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'devices_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'devices_page' не активна - OK!")


def test_roles_readonly_mode_devices_groups(device_group_page):
    assert (
        not device_group_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'devices_groups_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'devices_groups_page' не активна - OK!")


def test_roles_readonly_mode_users(user_page):
    assert (
        not user_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'user_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'user_page' не активна - OK!")

    user_page.select_item_by_index(0).click()
    user_panel = UserPanel.from_page_obj(user_page)

    assert (
        not user_panel.save_changes().is_enabled()
    ), "Кнопка 'save_changes' на панели 'user_panel' активна - ERROR!"
    logger.info("Кнопка 'save_changes' на панели 'user_panel' не активна - OK!")


def test_roles_readonly_mode_templates(templates_page):
    assert (
        not templates_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'templates_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'templates_page' не активна - OK!")


def test_roles_readonly_mode_updates(browser):
    updates_page = NavPanel.from_page_obj(browser).goto_updates_page()

    assert (
        not updates_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'updates_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'updates_page' не активна - OK!")


def test_roles_readonly_mode_applications(applications_page):
    assert (
        not applications_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'applications_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'applications_page' не активна - OK!")


def test_roles_readonly_mode_roles(browser):
    roles_page = NavPanel.from_page_obj(browser).goto_roles_page()
    assert (
        not roles_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'roles_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'roles_page' не активна - OK!")

    time.sleep(1)
    roles_page.select_item_by_index(0).click()
    roles_panel = RolesPanel.from_page_obj(roles_page)
    time.sleep(10)

    assert (
        not roles_panel.role_btn_submit().is_enabled()
    ), "Кнопка 'save_changes' на панели 'roles_panel' активна - ERROR!"
    logger.info("Кнопка 'save_changes' на панели 'roles_panel' не активна - OK!")


def test_roles_readonly_mode_tasks(browser):
    task_page = NavPanel.from_page_obj(browser).goto_tasks_page()

    assert (
        not task_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'tasks_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'tasks_page' не активна - OK!")


def test_roles_readonly_mode_scenarios(scenario_page):
    assert (
        not scenario_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'scenarios_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'scenarios_page' не активна - OK!")


def test_roles_readonly_mode_commands(commands_page):
    assert (
        not commands_page.combo_button().is_enabled()
    ), "Кнопка 'Меню'  на странице 'commands_page' активна - ERROR!"
    logger.info("Кнопка 'Меню' на странице 'commands_page' не активна - OK!")


@pytest.mark.skip(reason="Дополнить тест согласно тестового сценария")
def test_roles_readonly_mode_companies(companies_page):
    ...


@pytest.mark.skip(reason="Дополнить тест согласно тестового сценария")
def test_roles_readonly_mode_settings(sync_page):
    ...


@pytest.mark.skip(reason="Дополнить тест согласно тестового сценария")
def test_roles_readonly_mode_diagnostics(diagnostics_page):
    ...


@pytest.mark.skip(reason="Дополнить тест согласно тестового сценария")
def test_roles_readonly_mode_journal(journal_page):
    ...
