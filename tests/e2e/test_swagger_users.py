"""E2E smoke tests for the local users service Swagger UI.

This is a technical smoke test, not the main POM case study.

The realistic POM case study lives in `test_ecommerce_checkout_flow.py`.
"""

from playwright.sync_api import Page

from pages.swagger_users_page import SwaggerUsersPage


class TestSwaggerUsersE2E:
    """[DOMAIN: GENERIC] Swagger UI smoke tests through a Page Object."""

    def test_get_users_returns_response(
        self,
        page: Page,
        users_service_for_swagger: str,
    ):
        """GET /users through Swagger UI returns a response from the service."""
        swagger = SwaggerUsersPage(page)
        swagger.open(f"{users_service_for_swagger}/docs")
        swagger.execute_get_users()

        response = swagger.get_response_body()

        assert response is not None
        assert len(response) > 0

    def test_swagger_ui_loads(
        self,
        page: Page,
        users_service_for_swagger: str,
    ):
        """Swagger UI for the users service loads correctly."""
        swagger = SwaggerUsersPage(page)
        swagger.open(f"{users_service_for_swagger}/docs")

        assert "Users Service" in page.title()
