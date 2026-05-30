"""
users_service.py
Service Object Model dla mikroserwisu users (port 8001).
Kontekst: klienci telco — CRUD użytkowników z polami MSISDN i planem.
"""
from typing import Literal

from pydantic import BaseModel, Field

from api.microservice_client import MicroserviceClient
from testdata.settings import USERS_BASE_URL


# --- Modele Pydantic (zgodne z services/users/main.py) ------------------------

class UserCreate(BaseModel):
    # [DOMAIN: GENERIC]
    full_name: str
    email: str | None = None

    # [DOMAIN: TELCO]
    msisdn: str
    contract_type: Literal["PREPAID", "POSTPAID"] | None = None
    plan: str | None = None
    account_status: Literal["ACTIVE", "SUSPENDED"] = "ACTIVE"


class UserUpdate(BaseModel):
    # [DOMAIN: GENERIC]
    full_name: str | None = None
    email: str | None = None

    # [DOMAIN: TELCO]
    msisdn: str | None = None
    contract_type: Literal["PREPAID", "POSTPAID"] | None = None
    plan: str | None = None
    account_status: Literal["ACTIVE", "SUSPENDED"] | None = None


class UserResponse(BaseModel):
    id: int
    # [DOMAIN: GENERIC]
    full_name: str
    email: str | None = None
    # [DOMAIN: TELCO]
    msisdn: str
    contract_type: Literal["PREPAID", "POSTPAID"] | None = None
    plan: str | None = None
    account_status: Literal["ACTIVE", "SUSPENDED"] = "ACTIVE"


class HealthResponse(BaseModel):
    """Odpowiedź endpointu /health."""
    status: str
    service: str
    port: int
    items_count: int = Field(..., description="Liczba rekordów w magazynie")


class UserService(MicroserviceClient):
    """Klient HTTP dla mikroserwisu users."""

    ENDPOINT_USERS = "/users"
    ENDPOINT_HEALTH = "/health"

    def __init__(self, base_url: str | None = None):
        super().__init__(base_url or USERS_BASE_URL)

    def get_all(self) -> list[UserResponse]:
        """Pobiera listę wszystkich użytkowników."""
        data = self._get(self.ENDPOINT_USERS)
        return [UserResponse(**item) for item in data]

    def get(self, user_id: int) -> UserResponse:
        """Pobiera jednego użytkownika po ID."""
        data = self._get(f"{self.ENDPOINT_USERS}/{user_id}")
        return UserResponse(**data)

    def create(self, payload: UserCreate | dict) -> UserResponse:
        """Tworzy nowego użytkownika."""
        body = payload.model_dump(exclude_unset=True) if isinstance(payload, BaseModel) else payload
        data = self._post(self.ENDPOINT_USERS, body)
        return UserResponse(**data)

    def update(self, user_id: int, payload: UserUpdate | dict) -> UserResponse:
        """Aktualizuje użytkownika (PUT)."""
        body = payload.model_dump(exclude_unset=True) if isinstance(payload, BaseModel) else payload
        data = self._put(f"{self.ENDPOINT_USERS}/{user_id}", body)
        return UserResponse(**data)

    def delete(self, user_id: int) -> None:
        """Usuwa użytkownika po ID."""
        self._delete(f"{self.ENDPOINT_USERS}/{user_id}")

    def health_check(self) -> HealthResponse:
        """Sprawdza żywotność mikroserwisu users."""
        data = self._get(self.ENDPOINT_HEALTH)
        return HealthResponse(**data)
