"""Page Object for the local demo shop product details page."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class EcommerceProductPage(BasePage):
    """Product details page for the local e-commerce POM case study."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def product_name(self) -> str:
        return self.text_by_test_id("product-name")

    def price(self) -> str:
        return self.text_by_test_id("product-price")

    def availability(self) -> str:
        return self.text_by_test_id("product-availability")

    def add_to_cart(self) -> None:
        self.click_by_test_id("add-to-cart")
