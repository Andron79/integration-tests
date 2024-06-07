import logging

import yarl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from common import settings
from common.settings import download_default_directory
from shura.pages.login_page import LoginPage

from shura.pages.summary_page import SummaryPage
from shura.panels.nav import NavPanel

logger = logging.getLogger(__name__)


class WebDriver:
    def __init__(
        self,
        base_url: yarl.URL = settings.GMSERVER_ADDRESS,
        headless: bool = True,
        implicitly_wait: int = 10,
    ):
        """
        headless = True - Браузер не запускается
        headless = False - Браузер запускается
        """
        chrome_service = Service()
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option(
            "prefs", {"download.default_directory": str(download_default_directory)}
        )
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--ignore-certificate-errors")
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.driver.delete_all_cookies()
        self.driver.implicitly_wait(implicitly_wait)
        self.base_url = base_url

    def get(self, url: str = ""):
        return self.driver.get(f"{self.base_url / url.lstrip('/')}")

    def destroy(self):
        self.driver.quit()

    def goto_login_page(self) -> LoginPage:
        self.get()
        return LoginPage(self.driver)

    def login_in_server(
        self, login: str = "superadmin", password: str = "superadmin"
    ) -> SummaryPage:
        login_page = self.goto_login_page()
        login_page.login_field().send_keys(login)
        login_page.password_field().send_keys(password)
        login_page.login_btn().click()
        return SummaryPage(self.driver)

    def logout(self):
        NavPanel.from_page_obj(self).logout_link().click()
        NavPanel.from_page_obj(self).logout_confirm().click()
