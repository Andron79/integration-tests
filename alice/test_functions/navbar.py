import logging

from alice.page_objects.main_page import MainPage
from alice.page_objects.nav_bar import NavigationRightSide

logger = logging.getLogger(__name__)


def switch_theme(main_page: MainPage) -> bool:
    navbar = NavigationRightSide.from_page_obj(main_page)
    navbar.theme_switcher().click()
    return main_page.get_current_theme()
