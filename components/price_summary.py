"""Reusable UI component object for price summary widgets."""

from playwright.sync_api import Page


class PriceSummary:
    """Small component abstraction around a total price field."""

    def __init__(self, page: Page, total_test_id: str) -> None:
        self.page = page
        self.total_test_id = total_test_id

    def total(self) -> str:
        return self.page.get_by_test_id(self.total_test_id).inner_text()
