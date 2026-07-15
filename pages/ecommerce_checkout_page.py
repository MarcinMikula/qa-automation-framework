"""Page Object for the local demo shop checkout page."""

from playwright.sync_api import Page

from components.price_summary import PriceSummary
from pages.base_page import BasePage


class EcommerceCheckoutPage(BasePage):
    """Checkout page for the local e-commerce POM case study."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.price_summary = PriceSummary(page, total_test_id="checkout-total")

    def total(self) -> str:
        return self.price_summary.total()

    def place_order(self, customer_name: str) -> None:
        self.fill_by_test_id("customer-name", customer_name)
        self.click_by_test_id("place-order")
