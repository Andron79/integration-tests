import logging
import time

from shura.pages.base import InternalPage
from shura.pages.settings_page import AdSynchronization, SettingsPage

from shura.pages.user_page import UserPanel, UserPage
from shura.panels.nav import NavPanel
from shura.test_data.constants import (
    AD_FILTER,
    TEST_AD_DATA,
    FAKE_FILTER,
    ALL_USER_FIELDS_CHECKED,
    SELENIUM_TEST_USER_FILTER,
    SELENIUM_TEST_USERNAME,
    STANDARD_USER_FIELDS,
    ADMIN_USERNAME,
    NON_AD_USERS,
    TEST_USER_PROFILE_UPDATE,
)

from shura.settings import (
    SYNC_START_DELAY,
    SYNC_FINISH_CHECK_RETRIES,
    SYNC_FINISH_CHECK_INTERVAL,
)

logger = logging.getLogger(__name__)


def build_test_data(custom_data: dict) -> dict:
    return {**TEST_AD_DATA, **custom_data}


def wait_for_sync(page: InternalPage) -> UserPage:
    time.sleep(SYNC_START_DELAY)
    user_page = NavPanel.from_page_obj(page).goto_user_page()
    user_page.refresh()

    def user_finder():
        return list(user_page.users(NON_AD_USERS))

    user_page.wait_until_no_change(
        func=user_finder,
        comparator=lambda x, y: x is not None and len(x) == len(y),
        retries=SYNC_FINISH_CHECK_RETRIES,
        interval=SYNC_FINISH_CHECK_INTERVAL,
    )

    return user_page


def save_sync_settings(page: SettingsPage, data: dict):
    ad_panel = AdSynchronization.from_page_obj(page)
    ad_panel.save_sync_settings(data)


def test_ad_filter(sync_page):
    save_sync_settings(sync_page, data=build_test_data({"USER-filter": AD_FILTER}))

    user_page = wait_for_sync(sync_page)
    users = list(user_page.users(ignore_users_list=NON_AD_USERS))
    ad_users = list(user_page.ad_users())

    assert ad_users and ad_users == users


def test_fake_filter(sync_page):
    save_sync_settings(sync_page, data=build_test_data({"USER-filter": FAKE_FILTER}))
    user_page = wait_for_sync(sync_page)
    sync_page = NavPanel.from_page_obj(user_page).goto_settings_page()

    ad_panel = AdSynchronization.from_page_obj(sync_page)
    ad_panel.clear_outdated_users()

    user_page = wait_for_sync(sync_page)
    fake_users = list(user_page.users(ignore_users_list=NON_AD_USERS))

    assert not fake_users


def test_mapping_fields(sync_page):
    test_data = build_test_data(
        {"mapping": ALL_USER_FIELDS_CHECKED, "USER-filter": SELENIUM_TEST_USER_FILTER}
    )
    save_sync_settings(sync_page, data=test_data)

    user_page = wait_for_sync(sync_page)
    user_page.user_record(SELENIUM_TEST_USERNAME).click()
    user_panel = UserPanel.from_page_obj(user_page)
    user_panel.collapse_first_section()
    user_panel.expand_all()
    user_dict = user_panel.get_user_profile_data(TEST_USER_PROFILE_UPDATE)
    non_empty_mapping_fields = user_panel.non_empty_mapping_fields(
        TEST_USER_PROFILE_UPDATE
    )
    avatar = user_panel.user_avatar()

    assert avatar and len(user_dict) == len(non_empty_mapping_fields)


def test_clear_mapping_fields(sync_page):
    test_data = build_test_data(
        {"mapping": STANDARD_USER_FIELDS, "USER-filter": FAKE_FILTER}
    )
    save_sync_settings(sync_page, data=test_data)
    user_page = wait_for_sync(sync_page)
    sync_page = NavPanel.from_page_obj(user_page).goto_settings_page()

    ad_panel = AdSynchronization.from_page_obj(sync_page)
    ad_panel.clear_outdated_users()

    user_page = wait_for_sync(sync_page)
    user_page.user_record(ADMIN_USERNAME).click()
    user_panel = UserPanel.from_page_obj(user_page)
    user_panel.collapse_first_section()
    user_panel.expand_all()

    non_empty_mapping_fields = user_panel.non_empty_mapping_fields(
        TEST_USER_PROFILE_UPDATE
    )

    assert (
        len(non_empty_mapping_fields) == 1
    )  # команда из STANDARD_USER_FIELDS возвращает 1 текстовое поле title
