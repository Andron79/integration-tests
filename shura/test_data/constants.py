import random
from enum import Enum
from pathlib import Path

import yaml

from common.settings import download_default_directory, GMSERVER_ADDRESS

# tests users
with open(Path(__file__).parent / "user_data.yaml") as f:
    test_user_data = yaml.safe_load(f)

TEST_USER_PROFILE = test_user_data["create"]
TEST_USER_PROFILE_UPDATE = test_user_data["update"]

#  tests command
COMMAND_NAME = "AAAA___TEST_COMMAND_DONE"
COMMAND_DATA = "(cmd 'test_task')"
NEW_COMMAND_DATA = '(cmd "2")'
COMMAND_FOR_ROLES = ["ADMIN", "SECURITY"]
COMMAND_TYPE = "CONFIGURATION"
COMMAND_NAME_FOR_TASK = "AAAA___TEST_COMMAND_FOR_TASK"
COMMAND_TYPE_CONFIGURATION = "CONFIGURATION"
COMMANDS_NAMES_LIST = [COMMAND_NAME, COMMAND_NAME_FOR_TASK]


# test tasks
# такие имена нужны для отображения тестовых заданий вверху списка
TASK_NAME = "____AAA__sSelenium_test_task_name"
NEW_TASK_NAME = "____AAA__sSelenium_test_new__task_name"

# test tasks search & filtering
TASKS_NAMES_FOR_SEARCH_AND_FILTERING = ["123", "234", "34"]
TASKS_COMMANDS_FOR_SEARCH_AND_FILTERING = [
    "Debug mode OFF",
    "Debug mode ON",
    "Device Wipe",
]
TASKS_FILTER_VALUE = "23"
TASK_SEARCH_VALUE = "123"

# test templates
with open(Path(__file__).parent / "template_data.yaml") as f:
    template_test_data = yaml.safe_load(f)

# test ad fields validation (file with no valid data)
with open(Path(__file__).parent / "no_valid_ad_data.yaml") as f:
    NO_VALID_DATA = yaml.safe_load(f)

TEST_PROFILE_TEMPLATE = template_test_data["create"]
TEST_PROFILE_TEMPLATE_UPDATE = template_test_data["update"]

TEST_DATA = {"field": "field1", "value": "values1", "description": "description1"}
UPDATE_TEST_DATA = {
    "field": "field2",
    "value": "values2",
    "description": "description2",
}

STORAGE_URL_BASE = "https://storage.dev.getmobit.ru/testdata/gmserver-integration-test"

# tests license
expired_license = f"{STORAGE_URL_BASE}/getmobit-test_2021-03-11.lic"
overflown_license = f"{STORAGE_URL_BASE}/license_v3.0.0_getmobit-test_1-device.lic"
valid_license = (
    f"{STORAGE_URL_BASE}/license_v3.0.0_getmobit-test_20230202_WITH_SCENARIOS.lic"
)
new_license = (
    f"{STORAGE_URL_BASE}/license_v3.0.0_getmobit-test_20230202_WITH_SCENARIOS.lic"
)

# tests updates
firmware_path = f"{STORAGE_URL_BASE}/bios_H4001.X64.MP.U.05_20200922.swu"
COMMENT = "New Comment"

# test diagnostics
result_zip_file = Path(download_default_directory, "results.zip")

diagnostics_max_wait = (
    60  # Максимальное время ожидания окончания диагностики в секундах
)
diagnostics_download_result_max_wait = (
    5  # Максимальное время ожидания скачивания результатов диагностики в секундах
)

# tests device group
TEST_GROUP_TITLE = "TEST_GROUP_TITLE1"
TEST_GROUP_DESCRIPTION = "TEST_GROUP_DESCRIPTION"
NEW_TEST_GROUP_DESCRIPTION = "NEW_TEST_GROUP_DESCRIPTION"
DEVICE_ID = "180821A1100431"

# tests companies addresses
CORRECT_ADDRESSES_LIST = [
    "127.0.0.1",
    "69::69",
    "илуха.корп",
    "iluha.srv.gm.corp",
    "getmobit.ru",
    "министерство-финансов.рф",
    "республика-марий-эл.рф",
    "минсоц.чита.рф",
    "1.2.3.4",
    "autotest.ta.gm.corp",
]
INCORRECT_ADDRESSES_LIST = [
    "a.b.c",
    "1.2.3.4.5.6.7",
    "127.0.0.1sdvdsfv",
    "1:2:3",
    "khewihfiwerhfyrfy",
    "http://scheme-is-overrated.con",
    "http://autotest.ta.gm.corp/",
]
DEFAULT_COMPANY_ADDRESS = GMSERVER_ADDRESS.host

#  test ad_synchronization
with open(Path(__file__).parent / "ad_synchronization_data.yaml") as f:
    TEST_AD_DATA = yaml.safe_load(f)

#  test connect_AD_from_ldap
with open(Path(__file__).parent / "ldap_synchronization_data.yaml") as f:
    TEST_LDAP_DATA = yaml.safe_load(f)

