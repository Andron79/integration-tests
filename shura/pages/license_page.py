from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from shura.pages.base import InternalPage


class LicensePage(InternalPage):
    def license_dropzone(self):
        return self.driver.find_element(By.ID, "LicenseUpload__input-file")

    def choose_license_file(self, file):
        self.license_dropzone().send_keys(file)

    def upload_btn(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "LicenseUpload__upload-btn"))
        )

    def is_expired(self) -> bool:
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "ExpiredDateCell__icon")
                )
            )
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def is_uploaded(self) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "Alert--success"))
            )

            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def is_overflown(self) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".TdCell__progress-bar.overflow")
                )
            )
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def upload_license(self, filepath: str):
        self.choose_license_file(filepath)
        self.upload_btn().click()
