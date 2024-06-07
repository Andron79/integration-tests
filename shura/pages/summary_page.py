from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from shura.pages.base import InternalPage


class SummaryPage(InternalPage):
    def device_status(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "h2.Block__h2.link")
