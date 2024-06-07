from typing import Optional

from common.webdriver import WebDriver
from shura.panels.nav import NavPanel


def user_logout(driver: WebDriver) -> None:
    logout_link = NavPanel.from_page_obj(driver).logout_link()
    logout_link.click()
    confirm_logout = NavPanel.from_page_obj(driver).logout_confirm()
    confirm_logout.click()


def login_to_server(
    driver: WebDriver, login: Optional[str] = None, password: Optional[str] = None
) -> None:
    driver.login_in_server(login=login, password=password)
