"""Shared base class for reusable UI components.

BaseComponent contains small, reusable browser interaction helpers scoped to a
component root when a root locator is provided.

It should not contain business assertions or application-specific workflows.
Concrete components should expose reusable UI fragment behavior, while tests own
business assertions.
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page


class BaseComponent:
    """Base class for reusable UI component objects.

    A component may be global to the page or scoped to a root locator.

    Scoped components are useful when the same UI fragment appears more than
    once on a page, for example rows, cards, banners, modals, or price summaries.
    """

    def __init__(self, page: Page, root: Locator | None = None) -> None:
        self.page = page
        self.root = root

    def locator(self, selector: str) -> Locator:
        """Return a locator scoped to the component root when available."""
        if self.root is not None:
            return self.root.locator(selector)

        return self.page.locator(selector)

    def by_test_id(self, test_id: str) -> Locator:
        """Return a data-testid locator scoped to the component when possible."""
        if self.root is not None:
            return self.root.get_by_test_id(test_id)

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
