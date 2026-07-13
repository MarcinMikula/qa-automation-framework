"""Base Service Object Model client for external/API-facing tests.

`BaseClient` is the generic SOM counterpart to `BasePage`.

It returns raw `httpx.Response` objects so higher-level service objects can
choose how much parsing, validation, or assertion responsibility they own.
"""

from __future__ import annotations

from typing import Any

import httpx

from testdata.settings import API_BASE_URL, API_TIMEOUT


class BaseClient:
    """Small synchronous HTTP client used by generic Service Objects."""

    def __init__(
        self,
        token: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.base_url = (base_url or API_BASE_URL).rstrip("/")
        self.timeout = timeout or API_TIMEOUT
        self.headers = {"Content-Type": "application/json"}

        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def _url(self, endpoint: str) -> str:
        """Build a full URL from the configured base URL and endpoint path."""
        normalized_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        return f"{self.base_url}{normalized_endpoint}"

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """Send a GET request and return the raw response."""
        with httpx.Client(timeout=self.timeout) as client:
            return client.get(
                self._url(endpoint),
                headers=self.headers,
                params=params,
            )

    def post(self, endpoint: str, payload: dict[str, Any]) -> httpx.Response:
        """Send a POST request and return the raw response."""
        with httpx.Client(timeout=self.timeout) as client:
            return client.post(
                self._url(endpoint),
                headers=self.headers,
                json=payload,
            )

    def put(self, endpoint: str, payload: dict[str, Any]) -> httpx.Response:
        """Send a PUT request and return the raw response."""
        with httpx.Client(timeout=self.timeout) as client:
            return client.put(
                self._url(endpoint),
                headers=self.headers,
                json=payload,
            )

    def patch(self, endpoint: str, payload: dict[str, Any]) -> httpx.Response:
        """Send a PATCH request and return the raw response."""
        with httpx.Client(timeout=self.timeout) as client:
            return client.patch(
                self._url(endpoint),
                headers=self.headers,
                json=payload,
            )

    def delete(self, endpoint: str) -> httpx.Response:
        """Send a DELETE request and return the raw response."""
        with httpx.Client(timeout=self.timeout) as client:
            return client.delete(
                self._url(endpoint),
                headers=self.headers,
            )
