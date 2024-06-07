import os
from pathlib import Path

import yarl


def os_get_boolean(name: str, default: bool = False) -> bool:
    return (
        value.lower() == "true"
        if isinstance(value := os.getenv(name), str)
        else default
    )


# Папка для загрузки файлов драйвера по умолчанию
download_default_directory = Path.home() / "tmp"

# Настройки запуска тестов

# По умолчанию используется chromedriver из окружения
HEADLESS = os_get_boolean("TEST_WEBDRIVER_HEADLESS", True)
GMSERVER_ADDRESS = yarl.URL(
    os.getenv("GMSERVER_ADDRESS", "http://autotest.ta.gm.corp/")
)
