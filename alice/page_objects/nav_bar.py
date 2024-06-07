from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class NavBar(ABC):
    ID = "Navigation"
    CLASS_NAME = "Navigation"

    def __init__(self, driver: WebDriver):
        self.driver = driver.find_element(By.CLASS_NAME, self.CLASS_NAME)

    @classmethod
    def from_page_obj(cls, page_obj):
        return cls(page_obj.driver)


class NavigationRightSide(NavBar):
    def theme_switcher(self) -> WebElement:
        """Переключатель системной темы.

        :return Элемент - переключатель темы:
        """
        return self.driver.find_element(By.CLASS_NAME, "ThemeSwitcher")

    def language_switcher(self) -> WebElement:
        """Переключатель языка.

        :return:
        """
        pass

    def get_username(self) -> str:
        """Получение имени авторизованного пользователя.

        :return Имя пользователя:
        """
        return self.driver.find_element(By.CLASS_NAME, "Navigation__dropdown-btn").text

    def user_profile(self) -> WebElement:
        """Профиль пользователя.

        :return:
        """
        pass


class NavigationMenu(NavBar):
    ...
