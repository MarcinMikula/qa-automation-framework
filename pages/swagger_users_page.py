"""
swagger_users_page.py
[DOMAIN: GENERIC] Page Object dla Swagger UI — warstwa UI testów E2E.
Działa z każdym serwisem FastAPI który generuje /docs.
"""
from playwright.sync_api import Page


class SwaggerUsersPage:
    """
    [DOMAIN: GENERIC] Page Object dla Swagger UI serwisu users.
    Abstrakcja nad UI Swaggera — test nie zna lokatorów, tylko metody biznesowe.
    """

    # --- Lokatory -----------------------------------------------------------
    # [DOMAIN: GENERIC] — Swagger UI generuje te same klasy dla każdego serwisu
    GET_USERS_SECTION = "#operations-users-list_items_users_get div"
    EXECUTE_BUTTON = ".execute-wrapper"
    POST_USERS_BUTTON = "button[name='POST /users Create Item']"

    def __init__(self, page: Page):
        self.page = page

    # --- Akcje --------------------------------------------------------------

    def open(self, url: str = "http://localhost:8001/docs") -> None:
        """Otwiera Swagger UI serwisu users."""
        self.page.goto(url)

    def execute_get_users(self) -> None:
        """
        [DOMAIN: GENERIC] Rozwija sekcję GET /users i wykonuje zapytanie
        przez przycisk Try it out → Execute.
        """
        self.page.locator(self.GET_USERS_SECTION).filter(
            has_text="GET/usersList Items"
        ).click()
        self.page.locator("div").filter(has_text="Parameters").first.click()
        self.page.locator(self.EXECUTE_BUTTON).click()

    def execute_post_user(self) -> None:
        """
        [DOMAIN: GENERIC] Rozwija sekcję POST /users i wykonuje zapytanie
        z domyślnym body.
        """
        self.page.get_by_role("button", name="POST /users Create Item").click()
        self.page.locator("div").filter(has_text="Parameters").nth(2).click()
        self.page.locator(self.EXECUTE_BUTTON).click()

    def get_response_body(self) -> str:
        """
        [DOMAIN: GENERIC] Zwraca treść ostatniej odpowiedzi z sekcji Responses.
        """
        return self.page.locator(".responses-wrapper").inner_text()