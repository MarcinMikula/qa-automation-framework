"""
navbar.py
Komponent nawigacji — wydzielony zgodnie z zasada pojedynczej odpowiedzialnosci.
Reuzywalny we wszystkich page objects gdzie navbar jest obecny.
"""
from pages.base_page import BasePage


class Navbar(BasePage):
    LINK_DASHBOARD = "[data-testid='nav-dashboard']"
    LINK_REPORTS = "[data-testid='nav-reports']"
    BTN_LOGOUT = "[data-testid='nav-logout']"
    LABEL_LOGGED_USER = "[data-testid='nav-username']"

    def logout(self):
        self.click(self.BTN_LOGOUT)

    def get_logged_user(self) -> str:
        return self.get_text(self.LABEL_LOGGED_USER)

    def go_to_dashboard(self):
        self.click(self.LINK_DASHBOARD)
