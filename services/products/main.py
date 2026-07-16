"""Deterministic local products service used by SOM examples."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from services.common.crud import create_crud_router
from services.common.store import InMemoryStore


PORT = 8003
SERVICE_NAME = "products"

app = FastAPI(
    title="Products Service",
    description="Domain-neutral local product catalog for framework tests",
    version="1.0.0",
)

store = InMemoryStore()


class ProductBase(BaseModel):
    """Fields shared by create and response models."""

    name: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    category: str | None = None
    description: str | None = None


class ProductCreate(ProductBase):
    """Create-product payload."""


class ProductUpdate(BaseModel):
    """Partial update-product payload."""

    name: str | None = Field(None, min_length=1)
    sku: str | None = Field(None, min_length=1)
    price: float | None = Field(None, ge=0)
    category: str | None = None
    description: str | None = None


class ProductResponse(ProductBase):
    """Products-service response."""

    id: int


def _to_response(data: dict) -> ProductResponse:
    return ProductResponse(**data)


app.include_router(
    create_crud_router(
        prefix="/products",
        tag="products",
        store=store,
        create_model=ProductCreate,
        update_model=ProductUpdate,
        response_model=ProductResponse,
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
        "services.products.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
    )
