"""Deterministic local orders service used by SOM examples."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from services.common.crud import create_crud_router
from services.common.store import InMemoryStore


PORT = 8002
SERVICE_NAME = "orders"
OrderStatus = Literal["NEW", "CONFIRMED", "COMPLETED", "CANCELLED"]

app = FastAPI(
    title="Orders Service",
    description="Domain-neutral local orders service for framework tests",
    version="1.0.0",
)

store = InMemoryStore()


class OrderBase(BaseModel):
    """Fields shared by create and response models."""

    user_id: int = Field(..., ge=1)
    product_id: int = Field(..., ge=1)
    quantity: int = Field(1, ge=1)
    total_amount: float = Field(..., ge=0)
    status: OrderStatus = "NEW"
    external_reference: str | None = None


class OrderCreate(OrderBase):
    """Create-order payload."""


class OrderUpdate(BaseModel):
    """Partial update-order payload."""

    user_id: int | None = Field(None, ge=1)
    product_id: int | None = Field(None, ge=1)
    quantity: int | None = Field(None, ge=1)
    total_amount: float | None = Field(None, ge=0)
    status: OrderStatus | None = None
    external_reference: str | None = None


class OrderResponse(OrderBase):
    """Orders-service response."""

    id: int


def _to_response(data: dict) -> OrderResponse:
    return OrderResponse(**data)


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
        "services.orders.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
    )
