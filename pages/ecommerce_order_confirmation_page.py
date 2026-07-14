"""Page Object for the local demo shop order confirmation page."""

from playwright.sync_api import Page


class EcommerceOrderConfirmationPage:
    """Order confirmation page for the local e-commerce POM case study."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def order_id(self) -> str:
        return self.page.get_by_test_id("order-id").inner_text()

    def status(self) -> str:
        return self.page.get_by_test_id("order-status").inner_text()

    def customer_name(self) -> str:
        return self.page.get_by_test_id("order-customer").inner_text()

    def item_names(self) -> list[str]:
        return self.page.get_by_test_id("confirmed-order-item").all_inner_texts()

    def total(self) -> str:
        return self.page.get_by_test_id("order-total").inner_text()
