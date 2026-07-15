"""Page Object for the local demo shop order confirmation page."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class EcommerceOrderConfirmationPage(BasePage):
    """Order confirmation page for the local e-commerce POM case study."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def order_id(self) -> str:
        return self.text_by_test_id("order-id")

    def status(self) -> str:
        return self.text_by_test_id("order-status")

    def customer_name(self) -> str:
        return self.text_by_test_id("order-customer")

    def item_names(self) -> list[str]:
        return self.texts_by_test_id("confirmed-order-item")

    def total(self) -> str:
        return self.text_by_test_id("order-total")
