"""Swagger UI Page Object for the local users service.

This is a technical smoke Page Object.

It proves that the browser can interact with a local FastAPI Swagger UI, but it
is not the main POM case study.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage


class SwaggerUsersPage(BasePage):
    """Page Object for the users service Swagger UI."""

    GET_USERS_SECTION = "#operations-users-list_items_users_get div"
    EXECUTE_BUTTON = ".execute-wrapper"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def execute_get_users(self) -> None:
        """Expand GET /users and execute it through the Swagger UI."""
        self.page.locator(self.GET_USERS_SECTION).filter(
            has_text="GET/usersList Items"
        ).click()
        self.page.locator("div").filter(has_text="Parameters").first.click()
        self.page.locator(self.EXECUTE_BUTTON).click()

    def execute_post_user(self) -> None:
        """Expand POST /users and execute it through the Swagger UI."""
        self.page.get_by_role("button", name="POST /users Create Item").click()
        self.page.locator("div").filter(has_text="Parameters").nth(2).click()
        self.page.locator(self.EXECUTE_BUTTON).click()

    def get_response_body(self) -> str:
        """Return text from the last Swagger response section."""
        return self.page.locator(".responses-wrapper").inner_text()
