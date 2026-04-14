"""
dashboard_page.py
Page Object dla dashboardu agenta — przeglad konta klienta.
Zawiera: wyszukiwarke klientow po MSISDN, status konta, faktury.
"""
from pages.base_page import BasePage
from testdata.settings import BASE_URL


class DashboardPage(BasePage):
    URL = f"{BASE_URL}/dashboard"

    # Selektory
    INPUT_MSISDN_SEARCH = "[data-testid='msisdn-search']"
    BTN_SEARCH = "[data-testid='btn-search']"
    LABEL_ACCOUNT_STATUS = "[data-testid='account-status']"
    LABEL_PLAN_NAME = "[data-testid='plan-name']"
    TABLE_INVOICES = "[data-testid='invoices-table']"
    LINK_SUPERVISOR_REPORTS = "[data-testid='supervisor-reports']"

    def search_customer(self, msisdn: str):
        self.fill(self.INPUT_MSISDN_SEARCH, msisdn)
        self.click(self.BTN_SEARCH)

    def get_account_status(self) -> str:
        return self.get_text(self.LABEL_ACCOUNT_STATUS)

    def get_plan_name(self) -> str:
        return self.get_text(self.LABEL_PLAN_NAME)

    def is_supervisor_reports_visible(self) -> bool:
        return self.is_visible(self.LINK_SUPERVISOR_REPORTS)
