"""Page Object for the local demo shop cart page."""

from playwright.sync_api import Page

from components.price_summary import PriceSummary
from pages.base_page import BasePage


class EcommerceCartPage(BasePage):
    """Cart page for the local e-commerce POM case study."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.price_summary = PriceSummary(page, total_test_id="cart-total")

    def item_names(self) -> list[str]:
        return self.texts_by_test_id("cart-item-name")

    def total(self) -> str:
        return self.price_summary.total()

    def proceed_to_checkout(self) -> None:
        self.click_by_test_id("continue-to-checkout")
