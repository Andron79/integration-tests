import logging

from shura.pages.base import ItemsTablePage
from shura.panels.base import Locator
from shura.panels.object import ObjectPanel

logger = logging.getLogger(__name__)


class UpdatesPage(ItemsTablePage):
    pass


class FirmwarePanel(ObjectPanel):
    ID = "FirmwareCreate"
    CSS_SELECTOR_LOCATOR: Locator = ".RightPanel"

    def comment_field(self):
        return self.element_by_id("comment")
