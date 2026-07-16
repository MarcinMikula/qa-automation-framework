"""Deterministic local users service used by SOM examples."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from services.common.crud import create_crud_router
from services.common.store import InMemoryStore


PORT = 8001
SERVICE_NAME = "users"
UserStatus = Literal["ACTIVE", "INACTIVE", "SUSPENDED"]

app = FastAPI(
    title="Users Service",
    description="Domain-neutral local users service for framework tests",
    version="1.0.0",
)

store = InMemoryStore()


class UserBase(BaseModel):
    """Fields shared by create and response models."""

    full_name: str = Field(..., min_length=1)
    external_id: str = Field(..., min_length=1)
    email: str | None = None
    status: UserStatus = "ACTIVE"


class UserCreate(UserBase):
    """Create-user payload."""


class UserUpdate(BaseModel):
    """Partial update-user payload."""

    full_name: str | None = Field(None, min_length=1)
    external_id: str | None = Field(None, min_length=1)
    email: str | None = None
    status: UserStatus | None = None


class UserResponse(UserBase):
    """Users-service response."""

    id: int


def _to_response(data: dict) -> UserResponse:
    return UserResponse(**data)


app.include_router(
    create_crud_router(
        prefix="/users",
        tag="users",
        store=store,
        create_model=UserCreate,
        update_model=UserUpdate,
        response_model=UserResponse,
        to_response=_to_response,
    )
)


@app.get("/health")
def health() -> dict:
    """Return deterministic service health information."""
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "port": PORT,
        "items_count": store.count(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "services.users.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
    )
