from abc import ABC
from typing import TypeVar, Type, Callable, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

T = TypeVar("T", bound="Panel")
Locator = Tuple[str, str]


class Panel(ABC):
    ID = ""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    @classmethod
    def from_page_obj(cls: Type[T], page_obj) -> T:
        return cls(page_obj.driver)

    def element(
        self,
        name: str,
        predicate: Callable[[Locator], None] = EC.element_to_be_clickable,
        by: str = By.ID,
        message: str = None,
    ) -> WebElement:
        return WebDriverWait(self.driver, 10).until(
            predicate((by, f"{self.ID}__{name}")), message=message or name
        )
