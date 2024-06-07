import logging

from shura.panels.nav import NavPanel

logger = logging.getLogger(__name__)


def test_logout(driver):
    logout_link = NavPanel.from_page_obj(driver).logout_link()
    logout_link.click()
    confirm_logout = NavPanel.from_page_obj(driver).logout_confirm()
    confirm_logout.click()
    logger.info("Разлогин - OK!")
    driver.goto_login_page()
    driver.login_in_server()

    logger.info("Логин - OK!")
