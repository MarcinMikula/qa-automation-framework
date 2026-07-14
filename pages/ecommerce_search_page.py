"""Page Object for the local demo shop search page."""

from playwright.sync_api import Page


class EcommerceSearchPage:
    """Search page for the local e-commerce POM case study."""

    def __init__(self, page: Page, base_url: str = "http://localhost:8010/shop") -> None:
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        self.page.goto(self.base_url)

    def search_for(self, query: str) -> None:
        self.page.get_by_test_id("search-input").fill(query)
        self.page.get_by_test_id("search-submit").click()

    def open_product(self, slug: str) -> None:
        self.page.get_by_test_id(f"open-product-{slug}").click()

    def result_names(self) -> list[str]:
        return self.page.get_by_test_id("product-card-name").all_inner_texts()
