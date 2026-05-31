"""
test_swagger_users.py
[DOMAIN: GENERIC] Test E2E — Swagger UI serwisu users przez Page Object.
Uruchomienie:
    pytest tests/e2e/ -v
"""
import pytest
from playwright.sync_api import Page
from pages.swagger_users_page import SwaggerUsersPage


class TestSwaggerUsersE2E:
    """[DOMAIN: GENERIC] Testy E2E przez Swagger UI."""

    def test_get_users_returns_response(self, page: Page):
        """GET /users przez UI zwraca odpowiedź z serwisu."""
        swagger = SwaggerUsersPage(page)
        swagger.open()
        swagger.execute_get_users()
        response = swagger.get_response_body()
        assert response is not None
        assert len(response) > 0

    def test_swagger_ui_loads(self, page: Page):
        """[DOMAIN: GENERIC] Swagger UI ładuje się poprawnie."""
        swagger = SwaggerUsersPage(page)
        swagger.open()
        assert "Users Service" in page.title()