"""Reusable UI component object for price summary widgets."""

from playwright.sync_api import Locator, Page

from components.base_component import BaseComponent


class PriceSummary(BaseComponent):
    """Small component abstraction around a total price field."""

    def __init__(
        self,
        page: Page,
        total_test_id: str,
        root: Locator | None = None,
    ) -> None:
        super().__init__(page, root=root)
        self.total_test_id = total_test_id

    def total(self) -> str:
        return self.text_by_test_id(self.total_test_id)
