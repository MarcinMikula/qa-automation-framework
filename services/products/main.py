"""
products/main.py
Mikroserwis produktów — port 8003.

Uruchomienie:
    python -m services.products.main
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field

from services.common.crud import create_crud_router
from services.common.store import InMemoryStore

PORT = 8003
SERVICE_NAME = "products"

app = FastAPI(
    title="Products Service",
    description="Mikroserwis katalogu produktów",
    version="1.0.0",
)

store = InMemoryStore()


# --- Modele Pydantic ----------------------------------------------------------

class ProductBase(BaseModel):
    # [DOMAIN: GENERIC] — uniwersalny katalog produktów
    name: str = Field(..., description="Nazwa produktu")
    sku: str = Field(..., description="Kod SKU")
    price: float = Field(..., ge=0, description="Cena jednostkowa")
    category: str | None = Field(None, description="Kategoria produktu")
    description: str | None = Field(None, description="Opis produktu")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    # [DOMAIN: GENERIC]
    name: str | None = None
    sku: str | None = None
    price: float | None = Field(None, ge=0)
    category: str | None = None
    description: str | None = None


class ProductResponse(ProductBase):
    id: int


def _to_response(data: dict) -> ProductResponse:
    return ProductResponse(**data)


# --- Router CRUD --------------------------------------------------------------

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
    """Sprawdzenie żywotności serwisu."""
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "port": PORT,
        "items_count": store.count(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.products.main:app", host="0.0.0.0", port=PORT, reload=False)
