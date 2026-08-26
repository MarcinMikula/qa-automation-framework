"""Shared base class for Page Objects.

BasePage contains small, reusable browser interaction helpers.

It should not contain business assertions or application-specific flows.
Concrete Page Objects should expose domain-readable actions, while tests own
business assertions.
"""

from __future__ import annotations

from collections.abc import Callable
from urllib.parse import urljoin

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


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
        try:
            self.by_test_id(test_id).click()
        except PlaywrightError as exc:
            if not self._should_delegate_test_id_repair(error=exc, test_id=test_id):
                raise

            recovered = self._try_repair_test_id_action(
                action_name="click",
                test_id=test_id,
                retry=lambda replacement: self.by_test_id(replacement).click(),
            )
            if recovered:
                return
            raise

    def fill_by_test_id(self, test_id: str, value: str) -> None:
        """Fill an input identified by data-testid."""
        try:
            self.by_test_id(test_id).fill(value)
        except PlaywrightError as exc:
            if not self._should_delegate_test_id_repair(error=exc, test_id=test_id):
                raise

            recovered = self._try_repair_test_id_action(
                action_name="fill",
                test_id=test_id,
                retry=lambda replacement: self.by_test_id(replacement).fill(value),
            )
            if recovered:
                return
            raise

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

    def _should_delegate_test_id_repair(
        self,
        *,
        error: PlaywrightError,
        test_id: str,
    ) -> bool:
        """Return whether a failed test-id interaction may enter TRE."""

        if isinstance(error, PlaywrightTimeoutError):
            return True

        if "strict mode violation" not in error.message.lower():
            return False

        try:
            return self.by_test_id(test_id).count() > 1
        except PlaywrightError:
            return False
    def _try_repair_test_id_action(
        self,
        *,
        action_name: str,
        test_id: str,
        retry: Callable[[str], None],
    ) -> bool:
        """Delegate one qualified failed test-id interaction to optional TestRepairEngine.

        The import is deliberately lazy so the framework remains independently
        runnable when TestRepairEngine is not installed. If the package is
        installed but its own import fails for another reason, that error is not
        hidden as an optional-dependency absence.
        """

        try:
            from test_repair_engine.contracts import RepairAction
            from test_repair_engine.playwright_adapter import recover_test_id_action
        except ModuleNotFoundError as exc:
            if exc.name == "test_repair_engine":
                return False
            raise

        return recover_test_id_action(
            self.page,
            action=RepairAction(action_name),
            original_test_id=test_id,
            retry=retry,
            page_object=self.__class__.__name__,
            method_name=f"{action_name}_by_test_id",
        )

    def _build_url(self, path: str) -> str:
        """Build a URL from an absolute URL or a path relative to base_url."""
        if path.startswith(("http://", "https://")):
            return path

        if not self.base_url:
            return path

        if not path:
            return self.base_url

        return urljoin(f"{self.base_url}/", path.lstrip("/"))
