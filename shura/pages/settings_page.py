from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from shura.pages.base import InternalPage
from shura.panels.object import ObjectPanel
from shura.panels.popup import Popup


class SettingsPage(InternalPage):
    pass


class AdSynchronization(ObjectPanel):
    ID = "Sync"
    CSS_SELECTOR_LOCATOR = "div[class^=SyncForm_Sync-ad__]"

    def _toggle_sync(self, target_value: str):
        sync = self.driver.find_element(By.ID, f"{self.ID}__is_active")
        if str(sync.get_attribute("value")) != target_value:
            sync_label = self.driver.find_element(
                By.CSS_SELECTOR, "#Sync__is_active ~ .checkmark"
            )
            return sync_label.click()

    def sync_on(self):
        self._toggle_sync("true")

    def sync_off(self):
        self._toggle_sync("false")

    def apply_sync_settings(self):
        self.save_changes_btn().click()

    def clear_outdated_users(self):
        self.element("clear-outdated-users").click()
        popup = Popup.from_page_obj(self)
        popup.confirm().click()

    def accordion_filters(self):
        return WebDriverWait(self.root, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "accordion-button"))
        )

    def save_sync_settings(self, data: dict):
        self.sync_on()
        self.accordion_filters().click()
        self.fill_panel_with_data(data, start_delay=0.2, input_delay=0.1)
        self.apply_sync_settings()

    def clear_sync_settings(self):
        self.sync_off()
        self.apply_sync_settings()
        self.clear_outdated_users()

    def validation_error_count(self) -> int:
        """
        Метод возвращает кол-во элементов не прошедших валидацию
        """
        return len(self.driver.find_elements(By.CLASS_NAME, "error-validate"))

    def validation_error_massages(self) -> set[str]:
        """
        Метод возвращает множество сообщений элементов на странице не прошедших валидацию
        """
        return set(
            error.text
            for error in self.driver.find_elements(By.CLASS_NAME, "error-validate")
            if error.text
        )


class SyncTemplatesPopup(Popup):
    def rewrite(self) -> WebElement:
        return self.driver.find_element(By.ID, "rewrite")

    def write_empty(self) -> WebElement:
        return self.driver.find_element(By.ID, "writeEmpty")
