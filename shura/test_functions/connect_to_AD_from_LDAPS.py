from __future__ import annotations

import logging

from shura.pages.settings_page import SettingsPage, AdSynchronization

logger = logging.getLogger(__name__)


def save_sync_settings(page: SettingsPage, data: dict) -> None:
    ad_panel = AdSynchronization.from_page_obj(page)
    ad_panel.save_sync_settings(data)


def connect_to_ad_from_ldaps(page: SettingsPage, data: dict) -> None:
    save_sync_settings(page, data=data)


def get_authorized_user(page: SettingsPage) -> str | None:
    return page.get_authorized_username()
