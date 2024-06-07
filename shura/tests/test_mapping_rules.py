import logging
from shura.test_data.constants import TEST_DATA, TEST_PROFILE_TEMPLATE, UPDATE_TEST_DATA

from shura.test_functions.mapping_rules import (
    create_mapping_rules_group,
    update_mapping_rules_group,
    delete_mapping_rules,
    create_mapping_rules_attribute,
    update_mapping_rules_attribute,
    create_mapping_rules_default,
    update_mapping_rules_default,
)

logger = logging.getLogger(__name__)


# @pytest.mark.skip(reason="Чинить")
def test_mapping_rules_crud(mapping_rules_page):
    #  Тест создания Правила сопоставления шаблонов с типом Группа
    create_mapping_rules_group(
        mapping_rules_page=mapping_rules_page,
        value=TEST_DATA["value"],
        descriptions=TEST_DATA["description"],
    )

    mapping_rules_group_exist = mapping_rules_page.get_mapping_rules_by_template(
        TEST_PROFILE_TEMPLATE["name"]
    )
    assert (
        mapping_rules_group_exist
    ), "Правила сопоставления шаблонов с типом Группа не создано!"

    logger.info("Правила сопоставления шаблонов с типом Группа создано - OK!")

    #  Тест на изменение Правила сопоставления шаблонов с типом Группа
    update_mapping_rules_group(
        mapping_rules_page=mapping_rules_page,
        update_value=UPDATE_TEST_DATA["value"],
        update_descriptions=UPDATE_TEST_DATA["description"],
    )

    mapping_rules_group_updated = mapping_rules_page.get_mapping_rules_by_description(
        UPDATE_TEST_DATA["description"]
    )

    assert (
        mapping_rules_group_updated
    ), "Правило сопоставления шаблонов с типом Группа не изменено!"
    logger.info("Правило сопоставления шаблонов с типом Группа изменено - OK!")

    #  Тест удаление всех сопоставлений
    delete_mapping_rules(
        mapping_rules_page=mapping_rules_page,
    )

    mapping_rules_group_exist = mapping_rules_page.get_mapping_rules_by_template(
        TEST_PROFILE_TEMPLATE["name"]
    )

    assert (
        mapping_rules_group_exist is False
    ), "Правило сопоставления шаблонов типом группа не удалено!"
    logger.info("Правило сопоставления шаблонов с типом группа удалено - OK!")

    create_mapping_rules_attribute(
        mapping_rules_page=mapping_rules_page,
        field=TEST_DATA["field"],
        value=TEST_DATA["value"],
        description=TEST_DATA["description"],
    )

    mapping_rules_attribute_exist = mapping_rules_page.get_mapping_rules_by_template(
        TEST_PROFILE_TEMPLATE["name"]
    )

    assert (
        mapping_rules_attribute_exist
    ), "Правила сопоставления шаблонов с типом атрибуты не создано!"
    logger.info("Правила сопоставления шаблонов с типом атрибуты создано - OK!")

    update_mapping_rules_attribute(
        mapping_rules_page=mapping_rules_page,
        update_field=UPDATE_TEST_DATA["field"],
        update_value=UPDATE_TEST_DATA["value"],
        update_description=UPDATE_TEST_DATA["description"],
    )

    mapping_rules_attribute_updated = (
        mapping_rules_page.get_mapping_rules_by_description(
            UPDATE_TEST_DATA["description"]
        )
    )

    assert (
        mapping_rules_attribute_updated
    ), "Правила сопоставления шаблонов с типом атрибуты не изменено!"
    logger.info("Правила сопоставления шаблонов с типом атрибуты изменено - OK!")

    delete_mapping_rules(
        mapping_rules_page=mapping_rules_page,
    )

    mapping_rules_attribute_exist = mapping_rules_page.get_mapping_rules_by_template(
        TEST_PROFILE_TEMPLATE["name"]
    )

    assert (
        mapping_rules_attribute_exist is False
    ), "Правила сопоставления шаблонов с типом атрибуты не удалено!"
    logger.info("Правила сопоставления шаблонов с типом атрибуты удалено - OK!")

    create_mapping_rules_default(
        mapping_rules_page=mapping_rules_page, descriptions=TEST_DATA["description"]
    )

    mapping_rules_default = mapping_rules_page.get_mapping_rules_by_template(
        TEST_PROFILE_TEMPLATE["name"]
    )

    assert (
        mapping_rules_default
    ), "Правило сопоставления шаблонов с типом по умолчанию не создано!"
    logger.info("Правила сопоставления шаблонов с типом по умолчанию создано - OK!")

    update_mapping_rules_default(
        mapping_rules_page=mapping_rules_page,
        descriptions=UPDATE_TEST_DATA["description"],
    )

    mapping_rules_default_updated = mapping_rules_page.get_mapping_rules_by_description(
        UPDATE_TEST_DATA["description"]
    )

    assert (
        mapping_rules_default_updated
    ), "Правило сопоставления шаблонов с типом по умолчанию не изменено!"
    logger.info("Правила сопоставления шаблонов с типом по умолчанию изменено - OK!")

    delete_mapping_rules(
        mapping_rules_page=mapping_rules_page,
    )

    mapping_rules_attribute_exist = mapping_rules_page.get_mapping_rules_by_template(
        TEST_PROFILE_TEMPLATE["name"]
    )

    assert (
        mapping_rules_attribute_exist is False
    ), "Правила сопоставления шаблонов с типом по умолчанию не удалено!"
    logger.info("Правила сопоставления шаблонов с типом по умолчанию удалено - OK!")
