"""Browser-level RED for the qualified BasePage ROLE_LINK CLICK handoff."""

from __future__ import annotations

import re

from playwright.sync_api import sync_playwright

from pages.base_page import BasePage

OLD_NAME = "Belt Sander Belt Sander $73.59"
NEW_NAME = "Belt Sander Compare Belt Sander CO2 A B C D E $73.59"


class RepairingCatalogPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.repair_calls = 0

    def _try_repair_role_link_click(
        self,
        *,
        accessible_name: str,
        retry,
    ) -> bool:
        self.repair_calls += 1
        assert accessible_name == OLD_NAME

        replacement = re.compile(
            r"^Belt\b.*?\bSander\b.*?\bBelt\b.*?\bSander\b.*?\b73\b.*?\b59$",
            re.IGNORECASE | re.DOTALL,
        )
        retry(replacement)
        return True


def test_base_page_role_link_handoff_recovers_browser_click() -> None:
    html = f"""
    <main>
      <a
        href="#product"
        aria-label="{NEW_NAME}"
        onclick="document.body.dataset.clicked='yes'"
      >candidate</a>
    </main>
    """

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page()
            page.set_content(html)
            catalog = RepairingCatalogPage(page)

            assert page.get_by_role(
                "link",
                name=OLD_NAME,
                exact=True,
            ).count() == 0
            assert page.get_by_role(
                "link",
                name=NEW_NAME,
                exact=True,
            ).count() == 1

            catalog.click_by_role_link(OLD_NAME)

            assert catalog.repair_calls == 1
            assert (
                page.locator("body").get_attribute("data-clicked")
                == "yes"
            )
        finally:
            browser.close()
