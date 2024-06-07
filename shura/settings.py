# Настройки для автоматической очистки сервера перед прогоном тестов
import os

from common.settings import os_get_boolean

# Переменная для запуска/отключения очистки сервера
CLEAR_TEST_DATA = os_get_boolean("CLEAR_TEST_DATA", False)

# Время ожидания получения настроек синхронизации от сервера
SYNC_SETTINGS_RESPONSE_DELAY = 1.0
# Таймаут, чтобы фильтр успел сохраниться на сервере
SYNC_START_DELAY = float(os.getenv("SYNC_START_DELAY", 10.0))
SYNC_FINISH_CHECK_INTERVAL = 10.0
SYNC_FINISH_CHECK_RETRIES = 5.0

# Таймаут для сохранения Определений шаблонов и Правил сопоставления на сервере
SAVE_PANEL_DELAY = float(os.getenv("SAVE_PANEL_DELAY", 0.5))

# Таймаут для получения списка устройств подключенных к серверу
SYNC_RESPONSE_DEVICES_DELAY = float(os.getenv("SYNC_RESPONSE_DEVICES_DELAY", 0.2))

# Таймаут для выбора чекбоксов списка ролей в панели команд
SELECT_CHECKBOX_ROLES_DELAY = float(os.getenv("SELECT_CHECKBOX_ROLES_DELAY", 0.2))

# Таймаут для получения данный профиля пользователя
SYNC_RESPONSE_USER_PROFILE_DELAY = float(
    os.getenv("SYNC_RESPONSE_USER_PROFILE_DELAY", 0.2)
)

# Таймаут для валидации полей AD
TIMEOUT_VALIDATIONS = float(os.getenv("TIMEOUT_VALIDATIONS", 2))

# Время ожидания получения пользователей из LDAPS
SYNC_LDAPS_USERS_DELAY = 2

# Таймаут для получения результатов поиски и фильтрации заданий
TIMEOUT_TASKS_SEARCH_FILTERING = float(os.getenv("TIMEOUT_TASKS_SEARCH_FILTERING", 0.5))
