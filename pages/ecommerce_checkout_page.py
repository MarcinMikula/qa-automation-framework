"""Page Object for the local demo shop checkout page."""

from playwright.sync_api import Page

from components.price_summary import PriceSummary


class EcommerceCheckoutPage:
    """Checkout page for the local e-commerce POM case study."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.price_summary = PriceSummary(page, total_test_id="checkout-total")

    def total(self) -> str:
        return self.price_summary.total()

    def place_order(self, customer_name: str) -> None:
        self.page.get_by_test_id("customer-name").fill(customer_name)
        self.page.get_by_test_id("place-order").click()
