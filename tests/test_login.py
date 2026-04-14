"""
test_login.py
Testy UI warstwy logowania — weryfikacja rol i scenariuszy negatywnych.
Kontekst: portal agentow telco, rozne poziomy uprawnien.
"""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from testdata.settings import AGENT_USER, AGENT_PASS, SUPERVISOR_USER, SUPERVISOR_PASS


class TestLogin:

    def test_agent_can_login_successfully(self, page):
        login = LoginPage(page)
        login.open()
        login.login(AGENT_USER, AGENT_PASS)
        login.wait_for_url("**/dashboard")
        dashboard = DashboardPage(page)
        assert dashboard.is_visible(dashboard.INPUT_MSISDN_SEARCH)

    def test_invalid_credentials_show_error(self, page):
        login = LoginPage(page)
        login.open()
        login.login("wrong_user", "wrong_pass")
        assert "Nieprawidlowy" in login.get_error_message()

    def test_agent_cannot_access_supervisor_reports(self, page):
        login = LoginPage(page)
        login.open()
        login.login(AGENT_USER, AGENT_PASS)
        login.wait_for_url("**/dashboard")
        dashboard = DashboardPage(page)
        assert not dashboard.is_supervisor_reports_visible()

    def test_supervisor_can_access_reports(self, page):
        login = LoginPage(page)
        login.open()
        login.login(SUPERVISOR_USER, SUPERVISOR_PASS)
        login.wait_for_url("**/dashboard")
        dashboard = DashboardPage(page)
        assert dashboard.is_supervisor_reports_visible()
