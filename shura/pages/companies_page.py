from shura.pages.base import ItemsTablePage
from shura.panels.base import Locator
from shura.panels.object import ObjectPanel


class CompaniesPanel(ObjectPanel):
    ID = "CompanyCreate"
    CSS_SELECTOR_LOCATOR: Locator = ".RightPanel"

    def address_field(self):
        return self.element_by_id("primary-address")


class CompaniesPage(ItemsTablePage):
    ...
