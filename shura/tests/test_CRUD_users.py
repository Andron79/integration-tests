import logging

from common.service_utils import compare_data
from shura.test_data.constants import TEST_USER_PROFILE, TEST_USER_PROFILE_UPDATE
from shura.test_functions.users import (
    create_user,
    delete_user,
    update_user,
    get_new_user_profile,
)

logger = logging.getLogger(__name__)


def test_user_crud(user_page):
    if not user_page.list_item_exists(TEST_USER_PROFILE["title"]):
        create_user(
            user_page=user_page,
            username=TEST_USER_PROFILE["username"],
            password=TEST_USER_PROFILE["password"],
            title=TEST_USER_PROFILE["title"],
        )

        assert user_page.list_item_exists(
            TEST_USER_PROFILE["title"]
        ), "Пользователь не создан!"
        logger.info("Пользователь создан - OK!")

    update_user(
        user_page=user_page,
        username=TEST_USER_PROFILE["username"],
        user_profile_update=TEST_USER_PROFILE_UPDATE,
        title=TEST_USER_PROFILE["title"],
    )

    new_user_profile = get_new_user_profile(
        user_page=user_page,
        username=TEST_USER_PROFILE["username"],
        title=TEST_USER_PROFILE["title"],
    )

    diff = compare_data(local=TEST_USER_PROFILE_UPDATE, remote=new_user_profile)
    assert (
        not diff
    ), f"Поля профиля различаются: {', '.join(f'{k}: {v[0]} -> {v[1]}' for k, v in diff.items())}"

    logger.info("Профиль пользователя изменен  - OK!")

    delete_user(
        user_page=user_page,
        username=TEST_USER_PROFILE["username"],
        title=TEST_USER_PROFILE["title"],
    )

    assert not user_page.list_item_exists(
        TEST_USER_PROFILE["username"]
    ), "Пользователь не удален!"
    logger.info("Пользователь удален  - OK!")
