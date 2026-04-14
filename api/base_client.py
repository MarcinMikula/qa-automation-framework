"""
base_client.py
Bazowa klasa Service Object Model (SOM) — analog BasePage dla warstwy API.
Uzywa httpx dla synchronicznych wywolan REST.
"""
import httpx
from testdata.settings import API_BASE_URL, API_TIMEOUT


class BaseClient:
    def __init__(self, token: str = None):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.headers = {"Content-Type": "application/json"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get(self, endpoint: str, params: dict = None) -> httpx.Response:
        with httpx.Client(timeout=self.timeout) as client:
            return client.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=params
            )

    def post(self, endpoint: str, payload: dict) -> httpx.Response:
        with httpx.Client(timeout=self.timeout) as client:
            return client.post(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                json=payload
            )

    def patch(self, endpoint: str, payload: dict) -> httpx.Response:
        with httpx.Client(timeout=self.timeout) as client:
            return client.patch(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                json=payload
            )
