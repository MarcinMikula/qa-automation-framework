"""Unit tests for the reusable HTTP microservice client."""

from unittest.mock import Mock

import httpx
import pytest

from api.microservice_client import MicroserviceClient


class DummyHttpClient:
    def __init__(self, response: httpx.Response):
        self.response = response
        self.calls: list[tuple[str, str, dict | None]] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def get(self, url: str, headers: dict):
        self.calls.append(("GET", url, None))
        return self.response

    def post(self, url: str, headers: dict, json: dict):
        self.calls.append(("POST", url, json))
        return self.response

    def put(self, url: str, headers: dict, json: dict):
        self.calls.append(("PUT", url, json))
        return self.response

    def delete(self, url: str, headers: dict):
        self.calls.append(("DELETE", url, None))
        return self.response


def make_response(status_code: int, json_data=None) -> httpx.Response:
    request = httpx.Request("GET", "http://service.local/items")
    if status_code == 204:
        return httpx.Response(status_code=status_code, request=request)

    return httpx.Response(status_code=status_code, json=json_data, request=request)


class TestMicroserviceClientUrl:
    def test_base_url_trailing_slash_is_removed(self):
        client = MicroserviceClient("http://service.local/")

        assert client.base_url == "http://service.local"
        assert client._url("/items") == "http://service.local/items"


class TestMicroserviceClientParsing:
    def test_parse_returns_json_for_success_response(self):
        client = MicroserviceClient("http://service.local")
        response = make_response(200, {"id": 1})

        assert client._parse(response) == {"id": 1}

    def test_parse_returns_none_for_204_response(self):
        client = MicroserviceClient("http://service.local")
        response = make_response(204)

        assert client._parse(response) is None

    def test_parse_raises_for_error_response(self):
        client = MicroserviceClient("http://service.local")
        response = make_response(404, {"detail": "missing"})

        with pytest.raises(httpx.HTTPStatusError):
            client._parse(response)


class TestMicroserviceClientHttpVerbs:
    def test_get_uses_configured_base_url(self, monkeypatch):
        dummy = DummyHttpClient(make_response(200, [{"id": 1}]))
        monkeypatch.setattr("api.microservice_client.httpx.Client", Mock(return_value=dummy))

        client = MicroserviceClient("http://service.local")

        assert client._get("/items") == [{"id": 1}]
        assert dummy.calls == [("GET", "http://service.local/items", None)]

    def test_post_sends_json_payload(self, monkeypatch):
        dummy = DummyHttpClient(make_response(201, {"id": 1, "name": "Created"}))
        monkeypatch.setattr("api.microservice_client.httpx.Client", Mock(return_value=dummy))

        client = MicroserviceClient("http://service.local")

        assert client._post("/items", {"name": "Created"}) == {"id": 1, "name": "Created"}
        assert dummy.calls == [("POST", "http://service.local/items", {"name": "Created"})]

    def test_put_sends_json_payload(self, monkeypatch):
        dummy = DummyHttpClient(make_response(200, {"id": 1, "name": "Updated"}))
        monkeypatch.setattr("api.microservice_client.httpx.Client", Mock(return_value=dummy))

        client = MicroserviceClient("http://service.local")

        assert client._put("/items/1", {"name": "Updated"}) == {"id": 1, "name": "Updated"}
        assert dummy.calls == [("PUT", "http://service.local/items/1", {"name": "Updated"})]

    def test_delete_returns_none_for_204_response(self, monkeypatch):
        dummy = DummyHttpClient(make_response(204))
        monkeypatch.setattr("api.microservice_client.httpx.Client", Mock(return_value=dummy))

        client = MicroserviceClient("http://service.local")

        assert client._delete("/items/1") is None
        assert dummy.calls == [("DELETE", "http://service.local/items/1", None)]
