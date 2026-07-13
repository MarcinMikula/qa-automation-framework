"""Unit tests for the generic BaseClient SOM helper."""

from unittest.mock import Mock

import httpx

from api.base_client import BaseClient


class DummyHttpClient:
    def __init__(self, response: httpx.Response):
        self.response = response
        self.calls: list[tuple[str, str, dict | None, dict | None]] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def get(self, url: str, headers: dict, params: dict | None = None):
        self.calls.append(("GET", url, None, params))
        return self.response

    def post(self, url: str, headers: dict, json: dict):
        self.calls.append(("POST", url, json, None))
        return self.response

    def put(self, url: str, headers: dict, json: dict):
        self.calls.append(("PUT", url, json, None))
        return self.response

    def patch(self, url: str, headers: dict, json: dict):
        self.calls.append(("PATCH", url, json, None))
        return self.response

    def delete(self, url: str, headers: dict):
        self.calls.append(("DELETE", url, None, None))
        return self.response


def make_response(status_code: int = 200, json_data=None) -> httpx.Response:
    request = httpx.Request("GET", "http://api.local/items")
    return httpx.Response(status_code=status_code, json=json_data or {}, request=request)


class TestBaseClientConfiguration:
    def test_custom_base_url_is_trimmed(self):
        client = BaseClient(base_url="http://api.local/")

        assert client.base_url == "http://api.local"
        assert client._url("/items") == "http://api.local/items"

    def test_endpoint_without_leading_slash_is_supported(self):
        client = BaseClient(base_url="http://api.local")

        assert client._url("items") == "http://api.local/items"

    def test_token_adds_authorization_header(self):
        client = BaseClient(token="abc123", base_url="http://api.local")

        assert client.headers["Authorization"] == "Bearer abc123"
        assert client.headers["Content-Type"] == "application/json"


class TestBaseClientHttpMethods:
    def test_get_sends_query_params_and_returns_raw_response(self, monkeypatch):
        response = make_response(200, {"items": []})
        dummy = DummyHttpClient(response)
        monkeypatch.setattr("api.base_client.httpx.Client", Mock(return_value=dummy))

        client = BaseClient(base_url="http://api.local")
        result = client.get("/items", params={"page": 1})

        assert result is response
        assert dummy.calls == [("GET", "http://api.local/items", None, {"page": 1})]

    def test_post_sends_json_payload(self, monkeypatch):
        response = make_response(201, {"id": 1})
        dummy = DummyHttpClient(response)
        monkeypatch.setattr("api.base_client.httpx.Client", Mock(return_value=dummy))

        client = BaseClient(base_url="http://api.local")
        result = client.post("/items", {"name": "Created"})

        assert result is response
        assert dummy.calls == [("POST", "http://api.local/items", {"name": "Created"}, None)]

    def test_put_sends_json_payload(self, monkeypatch):
        response = make_response(200, {"id": 1})
        dummy = DummyHttpClient(response)
        monkeypatch.setattr("api.base_client.httpx.Client", Mock(return_value=dummy))

        client = BaseClient(base_url="http://api.local")
        result = client.put("/items/1", {"name": "Updated"})

        assert result is response
        assert dummy.calls == [("PUT", "http://api.local/items/1", {"name": "Updated"}, None)]

    def test_patch_sends_json_payload(self, monkeypatch):
        response = make_response(200, {"id": 1})
        dummy = DummyHttpClient(response)
        monkeypatch.setattr("api.base_client.httpx.Client", Mock(return_value=dummy))

        client = BaseClient(base_url="http://api.local")
        result = client.patch("/items/1", {"status": "ACTIVE"})

        assert result is response
        assert dummy.calls == [("PATCH", "http://api.local/items/1", {"status": "ACTIVE"}, None)]

    def test_delete_returns_raw_response(self, monkeypatch):
        response = make_response(204)
        dummy = DummyHttpClient(response)
        monkeypatch.setattr("api.base_client.httpx.Client", Mock(return_value=dummy))

        client = BaseClient(base_url="http://api.local")
        result = client.delete("/items/1")

        assert result is response
        assert dummy.calls == [("DELETE", "http://api.local/items/1", None, None)]
