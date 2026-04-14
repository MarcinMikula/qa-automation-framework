"""
login_page.py
Page Object dla strony logowania TelcoBilling Portal.
Role: AGENT, SUPERVISOR, ADMIN — kazda z roznymi uprawnieniami.
"""
from pages.base_page import BasePage
from testdata.settings import BASE_URL


class LoginPage(BasePage):
    URL = f"{BASE_URL}/login"

    # Selektory
    INPUT_USERNAME = "[data-testid='username']"
    INPUT_PASSWORD = "[data-testid='password']"
    BTN_LOGIN = "[data-testid='btn-login']"
    MSG_ERROR = "[data-testid='login-error']"

    def open(self):
        self.navigate(self.URL)

    def login(self, username: str, password: str):
        self.fill(self.INPUT_USERNAME, username)
        self.fill(self.INPUT_PASSWORD, password)
        self.click(self.BTN_LOGIN)

    def get_error_message(self) -> str:
        return self.get_text(self.MSG_ERROR)
