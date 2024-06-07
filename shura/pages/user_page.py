import logging
import time
from typing import Generator, Any, Iterable
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.service_utils import overwrite_input
from shura.pages.base import InternalPage, ItemsTablePage
from shura.panels.base import Locator
from shura.panels.object import ObjectPanel
from shura.test_data.constants import PREDEFINED_USERS

logger = logging.getLogger(__name__)


class UserPage(ItemsTablePage, InternalPage):
    PREDEFINED_ITEMS = PREDEFINED_USERS

    def user_record(self, item):
        """
        :param item:
        :return Запись на станице списка пользователей для клика на пользователя username:
        """
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"tr[data-username='{item}']"))
        )

    def select_checkbox(self, item: str):
        """
        :param item: username пользователя
        :return Чекбокс для клика пользователя username:
        """
        return self.user_record(item).find_element(
            By.CSS_SELECTOR, "span.checkbox-indicator"
        )

    def users(
        self, ignore_users_list: Iterable[str] = None
    ) -> Generator[Any, Any, None]:
        """
        :param ignore_users_list:
        :return Генератор со всеми пользователями на странице, исключая тех, кто в списке ignore_users_list:
        """
        if ignore_users_list is None:
            ignore_users_list = []
        all_users = self.driver.find_elements(By.CLASS_NAME, "Table__icon-wrapper")
        return (user.text for user in all_users if user.text not in ignore_users_list)

    def list_table_items(self) -> Generator[str, None, None]:
        """
        Создает генератор с username всех пользователей, которые найдет на активной странице
        :return: генератор с username всех найденных пользователей:
        """
        all_users = self.driver.find_elements(By.CLASS_NAME, "Table__icon-wrapper")
        for user in all_users:
            yield user.text

    def ad_users(self) -> Generator:
        """
        :return Генератор с пользователями AD:
        """
        return (ad_user for ad_user in self.users() if ad_user.startswith("ad_"))


class UserPanel(ObjectPanel):
    ID = "EmployeeCreate__"
    CSS_SELECTOR_LOCATOR: Locator = ".App-Main"

    def username_field(self) -> WebElement:
        return self.element_by_id("username")

    def password_field(self) -> WebElement:
        return self.element_by_id("password")

    def password_confirmation_field(self) -> WebElement:
        return self.element_by_id("passwordConfirmation")

    def fullname_field(self) -> WebElement:
        return self.element_by_id("title")

    def user_role(self) -> WebElement:
        return self.element_by_id("roles")

    def select_user_role(self, role: str = None) -> None:
        self.user_role().click()
        return self.driver.find_element(By.ID, f"select-option__{role}").click()

    def get_user_profile_data(self, data: list) -> dict:
        """Чтение данных профиля юзера."""
        user_profile = {}
        user_profile.update(
            {
                key: self.driver.find_element(By.ID, f"{self.ID}__{key}").get_attribute(
                    "value"
                )
                for key in data
            }
        )
        return user_profile

    def non_empty_mapping_fields(self, data: list) -> list:
        mapping_fields = self.get_user_profile_data(data=data)
        return [item for item in mapping_fields.values() if item]

    def user_avatar(self) -> bool:
        """Проверка на наличие аватара юзера."""
        return bool(
            self.root.find_element(
                By.CSS_SELECTOR,
                "div[class^='EmployeeProfile_avatarWrapper'] img[src^='data:']",
            )
        )

    def create_btn(self):
        return self.root.find_element(By.CLASS_NAME, "Button.primary.medium")

    def collapse_first_section(self):
        """Закрывает первый блок профиля юзера."""
        return self.driver.find_element(
            By.CSS_SELECTOR, "div[class^='EmployeeEditProfile_accordionHeader']"
        ).click()

    def expand_all(self):
        """Раскрывает вск блоки профиля юзера."""
        return (
            WebDriverWait(self.driver, 5)
            .until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "EmployeeEditProfile_expandButton__CRose")
                )
            )
            .click()
        )

    def fill_panel_with_user_data(
        self, data: dict, start_delay: float = 0.0, input_delay: float = 0.0
    ):
        for field_name, value in data.items():
            field = self.driver.find_element(By.ID, f"{self.ID}__{field_name}")
            time.sleep(start_delay)
            overwrite_input(field, value, delay=input_delay)

    def save_changes(self):
        return self.root.find_element(By.CLASS_NAME, "Button.primary.medium")

    def back_btn(self):
        return self.driver.find_element(By.ID, "NavigationLink__employees")
