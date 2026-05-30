"""
microservice_client.py
[DOMAIN: GENERIC] Bazowy klient HTTP dla lokalnych mikroserwisów FastAPI.
Zwraca sparsowane dane (dict/list), nie surowe obiekty Response.
"""
import httpx
from testdata.settings import API_TIMEOUT


class MicroserviceClient:
    """Klient httpx z konfigurowalnym BASE_URL per mikroserwis."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.timeout = API_TIMEOUT
        self.headers = {"Content-Type": "application/json"}

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def _parse(self, response: httpx.Response) -> dict | list | None:
        response.raise_for_status()
        if response.status_code == 204:
            return None
        return response.json()

    def _get(self, endpoint: str) -> dict | list:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(self._url(endpoint), headers=self.headers)
        return self._parse(response)

    def _post(self, endpoint: str, payload: dict) -> dict:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                self._url(endpoint), headers=self.headers, json=payload
            )
        return self._parse(response)

    def _put(self, endpoint: str, payload: dict) -> dict:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.put(
                self._url(endpoint), headers=self.headers, json=payload
            )
        return self._parse(response)

    def _delete(self, endpoint: str) -> None:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.delete(self._url(endpoint), headers=self.headers)
        self._parse(response)
