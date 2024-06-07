import logging
import pytest

from alice import settings
from alice.page_objects.main_page import MainPage

logger = logging.getLogger(__name__)


@pytest.fixture()
def main_page(driver):
    driver.get(f"{settings.LOGIN_PATH}{settings.LOGIN_TOKEN}")
    yield MainPage(driver.driver)
