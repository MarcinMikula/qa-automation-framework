"""Service Object Model for the local products service."""

from __future__ import annotations

from pydantic import BaseModel, Field

from api.microservice_client import MicroserviceClient
from testdata.settings import PRODUCTS_BASE_URL


class ProductCreate(BaseModel):
    """Payload used to create a product."""

    name: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    category: str | None = None
    description: str | None = None


class ProductUpdate(BaseModel):
    """Partial payload used to update a product."""

    name: str | None = Field(None, min_length=1)
    sku: str | None = Field(None, min_length=1)
    price: float | None = Field(None, ge=0)
    category: str | None = None
    description: str | None = None


class ProductResponse(BaseModel):
    """Typed products-service response."""

    id: int
    name: str
    sku: str
    price: float
    category: str | None = None
    description: str | None = None


class HealthResponse(BaseModel):
    """Typed health-check response."""

    status: str
    service: str
    port: int
    items_count: int = Field(..., ge=0)


class ProductService(MicroserviceClient):
    """Business-readable adapter for the local products API."""

    ENDPOINT_PRODUCTS = "/products"
    ENDPOINT_HEALTH = "/health"

    def __init__(self, base_url: str | None = None) -> None:
        super().__init__(base_url or PRODUCTS_BASE_URL)

    def get_all(self) -> list[ProductResponse]:
        data = self._get(self.ENDPOINT_PRODUCTS)
        return [ProductResponse(**item) for item in data]

    def get(self, product_id: int) -> ProductResponse:
        data = self._get(f"{self.ENDPOINT_PRODUCTS}/{product_id}")
        return ProductResponse(**data)

    def create(self, payload: ProductCreate | dict) -> ProductResponse:
        body = (
            payload.model_dump(exclude_unset=True)
            if isinstance(payload, BaseModel)
            else payload
        )
        data = self._post(self.ENDPOINT_PRODUCTS, body)
        return ProductResponse(**data)

    def update(
        self,
        product_id: int,
        payload: ProductUpdate | dict,
    ) -> ProductResponse:
        body = (
            payload.model_dump(exclude_unset=True)
            if isinstance(payload, BaseModel)
            else payload
        )
        data = self._put(f"{self.ENDPOINT_PRODUCTS}/{product_id}", body)
        return ProductResponse(**data)

    def delete(self, product_id: int) -> None:
        self._delete(f"{self.ENDPOINT_PRODUCTS}/{product_id}")

    def health_check(self) -> HealthResponse:
        data = self._get(self.ENDPOINT_HEALTH)
        return HealthResponse(**data)
