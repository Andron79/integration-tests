from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.pages.base import PageBase


class MainPage(PageBase):
    def get_current_theme(self) -> bool:
        """Получение текущей системной темы.

        :return True - если текущая системная тема светлая, False - если темная:
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Main.light-theme"))
            )
        except TimeoutException:
            return False
        return True
