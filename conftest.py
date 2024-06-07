import logging
import pytest
from common import settings
from common.webdriver import WebDriver

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def driver() -> WebDriver:
    driver = WebDriver(
        base_url=settings.GMSERVER_ADDRESS,
        implicitly_wait=1,
        headless=settings.HEADLESS,
    )
    yield driver
    driver.destroy()
