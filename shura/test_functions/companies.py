from selenium.common import StaleElementReferenceException
from tenacity import Retrying, stop_after_attempt, retry_if_exception_type, wait_fixed

from shura.pages.companies_page import CompaniesPage, CompaniesPanel
from common.service_utils import overwrite_input


def update_company_address(companies_page: CompaniesPage, address: str):
    for attempt in Retrying(
        retry=retry_if_exception_type(StaleElementReferenceException),
        stop=stop_after_attempt(5),
        wait=wait_fixed(1),
        reraise=True,
    ):
        with attempt:
            companies_page.close_alerts()
            companies_page.select_item_by_index(0).click()

    companies_panel = CompaniesPanel.from_page_obj(companies_page)

    overwrite_input(input_field=companies_panel.address_field(), value=address)
    companies_panel.save_changes_and_exit_btn().click()