with open(Path(__file__).parent / "clear_sync_data.yaml") as f:
    CLEAR_AD_DATA = yaml.safe_load(f)

AD_FILTER = "(&(objectClass=person)(!(objectClass=computer))(|(sAMAccountName=ad_*)))"
ALL_USER_FILTER = (
    "(&(objectClass=person)(!(objectClass=computer))(|(sAMAccountName=a*)))"
)
FAKE_FILTER = (
    "(&(objectClass=person)(!(objectClass=computer))(|(sAMAccountName=bred_bred_*)))"
)
STANDARD_USER_FIELDS = (
    "avatar=thumbnailPhoto,configuration.ad.member_of=memberOf,password=userPrincipalName,"
    "title=cn,username=sAMAccountName"
)
SELENIUM_TEST_USER_FILTER = (
    "(&(objectClass=person)(!(objectClass=computer))(|(sAMAccountName=__*)))"
)
SELENIUM_TEST_USERNAME = "___autotest_selenium"
ADMIN_USERNAME = "admin"

SUPERADMIN_USERNAME = "superadmin"
SUPERADMIN_PASSWORD = "superadmin"
NON_AD_USERS = {ADMIN_USERNAME, SUPERADMIN_USERNAME, TEST_USER_PROFILE["username"]}
ALL_USER_FIELDS_CHECKED = (
    "avatar=thumbnailPhoto,"
    "configuration.ad.member_of=memberOf,"
    "configuration.token_id=sAMAccountName,"
    "password=userPrincipalName,"
    "title=cn,"
    "username=sAMAccountName,"
    "configuration.nfc_id=sAMAccountName,"
    "configuration.rfid_id=sAMAccountName,"
    "configuration.vdi.host=sAMAccountName,"
    "configuration.vdi.session=sAMAccountName,"
    "configuration.vdi.user=sAMAccountName,"
    "configuration.vdi.password=sAMAccountName,"
    "configuration.vdi.domain=sAMAccountName,"
    "configuration.vdi.param1=sAMAccountName,"
    "configuration.vdi.param2=sAMAccountName,"
    "configuration.sip.hostname=sAMAccountName,"
    "configuration.sip.username=sAMAccountName,"
    "configuration.sip.userid=sAMAccountName,"
    "configuration.sip.password=sAMAccountName,"
    "configuration.sip.phone=sAMAccountName,"
    "configuration.sip.voicemail=sAMAccountName,"
    "configuration.sip.vlanid=sAMAccountName,"
    "configuration.sip.audio_codecs=sAMAccountName,"
    "configuration.ad.username=sAMAccountName,"
    "configuration.ad.password=sAMAccountName,"
    "configuration.ad.server=sAMAccountName,"
    "configuration.ad.port=sAMAccountName,"
    "configuration.ad.base=sAMAccountName,"
    "configuration.ad.telephone=sAMAccountName,"
    "configuration.ad.filter=sAMAccountName,"
    "configuration.extra=sAMAccountName"
)

# general
AUTOTEST_NAME = "AUTOTEST_NAME"
AUTOTEST_DESCRIPTION = "AUTOTEST_DESCRIPTION"
AUTOTEST_DESCRIPTION_UPDATED = "AUTOTEST_DESCRIPTION_UPDATED"

# список ролей сервера после свежей установки (для фикстуры очистки)
PREDEFINED_ROLES = ("ADMIN", "SUPER_ADMIN", "SECURITY", "USER")


class Roles(Enum):
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
    SECURITY = "SECURITY"
    USER = "USER"
    TEST_ROLE = "TEST_ROLE"
    TEST_NEW_ROLE = "TEST_NEW_ROLE"
    TEST_READONLY_ROLE = "TEST_READONLY_ROLE"


TEST_ROLES_LIST = [Roles.TEST_ROLE.value, Roles.TEST_NEW_ROLE.value]

# список пользователей чистой установки сервера (для фикстуры очистки)
PREDEFINED_USERS = ("admin", "superadmin")

# список команд чистой установки сервера
PREDEFINED_TASKS = ("Zero Deploy Task",)

#  Названия сценариев
TEST_SCENARIO = "TEST_SCENARIO"
UPDATE_TEST_SCENARIO = "UPDATE_TEST_SCENARIO"
FAKE_SCENARIO = "FAKE_SCENARIO"
SCENARIOS = [TEST_SCENARIO, UPDATE_TEST_SCENARIO, FAKE_SCENARIO]
FILTER_TEST = "test"
FILTER_FAKE = "fake"


# расписание запуска сценариев
class ScenarioSchedule(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3


class Day(Enum):
    MONDAY = "mon"
    TUESDAY = "tue"
    WEDNESDAY = "wed"
    THURSDAY = "thu"
    FRIDAY = "fri"
    SATURDAY = "sat"
    SUNDAY = "sun"


class DebugMode(Enum):
    ON = 1
    OFF = 2


DAY_IN_MONTH = random.randint(1, 30)
START_TIME = "14:00"
UPDATED_START_TIME = "15:00"
