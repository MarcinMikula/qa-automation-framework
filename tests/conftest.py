"""
conftest.py
Fixtures pytest — zarzadzanie cyklem zycia przegladarki i sesji API.
"""
import pytest
from playwright.sync_api import sync_playwright
from testdata.settings import AGENT_USER, AGENT_PASS
from api.auth_service import AuthService


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="session")
def api_token():
    """Pobiera token JWT dla agenta — reuzywany w calej sesji testowej."""
    auth = AuthService()
    response = auth.login(AGENT_USER, AGENT_PASS)
    assert response.status_code == 200, "Nie udalo sie pobrac tokenu API"
    return response.json()["token"]
