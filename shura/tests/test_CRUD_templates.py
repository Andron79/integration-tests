import logging

from common.service_utils import compare_data
from shura.pages.templates_page import TemplateDefinitionPanel
from shura.test_data.constants import (
    TEST_PROFILE_TEMPLATE,
    TEST_PROFILE_TEMPLATE_UPDATE,
)
from shura.test_functions.templates import (
    create_template,
    delete_template,
    update_template,
    get_template_data,
)

logger = logging.getLogger(__name__)


def test_template_crud(templates_page):
    create_template(
        template_page=templates_page, profile_template=TEST_PROFILE_TEMPLATE
    )

    assert templates_page.template_present(
        TEST_PROFILE_TEMPLATE["name"]
    ), "Шаблон не создан!"
    logger.info("Шаблон создан - OK!")

    update_template(
        template_page=templates_page,
        profile_template=TEST_PROFILE_TEMPLATE,
        update_profile_template=TEST_PROFILE_TEMPLATE_UPDATE,
    )

    template_profile = get_template_data(
        template_page=templates_page,
        update_profile_template=TEST_PROFILE_TEMPLATE_UPDATE,
    )

    diff = compare_data(
        local=TEST_PROFILE_TEMPLATE_UPDATE,
        remote=template_profile,
        prefix=TemplateDefinitionPanel.ID,
    )
    assert (
        not diff
    ), f"Поля шаблона различаются: {', '.join(f'{k}: {v[0]} -> {v[1]}' for k, v in diff.items())}"

    logger.info("Шаблон успешно изменен - OK!")

    delete_template(
        template_page=templates_page,
        profile_template_title=TEST_PROFILE_TEMPLATE_UPDATE["title"],
    )

    assert templates_page.template_absent(
        TEST_PROFILE_TEMPLATE_UPDATE["name"]
    ), "Шаблон не удален!"
    logger.info("Шаблон удален - OK!")
