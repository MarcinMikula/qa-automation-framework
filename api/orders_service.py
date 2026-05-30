"""
orders_service.py
Service Object Model dla mikroserwisu orders (port 8002).
Kontekst: zamówienia z opcjonalną referencją billingową telco.
"""
from typing import Literal

from pydantic import BaseModel, Field

from api.microservice_client import MicroserviceClient
from testdata.settings import ORDERS_BASE_URL


# --- Modele Pydantic (zgodne z services/orders/main.py) -----------------------

class OrderCreate(BaseModel):
    # [DOMAIN: GENERIC]
    customer_id: int
    product_id: int
    quantity: int = 1
    total_amount: float
    status: Literal["NEW", "CONFIRMED", "SHIPPED", "CANCELLED"] = "NEW"

    # [DOMAIN: TELCO]
    invoice_reference: str | None = None


class OrderUpdate(BaseModel):
    # [DOMAIN: GENERIC]
    customer_id: int | None = None
    product_id: int | None = None
    quantity: int | None = None
    total_amount: float | None = None
    status: Literal["NEW", "CONFIRMED", "SHIPPED", "CANCELLED"] | None = None

    # [DOMAIN: TELCO]
    invoice_reference: str | None = None


class OrderResponse(BaseModel):
    id: int
    # [DOMAIN: GENERIC]
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: Literal["NEW", "CONFIRMED", "SHIPPED", "CANCELLED"]
    # [DOMAIN: TELCO]
    invoice_reference: str | None = None


class HealthResponse(BaseModel):
    """Odpowiedź endpointu /health."""
    status: str
    service: str
    port: int
    items_count: int = Field(..., description="Liczba rekordów w magazynie")


class OrderService(MicroserviceClient):
    """Klient HTTP dla mikroserwisu orders."""

    ENDPOINT_ORDERS = "/orders"
    ENDPOINT_HEALTH = "/health"

    def __init__(self, base_url: str | None = None):
        super().__init__(base_url or ORDERS_BASE_URL)

    def get_all(self) -> list[OrderResponse]:
        """Pobiera listę wszystkich zamówień."""
        data = self._get(self.ENDPOINT_ORDERS)
        return [OrderResponse(**item) for item in data]

    def get(self, order_id: int) -> OrderResponse:
        """Pobiera jedno zamówienie po ID."""
        data = self._get(f"{self.ENDPOINT_ORDERS}/{order_id}")
        return OrderResponse(**data)

    def create(self, payload: OrderCreate | dict) -> OrderResponse:
        """Tworzy nowe zamówienie."""
        body = payload.model_dump(exclude_unset=True) if isinstance(payload, BaseModel) else payload
        data = self._post(self.ENDPOINT_ORDERS, body)
        return OrderResponse(**data)

    def update(self, order_id: int, payload: OrderUpdate | dict) -> OrderResponse:
        """Aktualizuje zamówienie (PUT)."""
        body = payload.model_dump(exclude_unset=True) if isinstance(payload, BaseModel) else payload
        data = self._put(f"{self.ENDPOINT_ORDERS}/{order_id}", body)
        return OrderResponse(**data)

    def delete(self, order_id: int) -> None:
        """Usuwa zamówienie po ID."""
        self._delete(f"{self.ENDPOINT_ORDERS}/{order_id}")

    def health_check(self) -> HealthResponse:
        """Sprawdza żywotność mikroserwisu orders."""
        data = self._get(self.ENDPOINT_HEALTH)
        return HealthResponse(**data)
