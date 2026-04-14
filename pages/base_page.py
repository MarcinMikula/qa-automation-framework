"""
base_page.py
Bazowa klasa dla wszystkich Page Object Model.
Enkapsuluje wspólne akcje Playwrighta — DRY na poziomie warstwy UI.
"""
from playwright.sync_api import Page
from testdata.settings import DEFAULT_TIMEOUT


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = DEFAULT_TIMEOUT

    def navigate(self, url: str):
        self.page.goto(url)

    def click(self, selector: str):
        self.page.locator(selector).click(timeout=self.timeout)

    def fill(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_for_url(self, url_pattern: str):
        self.page.wait_for_url(url_pattern, timeout=self.timeout)
