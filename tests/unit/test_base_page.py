"""Unit tests for BasePage.

These tests protect reusable POM framework behavior without starting a browser.
"""

import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class FakeLocator:
    def __init__(
        self,
        text: str = "Example text",
        texts: list[str] | None = None,
        visible: bool = True,
        *,
        fail_click: bool = False,
        fail_fill: bool = False,
    ) -> None:
        self.text = text
        self.texts = texts or ["First", "Second"]
        self.visible = visible
        self.fail_click = fail_click
        self.fail_fill = fail_fill
        self.clicked = False
        self.filled_with: str | None = None

    def click(self) -> None:
        if self.fail_click:
            raise PlaywrightTimeoutError("click timed out")
        self.clicked = True

    def fill(self, value: str) -> None:
        if self.fail_fill:
            raise PlaywrightTimeoutError("fill timed out")
        self.filled_with = value

    def inner_text(self) -> str:
        return self.text

    def all_inner_texts(self) -> list[str]:
        return self.texts

    def is_visible(self) -> bool:
        return self.visible


class FakePage:
    def __init__(self) -> None:
        self.navigated_to: str | None = None
        self.requested_test_ids: list[str] = []
        self.locators_by_test_id: dict[str, FakeLocator] = {}
        self.load_states: list[str] = []
        self.url = "http://example.test/current"
        self.page_title = "Example title"

    def goto(self, url: str) -> None:
        self.navigated_to = url

    def wait_for_load_state(self, state: str) -> None:
        self.load_states.append(state)

    def get_by_test_id(self, test_id: str) -> FakeLocator:
        self.requested_test_ids.append(test_id)
        return self.locators_by_test_id.setdefault(test_id, FakeLocator())

    def title(self) -> str:
        return self.page_title


class TestBasePageNavigation:
    def test_open_without_path_uses_base_url(self):
        page = FakePage()
        base_page = BasePage(page, base_url="http://example.test/app")

        base_page.open()

        assert page.navigated_to == "http://example.test/app"

    def test_open_uses_path_relative_to_base_url(self):
        page = FakePage()
        base_page = BasePage(page, base_url="http://example.test/app")

        base_page.open("/dashboard")

        assert page.navigated_to == "http://example.test/app/dashboard"

    def test_open_supports_path_without_leading_slash(self):
        page = FakePage()
        base_page = BasePage(page, base_url="http://example.test/app")

        base_page.open("dashboard")

        assert page.navigated_to == "http://example.test/app/dashboard"

    def test_open_supports_absolute_url(self):
        page = FakePage()
        base_page = BasePage(page, base_url="http://example.test/app")

        base_page.open("https://external.example/login")

        assert page.navigated_to == "https://external.example/login"

    def test_open_without_base_url_uses_path_as_is(self):
        page = FakePage()
        base_page = BasePage(page)

        base_page.open("/local-path")

        assert page.navigated_to == "/local-path"

    def test_wait_for_ready_waits_for_domcontentloaded(self):
        page = FakePage()
        base_page = BasePage(page)

        base_page.wait_for_ready()

        assert page.load_states == ["domcontentloaded"]


class TestBasePageTestIdHelpers:
    def test_by_test_id_delegates_to_page(self):
        page = FakePage()
        base_page = BasePage(page)

        locator = base_page.by_test_id("submit-button")

        assert isinstance(locator, FakeLocator)
        assert page.requested_test_ids == ["submit-button"]

    def test_click_by_test_id_clicks_locator(self):
        page = FakePage()
        locator = FakeLocator()
        page.locators_by_test_id["submit-button"] = locator
        base_page = BasePage(page)

        base_page.click_by_test_id("submit-button")

        assert locator.clicked is True

    def test_fill_by_test_id_fills_locator(self):
        page = FakePage()
        locator = FakeLocator()
        page.locators_by_test_id["username"] = locator
        base_page = BasePage(page)

        base_page.fill_by_test_id("username", "marcin")

        assert locator.filled_with == "marcin"

    def test_click_by_test_id_uses_optional_repair_hook_after_timeout(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ):
        page = FakePage()
        page.locators_by_test_id["old-submit"] = FakeLocator(fail_click=True)
        replacement = FakeLocator()
        page.locators_by_test_id["new-submit"] = replacement
        base_page = BasePage(page)

        def recover(*, action_name: str, test_id: str, retry) -> bool:
            assert action_name == "click"
            assert test_id == "old-submit"
            retry("new-submit")
            return True

        monkeypatch.setattr(base_page, "_try_repair_test_id_action", recover)

        base_page.click_by_test_id("old-submit")

        assert replacement.clicked is True

    def test_fill_by_test_id_uses_optional_repair_hook_after_timeout(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ):
        page = FakePage()
        page.locators_by_test_id["old-username"] = FakeLocator(fail_fill=True)
        replacement = FakeLocator()
        page.locators_by_test_id["new-username"] = replacement
        base_page = BasePage(page)

        def recover(*, action_name: str, test_id: str, retry) -> bool:
            assert action_name == "fill"
            assert test_id == "old-username"
            retry("new-username")
            return True

        monkeypatch.setattr(base_page, "_try_repair_test_id_action", recover)

        base_page.fill_by_test_id("old-username", "marcin")

        assert replacement.filled_with == "marcin"

    def test_original_timeout_is_preserved_when_repair_does_not_recover(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ):
        page = FakePage()
        page.locators_by_test_id["old-username"] = FakeLocator(fail_fill=True)
        base_page = BasePage(page)

        monkeypatch.setattr(
            base_page,
            "_try_repair_test_id_action",
            lambda **_: False,
        )

        with pytest.raises(PlaywrightTimeoutError, match="fill timed out"):
            base_page.fill_by_test_id("old-username", "marcin")

    def test_non_timeout_playwright_error_is_not_delegated_to_repair(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ):
        page = FakePage()
        locator = FakeLocator()

        def fail_fill(_: str) -> None:
            raise PlaywrightError("browser interaction failed")

        locator.fill = fail_fill
        page.locators_by_test_id["username"] = locator
        base_page = BasePage(page)

        def unexpected_repair(**_) -> bool:
            pytest.fail("Repair hook must not run for non-timeout Playwright errors.")

        monkeypatch.setattr(
            base_page,
            "_try_repair_test_id_action",
            unexpected_repair,
        )

        with pytest.raises(PlaywrightError, match="browser interaction failed"):
            base_page.fill_by_test_id("username", "marcin")

    def test_text_by_test_id_returns_inner_text(self):
        page = FakePage()
        page.locators_by_test_id["message"] = FakeLocator(text="Saved")
        base_page = BasePage(page)

        assert base_page.text_by_test_id("message") == "Saved"

    def test_texts_by_test_id_returns_all_inner_texts(self):
        page = FakePage()
        page.locators_by_test_id["row"] = FakeLocator(texts=["A", "B", "C"])
        base_page = BasePage(page)

        assert base_page.texts_by_test_id("row") == ["A", "B", "C"]

    def test_is_visible_by_test_id_returns_visibility(self):
        page = FakePage()
        page.locators_by_test_id["modal"] = FakeLocator(visible=False)
        base_page = BasePage(page)

        assert base_page.is_visible_by_test_id("modal") is False


class TestBasePageMetadata:
    def test_current_url_returns_page_url(self):
        page = FakePage()
        page.url = "http://example.test/orders/123"
        base_page = BasePage(page)

        assert base_page.current_url() == "http://example.test/orders/123"

    def test_title_returns_page_title(self):
        page = FakePage()
        page.page_title = "Dashboard"
        base_page = BasePage(page)

        assert base_page.title() == "Dashboard"
