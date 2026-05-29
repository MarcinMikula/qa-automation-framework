"""
orders/main.py
Mikroserwis zamówień — port 8002.

Uruchomienie:
    python -m services.orders.main
"""
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from services.common.crud import create_crud_router
from services.common.store import InMemoryStore

PORT = 8002
SERVICE_NAME = "orders"

app = FastAPI(
    title="Orders Service",
    description="Mikroserwis zamówień — warstwa transakcyjna",
    version="1.0.0",
)

store = InMemoryStore()


# --- Modele Pydantic ----------------------------------------------------------

class OrderBase(BaseModel):
    # [DOMAIN: GENERIC] — standardowe pola zamówienia
    customer_id: int = Field(..., description="ID klienta (referencja do users)")
    product_id: int = Field(..., description="ID produktu (referencja do products)")
    quantity: int = Field(1, ge=1, description="Ilość sztuk")
    total_amount: float = Field(..., ge=0, description="Kwota zamówienia")
    status: Literal["NEW", "CONFIRMED", "SHIPPED", "CANCELLED"] = Field(
        "NEW", description="Status realizacji zamówienia"
    )

    # [DOMAIN: TELCO] — opcjonalny kontekst billingowy (np. numer faktury)
    invoice_reference: str | None = Field(
        None, description="[TELCO] Referencja do faktury w systemie billingowym"
    )


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    # [DOMAIN: GENERIC]
    customer_id: int | None = None
    product_id: int | None = None
    quantity: int | None = Field(None, ge=1)
    total_amount: float | None = Field(None, ge=0)
    status: Literal["NEW", "CONFIRMED", "SHIPPED", "CANCELLED"] | None = None

    # [DOMAIN: TELCO]
    invoice_reference: str | None = None


class OrderResponse(OrderBase):
    id: int


def _to_response(data: dict) -> OrderResponse:
    return OrderResponse(**data)


# --- Router CRUD --------------------------------------------------------------

app.include_router(
    create_crud_router(
        prefix="/orders",
        tag="orders",
        store=store,
        create_model=OrderCreate,
        update_model=OrderUpdate,
        response_model=OrderResponse,
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

    uvicorn.run("services.orders.main:app", host="0.0.0.0", port=PORT, reload=False)
