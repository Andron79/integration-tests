from __future__ import annotations

import logging
import time
from abc import ABC
from typing import Callable, Any, Iterable, Optional, Generator

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.pages.base import PageBase
from common.service_utils import overwrite_input
from shura.panels.popup import Popup

logger = logging.getLogger(__name__)


class InternalPage(PageBase, ABC):
    def popup_confirm(self):
        popup = Popup.from_page_obj(self)
        popup.confirm().click()

    def popup_cancel(self):
        popup = Popup.from_page_obj(self)
        popup.cancel().click()

    def close_alerts(self):
        """Принудительно закрывает предупреждения о завершении операции."""
        while True:
            try:
                WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".Alert .Alert__close")
                    )
                ).click()
            except TimeoutException:
                break

    def red_alert(self) -> Optional[WebElement]:
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "Alert--error"))
            )
        except TimeoutException:
            return None

    def wait_close_panel(self):
        return WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".Alert::after"))
        )

    def wait_until_no_change(
        self,
        func: Callable[[], Any],
        comparator: Callable[[Any, Any], bool] = lambda x, y: x == y,
        retries: int = 0,
        interval: float = 0.0,
    ) -> Any:
        attempt = 0
        prev, current = None, None
        while True:
            attempt += 1

            prev, current = current, func()
            if attempt > retries or comparator(prev, current):
                return current

            time.sleep(interval)
            self.refresh()

    def get_items_by_attribute_map(
        self, attribute_map: dict, element_tag: str = "*"
    ) -> list:
        attributes_selector = " and ".join(
            f"{k}='{v}'" for k, v in attribute_map.items()
        )
        selector = f"{element_tag}[{attributes_selector}]"
        return self.driver.find_elements_by_css_selector(selector)

    def element_is_absent(self, element: str):
        return WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, element))
        )

    def get_authorized_username(self) -> Any:
        """Возвращает имя авторизованного пользователя, если авторизоваться не
        удается, возвращает None."""
        try:
            return (
                WebDriverWait(self.driver, 3)
                .until(
                    EC.visibility_of_element_located(
                        (By.CLASS_NAME, "AppNavigation__username")
                    )
                )
                .text
            )
        except TimeoutException:
            return None

    @property
    def navigation_section_items(self) -> list[WebElement]:
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".NavigationLink"))
        )


class ComboButton(PageBase, ABC):
    def _open_combo_button(self):
        """Ищет ComboButton, и если кнопка закрыта, кликает на нее, чтобы
        открыть.

        :return WebElement: Открытая ComboButton
        """
        btn = self.combo_button()
        if btn.get_attribute("aria-expanded").lower() == "false":
            btn.click()

    def combo_button(self) -> WebElement:
        return self.driver.find_element(By.ID, "DropDownMenu")

    def combo_btn_add(self) -> WebElement:
        self._open_combo_button()
        return self.driver.find_element(By.ID, "DropDownMenu__add")

    def combo_btn_del(self) -> WebElement:
        self._open_combo_button()
        return self.driver.find_element(By.ID, "DropDownMenu__delete")


class FilterSection(PageBase, ABC):
    def filter_field(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, ".TableFilters__input")

    def filter_button(self) -> WebElement:
        return self.driver.find_element(By.ID, "TableFilters__btn-submit")

    def reset_button(self) -> WebElement:
        return self.driver.find_element(By.ID, "TableFilters__btn-reset")


class SearchSection(PageBase, ABC):
    def search_field(self):
        return self.driver.find_element(By.ID, "header__search-field")

    def clear_search_field(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, "clear_search_field")


class ItemsTablePage(InternalPage, ComboButton, FilterSection, SearchSection, ABC):
    PREDEFINED_ITEMS: Iterable[str] = tuple()

    def _select_table_item(self, item: str):
        """Метод для выделения объекта (checkbox)"""
        self.select_checkbox(item).click()

    def list_table_items(self) -> Generator[Any, Any, None]:
        """
        Создает генератор с названиями всех сущностей, которые найдет на активной странице
        :return: генератор с названиями всех найденных сущностей
        """
        return (
            item.text
            for item in self.driver.find_elements(
                By.CSS_SELECTOR, 'td[data-name="title"]'
            )
        )

    def delete_selected(self):
        """
        Удаление одного или нескольких отмеченных объектов
        :return:
        """
        self.combo_btn_del().click()
        self.popup_confirm()

    def clear_extra_items(self):
        """Метод для удаления всех объектов на странице, которые не входят в
        чистую установку сервера."""
        while extra_items := set(self.list_table_items()) - set(self.PREDEFINED_ITEMS):
            for item in extra_items:
                self._select_table_item(item)

            self.delete_selected()
            self.close_alerts()
            self.refresh()

    def select_checkbox(self, item: str) -> WebElement:
        """Метод для выделения чекбокса на станице.

        :param item: Название элемента.
        :return: Чекбокс
        """
        return self.driver.find_element(
            By.CSS_SELECTOR,
            f".checkbox-indicator.Table__checkbox-ghost.TableView__checkbox[data-title='{item}']",
        )

    def list_item_exists(self, item: str) -> bool:
        """Метод проверяет существование элемента на странице.

        :param item: Элемент
        :return: True - если есть элемент на странице иначе False
        """
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f".checkbox-col span[data-title='{item}']")
                )
            )
        except TimeoutException:
            return False
        return True

    def select_item(self, item: str) -> WebElement:
        """Метод для выделения элемента на странице.

        :param item: Название элемента.
        :return: Веб элемент
        """
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"tbody tr[data-title='{item}']")
            )
        )

    def select_item_by_index(self, index: int) -> WebElement:
        """Метод для выделения элемента на странице по индексу.

        :param index: Индекс элемента, начиная с 0.
        :return: Веб элемент
        """
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"tbody tr:nth-child({index + 1})")
            )
        )

    def set_filter(self, title) -> None:
        """Ввод данных в фильтр.

        :param title:
        :return:
        """
        input_field = self.driver.find_element(By.CLASS_NAME, "TableFilters__input")
        overwrite_input(input_field, title)

    def table_filter_btn(self) -> WebElement:
        """
        Кнопка запуска фильтрации
        :return: Кнопка фильтрации
        """
        return self.driver.find_element(By.ID, "TableFilters__btn-submit")

    def reset_table_filter_btn(self) -> WebElement:
        """
        Сброс значений фильтра
        :return: Кнопка сброса
        """
        return self.driver.find_element(By.ID, "TableFilters__btn-reset")

    def get_pagination_max(self) -> int:
        return int(
            self.driver.find_element(By.ID, "Pagination__input-page").get_attribute(
                "max"
            )
        )

    def get_current_pages(self) -> int:
        return int(
            self.driver.find_element(By.ID, "Pagination__input-page").get_attribute(
                "value"
            )
        )

    def delete_no_predefined_items(self):
        """Метод для удаления всех не предустановленных объектов тестирования
        на странице."""
        counter = 0
        pages = self.get_pagination_max() - self.get_current_pages()
        while extra_items := set(
            [
                elem.get_attribute("data-name")
                for elem in self.driver.find_elements(By.XPATH, "//*[@data-name]")
            ]
        ) - set(self.PREDEFINED_ITEMS):
            while pages >= 0:
                for item in extra_items:
                    if self.list_item_exists(item):
                        self._select_table_item(item)
                        counter += 1
                if counter:
                    self.delete_selected()
                    self.close_alerts()
                pages -= 1
                if pages:
                    self.driver.find_element(By.ID, "Pagination__arrow-next").click()
