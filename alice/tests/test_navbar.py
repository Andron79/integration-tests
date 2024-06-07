import logging

import pytest

from alice.test_functions.navbar import switch_theme

logger = logging.getLogger(__name__)


@pytest.mark.skip(reason="Отложено")
def test_switch_theme(main_page):
    theme = main_page.get_current_theme()
    new_theme = switch_theme(main_page)

    assert theme != new_theme, "Системная тема не переключена"
    logger.info("Системная тема успешно переключена - OK!")
