"""Page Object for the local demo shop product details page."""

from playwright.sync_api import Page


class EcommerceProductPage:
    """Product details page for the local e-commerce POM case study."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def product_name(self) -> str:
        return self.page.get_by_test_id("product-name").inner_text()

    def price(self) -> str:
        return self.page.get_by_test_id("product-price").inner_text()

    def availability(self) -> str:
        return self.page.get_by_test_id("product-availability").inner_text()

    def add_to_cart(self) -> None:
        self.page.get_by_test_id("add-to-cart").click()
