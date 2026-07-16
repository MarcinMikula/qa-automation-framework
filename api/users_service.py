"""Service Object Model for the local users service."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from api.microservice_client import MicroserviceClient
from testdata.settings import USERS_BASE_URL


UserStatus = Literal["ACTIVE", "INACTIVE", "SUSPENDED"]


class UserCreate(BaseModel):
    """Payload used to create a user."""

    full_name: str = Field(..., min_length=1)
    external_id: str = Field(..., min_length=1)
    email: str | None = None
    status: UserStatus = "ACTIVE"


class UserUpdate(BaseModel):
    """Partial payload used to update a user."""

    full_name: str | None = Field(None, min_length=1)
    external_id: str | None = Field(None, min_length=1)
    email: str | None = None
    status: UserStatus | None = None


class UserResponse(BaseModel):
    """Typed users-service response."""

    id: int
    full_name: str
    external_id: str
    email: str | None = None
    status: UserStatus = "ACTIVE"


class HealthResponse(BaseModel):
    """Typed health-check response."""

    status: str
    service: str
    port: int
    items_count: int = Field(..., ge=0)


class UserService(MicroserviceClient):
    """Business-readable adapter for the local users API."""

    ENDPOINT_USERS = "/users"
    ENDPOINT_HEALTH = "/health"

    def __init__(self, base_url: str | None = None) -> None:
        super().__init__(base_url or USERS_BASE_URL)

    def get_all(self) -> list[UserResponse]:
        data = self._get(self.ENDPOINT_USERS)
        return [UserResponse(**item) for item in data]

    def get(self, user_id: int) -> UserResponse:
        data = self._get(f"{self.ENDPOINT_USERS}/{user_id}")
        return UserResponse(**data)

    def create(self, payload: UserCreate | dict) -> UserResponse:
        body = (
            payload.model_dump(exclude_unset=True)
            if isinstance(payload, BaseModel)
            else payload
        )
        data = self._post(self.ENDPOINT_USERS, body)
        return UserResponse(**data)

    def update(self, user_id: int, payload: UserUpdate | dict) -> UserResponse:
        body = (
            payload.model_dump(exclude_unset=True)
            if isinstance(payload, BaseModel)
            else payload
        )
        data = self._put(f"{self.ENDPOINT_USERS}/{user_id}", body)
        return UserResponse(**data)

    def delete(self, user_id: int) -> None:
        self._delete(f"{self.ENDPOINT_USERS}/{user_id}")

    def health_check(self) -> HealthResponse:
        data = self._get(self.ENDPOINT_HEALTH)
        return HealthResponse(**data)
