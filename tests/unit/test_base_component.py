"""Unit tests for BaseComponent.

These tests protect reusable component-level POM behavior without starting a
browser.
"""

from components.base_component import BaseComponent
from components.price_summary import PriceSummary


class FakeLocator:
    def __init__(
        self,
        text: str = "Example text",
        texts: list[str] | None = None,
        visible: bool = True,
    ) -> None:
        self.text = text
        self.texts = texts or ["First", "Second"]
        self.visible = visible
        self.clicked = False
        self.filled_with: str | None = None
        self.requested_selectors: list[str] = []
        self.requested_test_ids: list[str] = []
        self.child_locators: dict[str, FakeLocator] = {}
        self.child_test_id_locators: dict[str, FakeLocator] = {}

    def locator(self, selector: str) -> "FakeLocator":
        self.requested_selectors.append(selector)
        return self.child_locators.setdefault(selector, FakeLocator())

    def get_by_test_id(self, test_id: str) -> "FakeLocator":
        self.requested_test_ids.append(test_id)
        return self.child_test_id_locators.setdefault(test_id, FakeLocator())

    def click(self) -> None:
        self.clicked = True

    def fill(self, value: str) -> None:
        self.filled_with = value

    def inner_text(self) -> str:
        return self.text

    def all_inner_texts(self) -> list[str]:
        return self.texts

    def is_visible(self) -> bool:
        return self.visible


class FakePage:
    def __init__(self) -> None:
        self.requested_selectors: list[str] = []
        self.requested_test_ids: list[str] = []
        self.locators_by_selector: dict[str, FakeLocator] = {}
        self.locators_by_test_id: dict[str, FakeLocator] = {}

    def locator(self, selector: str) -> FakeLocator:
        self.requested_selectors.append(selector)
        return self.locators_by_selector.setdefault(selector, FakeLocator())

    def get_by_test_id(self, test_id: str) -> FakeLocator:
        self.requested_test_ids.append(test_id)
        return self.locators_by_test_id.setdefault(test_id, FakeLocator())


class TestBaseComponentPageScopedLocators:
    def test_locator_uses_page_when_root_is_not_provided(self):
        page = FakePage()
        component = BaseComponent(page)

        locator = component.locator(".price-summary")

        assert isinstance(locator, FakeLocator)
        assert page.requested_selectors == [".price-summary"]

    def test_by_test_id_uses_page_when_root_is_not_provided(self):
        page = FakePage()
        component = BaseComponent(page)

        locator = component.by_test_id("cart-total")

        assert isinstance(locator, FakeLocator)
        assert page.requested_test_ids == ["cart-total"]


class TestBaseComponentRootScopedLocators:
    def test_locator_uses_root_when_root_is_provided(self):
        page = FakePage()
        root = FakeLocator()
        component = BaseComponent(page, root=root)

        locator = component.locator(".total")

        assert isinstance(locator, FakeLocator)
        assert root.requested_selectors == [".total"]
        assert page.requested_selectors == []

    def test_by_test_id_uses_root_when_root_is_provided(self):
        page = FakePage()
        root = FakeLocator()
        component = BaseComponent(page, root=root)

        locator = component.by_test_id("total")

        assert isinstance(locator, FakeLocator)
        assert root.requested_test_ids == ["total"]
        assert page.requested_test_ids == []


class TestBaseComponentInteractions:
    def test_click_by_test_id_clicks_locator(self):
        page = FakePage()
        locator = FakeLocator()
        page.locators_by_test_id["confirm"] = locator
        component = BaseComponent(page)

        component.click_by_test_id("confirm")

        assert locator.clicked is True

    def test_fill_by_test_id_fills_locator(self):
        page = FakePage()
        locator = FakeLocator()
        page.locators_by_test_id["quantity"] = locator
        component = BaseComponent(page)

        component.fill_by_test_id("quantity", "2")

        assert locator.filled_with == "2"

    def test_text_by_test_id_returns_inner_text(self):
        page = FakePage()
        page.locators_by_test_id["status"] = FakeLocator(text="Ready")
        component = BaseComponent(page)

        assert component.text_by_test_id("status") == "Ready"

    def test_texts_by_test_id_returns_all_inner_texts(self):
        page = FakePage()
        page.locators_by_test_id["row"] = FakeLocator(texts=["A", "B"])
        component = BaseComponent(page)

        assert component.texts_by_test_id("row") == ["A", "B"]

    def test_is_visible_by_test_id_returns_visibility(self):
        page = FakePage()
        page.locators_by_test_id["banner"] = FakeLocator(visible=False)
        component = BaseComponent(page)

        assert component.is_visible_by_test_id("banner") is False


class TestPriceSummary:
    def test_total_reads_text_from_configured_test_id(self):
        page = FakePage()
        page.locators_by_test_id["cart-total"] = FakeLocator(text="4999.00 PLN")
        price_summary = PriceSummary(page, total_test_id="cart-total")

        assert price_summary.total() == "4999.00 PLN"

    def test_total_can_be_scoped_to_root(self):
        page = FakePage()
        root = FakeLocator()
        root.child_test_id_locators["cart-total"] = FakeLocator(text="4999.00 PLN")
        price_summary = PriceSummary(page, total_test_id="cart-total", root=root)

        assert price_summary.total() == "4999.00 PLN"
        assert root.requested_test_ids == ["cart-total"]
        assert page.requested_test_ids == []
