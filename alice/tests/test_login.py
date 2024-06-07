import logging

import pytest

from alice.page_objects.nav_bar import NavigationRightSide
from alice.settings import LOGIN_TOKEN

logger = logging.getLogger(__name__)


@pytest.mark.skip(reason="Для начала создать Пользователя под этот тест")
def test_login_from_gmserver(main_page):
    navbar = NavigationRightSide.from_page_obj(main_page)

    assert (
        navbar.get_username() == LOGIN_TOKEN
    ), "Пользователь не смог залогиниться по токену из GM Server"
    logger.info("Пользователь успешно залогинился по токену из GM Server - OK!")
