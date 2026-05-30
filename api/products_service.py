"""
products_service.py
Service Object Model dla mikroserwisu products (port 8003).
Kontekst: uniwersalny katalog produktów.
"""
from pydantic import BaseModel, Field

from api.microservice_client import MicroserviceClient
from testdata.settings import PRODUCTS_BASE_URL


# --- Modele Pydantic (zgodne z services/products/main.py) ---------------------

class ProductCreate(BaseModel):
    # [DOMAIN: GENERIC]
    name: str
    sku: str
    price: float
    category: str | None = None
    description: str | None = None


class ProductUpdate(BaseModel):
    # [DOMAIN: GENERIC]
    name: str | None = None
    sku: str | None = None
    price: float | None = None
    category: str | None = None
    description: str | None = None


class ProductResponse(BaseModel):
    id: int
    # [DOMAIN: GENERIC]
    name: str
    sku: str
    price: float
    category: str | None = None
    description: str | None = None


class HealthResponse(BaseModel):
    """Odpowiedź endpointu /health."""
    status: str
    service: str
    port: int
    items_count: int = Field(..., description="Liczba rekordów w magazynie")


class ProductService(MicroserviceClient):
    """Klient HTTP dla mikroserwisu products."""

    ENDPOINT_PRODUCTS = "/products"
    ENDPOINT_HEALTH = "/health"

    def __init__(self, base_url: str | None = None):
        super().__init__(base_url or PRODUCTS_BASE_URL)

    def get_all(self) -> list[ProductResponse]:
        """Pobiera listę wszystkich produktów."""
        data = self._get(self.ENDPOINT_PRODUCTS)
        return [ProductResponse(**item) for item in data]

    def get(self, product_id: int) -> ProductResponse:
        """Pobiera jeden produkt po ID."""
        data = self._get(f"{self.ENDPOINT_PRODUCTS}/{product_id}")
        return ProductResponse(**data)

    def create(self, payload: ProductCreate | dict) -> ProductResponse:
        """Tworzy nowy produkt."""
        body = payload.model_dump(exclude_unset=True) if isinstance(payload, BaseModel) else payload
        data = self._post(self.ENDPOINT_PRODUCTS, body)
        return ProductResponse(**data)

    def update(self, product_id: int, payload: ProductUpdate | dict) -> ProductResponse:
        """Aktualizuje produkt (PUT)."""
        body = payload.model_dump(exclude_unset=True) if isinstance(payload, BaseModel) else payload
        data = self._put(f"{self.ENDPOINT_PRODUCTS}/{product_id}", body)
        return ProductResponse(**data)

    def delete(self, product_id: int) -> None:
        """Usuwa produkt po ID."""
        self._delete(f"{self.ENDPOINT_PRODUCTS}/{product_id}")

    def health_check(self) -> HealthResponse:
        """Sprawdza żywotność mikroserwisu products."""
        data = self._get(self.ENDPOINT_HEALTH)
        return HealthResponse(**data)
