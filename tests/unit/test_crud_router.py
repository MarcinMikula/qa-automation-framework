"""Unit tests for the reusable FastAPI CRUD router factory."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from services.common.crud import create_crud_router
from services.common.store import InMemoryStore


class DemoCreate(BaseModel):
    name: str
    status: str = "NEW"


class DemoUpdate(BaseModel):
    name: str | None = None
    status: str | None = None


class DemoResponse(BaseModel):
    id: int
    name: str
    status: str


def to_response(data: dict) -> DemoResponse:
    return DemoResponse(**data)


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    store = InMemoryStore()
    app.include_router(
        create_crud_router(
            prefix="/demo",
            tag="demo",
            store=store,
            create_model=DemoCreate,
            update_model=DemoUpdate,
            response_model=DemoResponse,
            to_response=to_response,
        )
    )
    return TestClient(app)


class TestCrudRouterHappyPath:
    def test_post_creates_item_with_id(self, client):
        response = client.post("/demo", json={"name": "First"})

        assert response.status_code == 201
        assert response.json() == {"id": 1, "name": "First", "status": "NEW"}

    def test_get_list_returns_created_items(self, client):
        client.post("/demo", json={"name": "First"})
        client.post("/demo", json={"name": "Second", "status": "ACTIVE"})

        response = client.get("/demo")

        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "name": "First", "status": "NEW"},
            {"id": 2, "name": "Second", "status": "ACTIVE"},
        ]

    def test_get_single_returns_item(self, client):
        created = client.post("/demo", json={"name": "First"}).json()

        response = client.get(f"/demo/{created['id']}")

        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "First", "status": "NEW"}

    def test_put_updates_existing_item(self, client):
        created = client.post("/demo", json={"name": "First", "status": "NEW"}).json()

        response = client.put(f"/demo/{created['id']}", json={"status": "DONE"})

        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "First", "status": "DONE"}

    def test_delete_removes_existing_item(self, client):
        created = client.post("/demo", json={"name": "First"}).json()

        response = client.delete(f"/demo/{created['id']}")

        assert response.status_code == 204
        assert client.get(f"/demo/{created['id']}").status_code == 404


class TestCrudRouterErrors:
    def test_get_missing_item_returns_404(self, client):
        response = client.get("/demo/999")

        assert response.status_code == 404
        assert "demo o id=999 nie istnieje" in response.json()["detail"]

    def test_put_missing_item_returns_404(self, client):
        response = client.put("/demo/999", json={"name": "Updated"})

        assert response.status_code == 404
        assert "demo o id=999 nie istnieje" in response.json()["detail"]

    def test_delete_missing_item_returns_404(self, client):
        response = client.delete("/demo/999")

        assert response.status_code == 404
        assert "demo o id=999 nie istnieje" in response.json()["detail"]

    def test_post_invalid_payload_returns_422(self, client):
        response = client.post("/demo", json={"status": "NEW"})

        assert response.status_code == 422
