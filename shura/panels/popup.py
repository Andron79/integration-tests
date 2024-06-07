from selenium.webdriver.remote.webelement import WebElement

from shura.panels.base import Panel


class Popup(Panel):
    ID = "Popup"

    def confirm(self) -> WebElement:
        return self.element("confirm")

    def cancel(self) -> WebElement:
        return self.element("cancel")
