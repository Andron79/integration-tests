import logging
from shura.pages.scenarios_page import ScenarioPanel
from shura.test_data.constants import (
    TEST_SCENARIO,
    UPDATE_TEST_SCENARIO,
    ScenarioSchedule,
    START_TIME,
    UPDATED_START_TIME,
    Day,
    DAY_IN_MONTH,
    FAKE_SCENARIO,
    SCENARIOS,
    FILTER_TEST,
    FILTER_FAKE,
)
from shura.test_functions.scenarios import (
    create_scenario_by_request,
    update_scenario_by_request,
    delete_scenario,
    create_scenario_by_trigger,
    update_scenario_by_trigger,
    create_scenario_by_scheduler,
    update_scenario_by_scheduler,
    start_scenario,
    input_scenario_filter_by_name,
)

logger = logging.getLogger(__name__)


def test_scenarios_by_request(scenario_page):
    create_scenario_by_request(scenario_page, title=TEST_SCENARIO)

    assert scenario_page.list_item_exists(
        TEST_SCENARIO
    ), f"Сценарий {TEST_SCENARIO} с режимом запуска по запросу не создан - ERROR!"
    logger.info(f"Сценарий {TEST_SCENARIO} с режимом запуска по запросу создан! - OK")

    start_scenario(scenario_page, title=TEST_SCENARIO)
    scenario_panel = ScenarioPanel.from_page_obj(scenario_page)

    assert (
        scenario_panel.scenario_in_complete_status()
    ), f"Сценарий {TEST_SCENARIO} с режимом запуска по запросу не запущен - ERROR!"
    logger.info(
        f"Сценарий {TEST_SCENARIO} с режимом запуска по запросу запушен и завершился успешно! - OK"
    )

    scenario_panel.back_btn().click()

    update_scenario_by_request(
        scenario_page, title=TEST_SCENARIO, new_title=UPDATE_TEST_SCENARIO
    )

    assert scenario_page.list_item_exists(
        UPDATE_TEST_SCENARIO
    ), f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по запросу не изменен - ERROR!"
    logger.info(
        f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по запросу изменен! - OK"
    )

    delete_scenario(scenario_page, title=UPDATE_TEST_SCENARIO)

    assert not scenario_page.list_item_exists(
        UPDATE_TEST_SCENARIO
    ), f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по запросу не удален - ERROR!"
    logger.info(
        f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по запросу удален! - OK"
    )


def test_scenarios_by_trigger(scenario_page):
    create_scenario_by_trigger(scenario_page, title=TEST_SCENARIO)

    assert scenario_page.list_item_exists(
        TEST_SCENARIO
    ), f"Сценарий {TEST_SCENARIO} с режимом запуска по событию не создан - ERROR!"
    logger.info(f"Сценарий {TEST_SCENARIO} с режимом запуска по событию создан! - OK")

    update_scenario_by_trigger(
        scenario_page, title=TEST_SCENARIO, new_title=UPDATE_TEST_SCENARIO
    )

    assert scenario_page.list_item_exists(
        UPDATE_TEST_SCENARIO
    ), f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по событию не изменен  - ERROR!"
    logger.info(
        f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по событию изменен! - OK"
    )

    delete_scenario(scenario_page, title=UPDATE_TEST_SCENARIO)

    assert not scenario_page.list_item_exists(
        TEST_SCENARIO
    ), f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по событию не удален - ERROR!"
    logger.info(
        f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по событию удален! - OK"
    )


