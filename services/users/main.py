"""
users/main.py
Mikroserwis użytkowników (klienci telco) — port 8001.

Uruchomienie:
    python -m services.users.main
"""
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from services.common.crud import create_crud_router
from services.common.store import InMemoryStore

PORT = 8001
SERVICE_NAME = "users"

app = FastAPI(
    title="Users Service",
    description="Mikroserwis użytkowników — kontekst telco/CRM",
    version="1.0.0",
)

store = InMemoryStore()


# --- Modele Pydantic ----------------------------------------------------------

class UserBase(BaseModel):
    # [DOMAIN: GENERIC] — uniwersalne pola użytkownika
    full_name: str = Field(..., description="Imię i nazwisko")
    email: str | None = Field(None, description="Adres e-mail")

    # [DOMAIN: TELCO] — pola specyficzne dla operatora / billingu
    msisdn: str = Field(..., description="Numer MSISDN (np. 48100200301)")
    contract_type: Literal["PREPAID", "POSTPAID"] | None = Field(
        None, description="Typ kontraktu"
    )
    plan: str | None = Field(None, description="Nazwa planu taryfowego")
    account_status: Literal["ACTIVE", "SUSPENDED"] = Field(
        "ACTIVE", description="Status konta abonenta"
    )


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    # [DOMAIN: GENERIC]
    full_name: str | None = None
    email: str | None = None

    # [DOMAIN: TELCO]
    msisdn: str | None = None
    contract_type: Literal["PREPAID", "POSTPAID"] | None = None
    plan: str | None = None
    account_status: Literal["ACTIVE", "SUSPENDED"] | None = None


class UserResponse(UserBase):
    id: int


def _to_response(data: dict) -> UserResponse:
    return UserResponse(**data)


# --- Router CRUD --------------------------------------------------------------

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
    """Sprawdzenie żywotności serwisu."""
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "port": PORT,
        "items_count": store.count(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.users.main:app", host="0.0.0.0", port=PORT, reload=False)
