"""Service Object Model for the local orders service."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from api.microservice_client import MicroserviceClient
from testdata.settings import ORDERS_BASE_URL


OrderStatus = Literal["NEW", "CONFIRMED", "COMPLETED", "CANCELLED"]


class OrderCreate(BaseModel):
    """Payload used to create an order."""

    user_id: int = Field(..., ge=1)
    product_id: int = Field(..., ge=1)
    quantity: int = Field(1, ge=1)
    total_amount: float = Field(..., ge=0)
    status: OrderStatus = "NEW"
    external_reference: str | None = None


class OrderUpdate(BaseModel):
    """Partial payload used to update an order."""

    user_id: int | None = Field(None, ge=1)
    product_id: int | None = Field(None, ge=1)
    quantity: int | None = Field(None, ge=1)
    total_amount: float | None = Field(None, ge=0)
    status: OrderStatus | None = None
    external_reference: str | None = None


class OrderResponse(BaseModel):
    """Typed orders-service response."""

    id: int
    user_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: OrderStatus
    external_reference: str | None = None


class HealthResponse(BaseModel):
    """Typed health-check response."""

    status: str
    service: str
    port: int
    items_count: int = Field(..., ge=0)


class OrderService(MicroserviceClient):
    """Business-readable adapter for the local orders API."""

    ENDPOINT_ORDERS = "/orders"
    ENDPOINT_HEALTH = "/health"

    def __init__(self, base_url: str | None = None) -> None:
        super().__init__(base_url or ORDERS_BASE_URL)

    def get_all(self) -> list[OrderResponse]:
        data = self._get(self.ENDPOINT_ORDERS)
        return [OrderResponse(**item) for item in data]

    def get(self, order_id: int) -> OrderResponse:
        data = self._get(f"{self.ENDPOINT_ORDERS}/{order_id}")
        return OrderResponse(**data)

    def create(self, payload: OrderCreate | dict) -> OrderResponse:
        body = (
            payload.model_dump(exclude_unset=True)
            if isinstance(payload, BaseModel)
            else payload
        )
        data = self._post(self.ENDPOINT_ORDERS, body)
        return OrderResponse(**data)

    def update(
        self,
        order_id: int,
        payload: OrderUpdate | dict,
    ) -> OrderResponse:
        body = (
            payload.model_dump(exclude_unset=True)
            if isinstance(payload, BaseModel)
            else payload
        )
        data = self._put(f"{self.ENDPOINT_ORDERS}/{order_id}", body)
        return OrderResponse(**data)

    def delete(self, order_id: int) -> None:
        self._delete(f"{self.ENDPOINT_ORDERS}/{order_id}")

    def health_check(self) -> HealthResponse:
        data = self._get(self.ENDPOINT_HEALTH)
        return HealthResponse(**data)
