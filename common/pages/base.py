from abc import ABC


class PageBase(ABC):
    def __init__(self, driver):
        self.driver = driver

    def refresh(self):
        return self.driver.refresh()
