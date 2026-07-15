"""Shared base class for Page Objects.

BasePage contains small, reusable browser interaction helpers.

It should not contain business assertions or application-specific flows.
Concrete Page Objects should expose domain-readable actions, while tests own
business assertions.
"""

from __future__ import annotations

from urllib.parse import urljoin

from playwright.sync_api import Locator, Page


class BasePage:
    """Base class for UI-facing Page Objects.

    The class intentionally stays small.

    It provides common Playwright interaction helpers without turning Page
    Objects into assertion-heavy test containers.
    """

    def __init__(self, page: Page, base_url: str = "") -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = "") -> None:
        """Open an absolute URL or a path relative to the configured base URL."""
        self.page.goto(self._build_url(path))

    def wait_for_ready(self) -> None:
        """Wait until the current page reaches the DOM content loaded state."""
        self.page.wait_for_load_state("domcontentloaded")

    def by_test_id(self, test_id: str) -> Locator:
        """Return a locator for a stable data-testid selector."""
        return self.page.get_by_test_id(test_id)

    def click_by_test_id(self, test_id: str) -> None:
        """Click an element identified by data-testid."""
        self.by_test_id(test_id).click()

    def fill_by_test_id(self, test_id: str, value: str) -> None:
        """Fill an input identified by data-testid."""
        self.by_test_id(test_id).fill(value)

    def text_by_test_id(self, test_id: str) -> str:
        """Return text from an element identified by data-testid."""
        return self.by_test_id(test_id).inner_text()

    def texts_by_test_id(self, test_id: str) -> list[str]:
        """Return text values from all matching data-testid elements."""
        return self.by_test_id(test_id).all_inner_texts()

    def is_visible_by_test_id(self, test_id: str) -> bool:
        """Return visibility state for an element identified by data-testid."""
        return self.by_test_id(test_id).is_visible()

    def current_url(self) -> str:
        """Return the current browser URL."""
        return self.page.url

    def title(self) -> str:
        """Return the current browser page title."""
        return self.page.title()

    def _build_url(self, path: str) -> str:
        """Build a URL from an absolute URL or a path relative to base_url."""
        if path.startswith(("http://", "https://")):
            return path

        if not self.base_url:
            return path

        if not path:
            return self.base_url

        return urljoin(f"{self.base_url}/", path.lstrip("/"))