def test_scenario_by_scheduler(scenario_page):
    for schedule in ScenarioSchedule:
        logger.info(f"Стартует тест с режимом запуска по расписанию {schedule.name}!")
        create_scenario_by_scheduler(
            scenario_page,
            title=TEST_SCENARIO,
            scheduler=schedule,
            start_time=START_TIME,
            day=Day.SATURDAY,
            day_in_month=DAY_IN_MONTH,
        )

        assert scenario_page.list_item_exists(
            TEST_SCENARIO
        ), f"Сценарий {TEST_SCENARIO} с режимом запуска по расписанию не создан - ERROR!"
        logger.info(
            f"Сценарий {TEST_SCENARIO} с режимом запуска по расписанию создан! - OK"
        )

        start_scenario(scenario_page, title=TEST_SCENARIO)
        scenario_panel = ScenarioPanel.from_page_obj(scenario_page)

        assert (
            scenario_panel.scenario_in_complete_status()
        ), f"Сценарий {TEST_SCENARIO} с режимом запуска по расписанию не запущен - ERROR!"
        logger.info(
            f"Сценарий {TEST_SCENARIO} с режимом запуска по расписанию запушен и завершился успешно! - OK"
        )

        scenario_panel.back_btn().click()

        update_scenario_by_scheduler(
            scenario_page,
            title=TEST_SCENARIO,
            new_title=UPDATE_TEST_SCENARIO,
            start_time=UPDATED_START_TIME,
        )

        assert scenario_page.list_item_exists(
            UPDATE_TEST_SCENARIO
        ), f"Сценарий {TEST_SCENARIO} с режимом запуска по расписанию не изменен - ERROR!"
        logger.info(
            f"Сценарий {TEST_SCENARIO} с режимом запуска по расписанию изменен! - OK"
        )

        delete_scenario(scenario_page, title=UPDATE_TEST_SCENARIO)

        assert not scenario_page.list_item_exists(
            TEST_SCENARIO
        ), f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по расписанию не удален - ERROR!"
        logger.info(
            f"Сценарий {UPDATE_TEST_SCENARIO} с режимом запуска по расписанию удален! - OK"
        )


def test_filter_scenarios(scenario_page):
    for scenario in SCENARIOS:
        create_scenario_by_request(scenario_page, title=scenario)

        assert scenario_page.list_item_exists(
            scenario
        ), f"Сценарий {scenario} для проверки фильтров не создан - ERROR!"
        logger.info(f"Сценарий {scenario} для проверки фильтров создан! - OK")

    input_scenario_filter_by_name(scenario_page=scenario_page, title=FILTER_TEST)

    assert scenario_page.list_item_exists(
        TEST_SCENARIO
    ), f"Применен фильтр {FILTER_TEST}: сценарий {TEST_SCENARIO} в списке не отображается - ERROR!"
    logger.info(
        f"Применен фильтр {FILTER_TEST}: сценарий {TEST_SCENARIO} в списке отображается - OK!"
    )

    assert scenario_page.list_item_exists(
        UPDATE_TEST_SCENARIO
    ), f"Применен фильтр {FILTER_TEST}: сценарий {UPDATE_TEST_SCENARIO} в списке не отображается - ERROR!"
    logger.info(
        f"Применен фильтр {FILTER_TEST}: {UPDATE_TEST_SCENARIO} ов списке отображается - OK!"
    )

    assert not scenario_page.list_item_exists(
        FAKE_SCENARIO
    ), f"Применен фильтр {FILTER_FAKE}: сценарий {FAKE_SCENARIO} в списке не отображается - ERROR!"
    logger.info(
        f"Применен фильтр {FILTER_FAKE}: {FAKE_SCENARIO} в списке отображается - OK!"
    )

    scenario_page.reset_table_filter_btn().click()

    input_scenario_filter_by_name(scenario_page=scenario_page, title=FILTER_FAKE)

    assert not scenario_page.list_item_exists(
        TEST_SCENARIO
    ), f"Применен фильтр {FILTER_TEST}: сценарий {TEST_SCENARIO} в списке не отображается - ERROR!"
    logger.info(
        f"Применен фильтр {FILTER_TEST}: сценарий {TEST_SCENARIO} в списке отображается - OK!"
    )

    assert not scenario_page.list_item_exists(
        UPDATE_TEST_SCENARIO
    ), f"Применен фильтр {FILTER_TEST}: сценарий {UPDATE_TEST_SCENARIO} в списке не отображается - ERROR!"
    logger.info(
        f"Применен фильтр {FILTER_TEST}: {UPDATE_TEST_SCENARIO} ов списке отображается - OK!"
    )

    assert scenario_page.list_item_exists(
        FAKE_SCENARIO
    ), f"Применен фильтр {FILTER_FAKE}: сценарий {FAKE_SCENARIO} в списке не отображается - ERROR!"
    logger.info(
        f"Применен фильтр {FILTER_FAKE}: {FAKE_SCENARIO} в списке отображается - OK!"
    )

    scenario_page.reset_table_filter_btn().click()

    for scenario in SCENARIOS:
        if scenario_page.list_item_exists(scenario):
            delete_scenario(scenario_page, title=scenario)
            logger.info(f"Окончательная очистка: сценарий {scenario} удален - OK!")
