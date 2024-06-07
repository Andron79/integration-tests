from shura.pages.tasks_page import TasksPage, TaskPanel
from shura.panels.nav import NavPanel


def create_task(
    task_page: TasksPage, downloaded_file, task_name: str, command_name: str
):
    """Создание Задания.

    :param task_page: Страница Задания
    :param downloaded_file: Фикстура для загрузки файла
    :param task_name: Название Задания
    :param command_name: Имя команды для задания
    :return:
    """
    task_page.combo_btn_add().click()
    task_panel = TaskPanel.from_page_obj(task_page)
    task_panel.task_name_field(task_name)
    task_panel.task_select_command_btn().click()
    task_panel.task_select_command_item_list(command_name).click()
    task_panel.load_file(downloaded_file)
    task_panel.load_btn().click()
    task_page.close_alerts()


def update_task(task_page: TasksPage, task_name: str, new_task_name: str):
    """Редактирование задания.

    :param task_page: Страница Задания
    :param task_name: Название Задания
    :param new_task_name: Отредактированное название Задания
    :return:
    """
    task_page = NavPanel.from_page_obj(task_page).goto_tasks_page()
    task_page.select_item(task_name).click()
    task_panel = TaskPanel.from_page_obj(task_page)
    task_panel.task_name_field_value(task_name)
    task_panel.task_name_field(new_task_name)
    task_panel.load_btn().click()


def delete_task(task_page: TasksPage, new_task_name: str):
    task_page = NavPanel.from_page_obj(task_page).goto_tasks_page()
    task_page.select_checkbox(new_task_name).click()
    task_page.combo_btn_del().click()
    task_page.popup_confirm()
    task_page.close_alerts()


def create_task_for_predefined_command(
    task_page: TasksPage, task_name: str, command_name: str
):
    """Создание Задания для предустановленной команды.

    :param task_page: Страница Задания
    :param task_name: Название Задания
    :param command_name: Имя команды для задания
    :return:
    """
    task_page.combo_btn_add().click()
    task_panel = TaskPanel.from_page_obj(task_page)
    task_panel.task_name_field(task_name)
    task_panel.task_select_command_btn().click()
    task_panel.task_select_command_item_list(command_name).click()
    task_panel.load_btn().click()
    task_page.close_alerts()
    task_panel.save_and_exit_btn().click()
    task_page.close_alerts()


def filtering_tasks(task_page: TasksPage, value: str):
    task_page.filter_field().send_keys(value)
    task_page.filter_button().click()


def reset_filter(task_page: TasksPage):
    task_page.reset_button().click()


def search_tasks(task_page: TasksPage, value: str):
    task_page.search_field().send_keys(value)


def clear_search_field(task_page: TasksPage):
    task_page.clear_search_field().click()
