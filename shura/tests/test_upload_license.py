import pytest

from shura.panels.nav import NavPanel
from shura.test_data.constants import expired_license, overflown_license, valid_license


@pytest.mark.parametrize("downloaded_file", [expired_license], indirect=True)
def test_add_expired_license(browser, downloaded_file):
    license_page = NavPanel.from_page_obj(browser).goto_license_page()
    license_page.choose_license_file(downloaded_file)
    license_page.upload_btn().click()

    assert license_page.is_uploaded()
    assert license_page.is_expired()


@pytest.mark.parametrize("downloaded_file", [overflown_license], indirect=True)
def test_add_overflown_license(browser, downloaded_file):
    license_page = NavPanel.from_page_obj(browser).goto_license_page()
    license_page.choose_license_file(downloaded_file)
    license_page.upload_btn().click()

    assert license_page.is_uploaded()
    assert license_page.is_overflown()


@pytest.mark.parametrize("downloaded_file", [valid_license], indirect=True)
def test_add_valid_license(browser, downloaded_file):
    license_page = NavPanel.from_page_obj(browser).goto_license_page()
    license_page.choose_license_file(downloaded_file)
    license_page.upload_btn().click()

    assert license_page.is_uploaded()
    assert not license_page.is_expired()
    assert not license_page.is_overflown()
