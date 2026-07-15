"""Page Object for the local demo shop search page."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class EcommerceSearchPage(BasePage):
    """Search page for the local e-commerce POM case study."""

    def __init__(self, page: Page, base_url: str = "http://localhost:8010/shop") -> None:
        super().__init__(page, base_url=base_url)

    def search_for(self, query: str) -> None:
        self.fill_by_test_id("search-input", query)
        self.click_by_test_id("search-submit")

    def open_product(self, slug: str) -> None:
        self.click_by_test_id(f"open-product-{slug}")

    def result_names(self) -> list[str]:
        return self.texts_by_test_id("product-card-name")
