"""Fail-before tests for Page-owned lifecycle plus scoped interactions."""

from __future__ import annotations

import sys
import types
from enum import StrEnum

from pages.base_page import BasePage


class FakeLocator:
    def __init__(self) -> None:
        self.clicked = False
        self.filled_with: str | None = None

    def count(self) -> int:
        return 1

    def click(self) -> None:
        self.clicked = True

    def fill(self, value: str) -> None:
        self.filled_with = value


class FakeScope:
    def __init__(self) -> None:
        self.requested_test_ids: list[str] = []
        self.requested_roles: list[tuple[str, object, bool]] = []
        self.test_id_locators: dict[str, FakeLocator] = {}
        self.role_locators: dict[tuple[str, object], FakeLocator] = {}

    def get_by_test_id(self, test_id: str) -> FakeLocator:
        self.requested_test_ids.append(test_id)
        return self.test_id_locators.setdefault(
            test_id,
            FakeLocator(),
        )

    def get_by_role(
        self,
        role: str,
        *,
        name: object,
        exact: bool = False,
    ) -> FakeLocator:
        self.requested_roles.append((role, name, exact))
        return self.role_locators.setdefault(
            (role, name),
            FakeLocator(),
        )


class FakePage(FakeScope):
    def __init__(self) -> None:
        super().__init__()
        self.navigated_to: str | None = None
        self.load_states: list[str] = []
        self.url = "http://example.test/current"
        self.page_title = "Example title"

    def goto(self, url: str) -> None:
        self.navigated_to = url

    def wait_for_load_state(self, state: str) -> None:
        self.load_states.append(state)

    def title(self) -> str:
        return self.page_title


def test_base_page_keeps_page_lifecycle_but_routes_interactions_to_scope() -> None:
    page = FakePage()
    scope = FakeScope()

    base_page = BasePage(
        page,
        base_url="http://example.test/app",
        interaction_scope=scope,
    )

    base_page.open("/dashboard")
    locator = base_page.by_test_id("inside-frame")

    assert page.navigated_to == "http://example.test/app/dashboard"
    assert page.requested_test_ids == []
    assert scope.requested_test_ids == ["inside-frame"]
    assert locator is scope.test_id_locators["inside-frame"]


def test_test_id_repair_handoff_receives_interaction_scope(
    monkeypatch,
) -> None:
    page = FakePage()
    scope = FakeScope()
    base_page = BasePage(page, interaction_scope=scope)

    captured: dict[str, object] = {}

    package = types.ModuleType("test_repair_engine")
    package.__path__ = []

    contracts = types.ModuleType("test_repair_engine.contracts")

    class RepairAction(StrEnum):
        CLICK = "click"
        FILL = "fill"

    contracts.RepairAction = RepairAction

    adapter = types.ModuleType("test_repair_engine.playwright_adapter")

    def recover_test_id_action(
        received_scope,
        **kwargs,
    ) -> bool:
        captured["scope"] = received_scope
        captured["action"] = kwargs["action"]
        return False

    adapter.recover_test_id_action = recover_test_id_action

    monkeypatch.setitem(
        sys.modules,
        "test_repair_engine",
        package,
    )
    monkeypatch.setitem(
        sys.modules,
        "test_repair_engine.contracts",
        contracts,
    )
    monkeypatch.setitem(
        sys.modules,
        "test_repair_engine.playwright_adapter",
        adapter,
    )

    recovered = base_page._try_repair_test_id_action(
        action_name="fill",
        test_id="old-search",
        retry=lambda _: None,
    )

    assert recovered is False
    assert captured["scope"] is scope
    assert captured["action"] is RepairAction.FILL


def test_role_link_repair_handoff_receives_interaction_scope(
    monkeypatch,
) -> None:
    page = FakePage()
    scope = FakeScope()
    base_page = BasePage(page, interaction_scope=scope)

    captured: dict[str, object] = {}

    package = types.ModuleType("test_repair_engine")
    package.__path__ = []

    adapter = types.ModuleType("test_repair_engine.playwright_adapter")

    def recover_role_link_click(
        received_scope,
        **kwargs,
    ) -> bool:
        captured["scope"] = received_scope
        captured["name"] = kwargs["original_accessible_name"]
        return False

    adapter.recover_role_link_click = recover_role_link_click

    monkeypatch.setitem(
        sys.modules,
        "test_repair_engine",
        package,
    )
    monkeypatch.setitem(
        sys.modules,
        "test_repair_engine.playwright_adapter",
        adapter,
    )

    recovered = base_page._try_repair_role_link_click(
        accessible_name="Belt Sander",
        retry=lambda _: None,
    )

    assert recovered is False
    assert captured["scope"] is scope
    assert captured["name"] == "Belt Sander"