import logging
from shura.pages.companies_page import CompaniesPanel
from shura.test_data.constants import (
    CORRECT_ADDRESSES_LIST,
    INCORRECT_ADDRESSES_LIST,
)
from shura.test_functions.companies import update_company_address

logger = logging.getLogger(__name__)


def test_discovery_address(companies_page):
    for company_address in CORRECT_ADDRESSES_LIST:
        update_company_address(companies_page=companies_page, address=company_address)

        assert not companies_page.red_alert(), "Адрес не сохранен - ERROR!"
        logger.info(f"{company_address} - Корректный адрес. Успешно сохранен - OK!")

    for company_address in INCORRECT_ADDRESSES_LIST:
        update_company_address(companies_page=companies_page, address=company_address)

        assert (
            companies_page.red_alert()
        ), f"Адрес {company_address} - не корректный, но был сохранен - ERROR!"
        companies_page.close_alerts()
        logger.info(f"{company_address} - Не корректный адрес. Не сохраняем - OK!")
        companies_panel = CompaniesPanel.from_page_obj(companies_page)
        companies_panel.close_panel_without_save().click()
        companies_page.popup_confirm()
