from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shura.pages.applications_page import ApplicationsPage
from shura.pages.commands_page import CommandsPage
from shura.pages.companies_page import CompaniesPage
from shura.pages.device_groups_page import DeviceGroupsPage
from shura.pages.devices_page import DevicesPage
from shura.pages.diagnostics_page import DiagnosticsPage
from shura.pages.journal_page import JournalPage
from shura.pages.license_page import LicensePage
from shura.pages.roles_page import RolesPage
from shura.pages.scenarios_page import ScenarioPage
from shura.pages.settings_page import SettingsPage
from shura.pages.summary_page import SummaryPage
from shura.pages.tasks_page import TasksPage
from shura.pages.templates_page import TemplateDefinitionPage
from shura.pages.updates_page import UpdatesPage
from shura.pages.user_page import UserPage
from shura.panels.base import Panel


class NavPanel(Panel):
    ID = "NavigationLink"

    def _goto_page(self, element_id: str):
        self.driver.find_element(By.ID, f"{self.ID}__{element_id}").click()

    def goto_summary_page(self) -> SummaryPage:
        self._goto_page("summary")
        return SummaryPage(self.driver)

    def goto_devices_page(self) -> DevicesPage:
        self._goto_page("devices")
        return DevicesPage(self.driver)

    def goto_device_group_page(self) -> DeviceGroupsPage:
        self._goto_page("groups")
        return DeviceGroupsPage(self.driver)

    def goto_user_page(self) -> UserPage:
        self._goto_page("employees")
        return UserPage(self.driver)

    def goto_template_page(self) -> TemplateDefinitionPage:
        self._goto_page("templates")
        return TemplateDefinitionPage(self.driver)

    def goto_roles_page(self) -> RolesPage:
        self._goto_page("roles")
        return RolesPage(self.driver)

    def goto_updates_page(self) -> UpdatesPage:
        self._goto_page("updates")
        return UpdatesPage(self.driver)

    def goto_applications_page(self) -> ApplicationsPage:
        self._goto_page("applications")
        return ApplicationsPage(self.driver)

    def goto_tasks_page(self) -> TasksPage:
        self._goto_page("tasks")
        return TasksPage(self.driver)

    def goto_commands_page(self) -> CommandsPage:
        self._goto_page("commands")
        return CommandsPage(self.driver)

    def goto_companies_page(self) -> CompaniesPage:
        self._goto_page("companies")
        return CompaniesPage(self.driver)

    def goto_journal_page(self) -> JournalPage:
        self._goto_page("journal")
        return JournalPage(self.driver)

    def goto_settings_page(self) -> SettingsPage:
        self._goto_page("settings")
        return SettingsPage(self.driver)

    def goto_license_page(self) -> LicensePage:
        self._goto_page("settings")
        self.driver.find_element(By.CSS_SELECTOR, "a.tab__license").click()
        return LicensePage(self.driver)

    def goto_diagnostics_page(self) -> DiagnosticsPage:
        self._goto_page("diagnostics")
        return DiagnosticsPage(self.driver)

    def goto_scenario_page(self) -> ScenarioPage:
        self._goto_page("scenarios")
        return ScenarioPage(self.driver)

    def logout_link(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, f"{self.ID}__logout"))
        )

    def logout_confirm(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Logout__confirm"))
        )
