"""
test_orders_api.py
Testy integracyjne OrderService — mikroserwis orders (port 8002).

Uruchomienie:
    pytest tests/integration/test_orders_api.py -v
"""
import httpx
import pytest

from api.orders_service import OrderCreate, OrderService, OrderUpdate


class TestOrderServiceHealth:
    """Testy endpointu /health."""

    def test_health_check_returns_ok(self, order_service: OrderService):
        """health_check zwraca status ok i nazwę serwisu orders."""
        health = order_service.health_check()

        assert health.status == "ok"
        assert health.service == "orders"
        assert health.port == 8002


class TestOrderServiceCrud:
    """[DOMAIN: GENERIC] Testy pełnego cyklu CRUD przez SOM."""

    def test_create_returns_order_with_id(self, clean_orders, order_service: OrderService):
        """create dodaje zamówienie i zwraca model z nadanym id."""
        order = order_service.create(
            OrderCreate(customer_id=1, product_id=1, total_amount=129.99)
        )

        assert order.id > 0
        assert order.customer_id == 1
        assert order.product_id == 1
        assert order.total_amount == 129.99
        assert order.status == "NEW"
        assert len(order_service.get_all()) == 1

    def test_get_returns_existing_order(self, clean_orders, order_service: OrderService):
        """get pobiera zamówienie po id."""
        created = order_service.create(
            OrderCreate(customer_id=2, product_id=3, total_amount=49.99, quantity=2)
        )

        fetched = order_service.get(created.id)

        assert fetched.id == created.id
        assert fetched.quantity == 2

    def test_get_all_returns_all_orders(self, clean_orders, order_service: OrderService):
        """get_all zwraca listę wszystkich zamówień."""
        order_service.create(
            OrderCreate(customer_id=1, product_id=1, total_amount=100.0)
        )
        order_service.create(
            OrderCreate(customer_id=2, product_id=2, total_amount=200.0)
        )

        orders = order_service.get_all()

        assert len(orders) == 2
        amounts = {o.total_amount for o in orders}
        assert amounts == {100.0, 200.0}

    def test_update_changes_order_fields(self, clean_orders, order_service: OrderService):
        """update modyfikuje pola zamówienia (PUT)."""
        created = order_service.create(
            OrderCreate(
                customer_id=1,
                product_id=1,
                total_amount=129.99,
                status="NEW",
            )
        )

        updated = order_service.update(
            created.id,
            OrderUpdate(status="CONFIRMED", total_amount=139.99),
        )

        assert updated.status == "CONFIRMED"
        assert updated.total_amount == 139.99
        assert updated.customer_id == 1

    def test_delete_removes_order(self, clean_orders, order_service: OrderService):
        """delete usuwa zamówienie — get_all jest puste po usunięciu."""
        created = order_service.create(
            OrderCreate(customer_id=9, product_id=9, total_amount=9.99)
        )

        order_service.delete(created.id)

        assert order_service.get_all() == []


class TestOrderServiceNegative:
    """[DOMAIN: GENERIC] Scenariusze negatywne — nieistniejące zasoby."""

    def test_get_nonexistent_id_raises_404(self, clean_orders, order_service: OrderService):
        """get nieistniejącego id zwraca HTTP 404."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            order_service.get(9999)

        assert exc_info.value.response.status_code == 404

    def test_delete_nonexistent_id_raises_404(self, clean_orders, order_service: OrderService):
        """delete nieistniejącego id zwraca HTTP 404."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            order_service.delete(9999)

        assert exc_info.value.response.status_code == 404


class TestTelcoOrderProfiles:
    """[DOMAIN: TELCO] Zamówienia z referencją billingową i różnymi statusami."""

    @pytest.mark.parametrize(
        "customer_id,product_id,quantity,total_amount,status,invoice_reference",
        [
            (1, 1, 1, 129.99, "NEW", None),
            (1, 2, 1, 129.99, "CONFIRMED", "INV-2025-08-001"),
            (3, 1, 2, 259.98, "SHIPPED", "INV-2025-07-015"),
            (3, 3, 1, 249.99, "CANCELLED", "INV-2025-06-099"),
        ],
        ids=["new_no_invoice", "confirmed_with_invoice", "shipped_billing_ref", "cancelled_overdue"],
    )
    def test_create_telco_order_profile(
        self,
        clean_orders,
        order_service: OrderService,
        customer_id: int,
        product_id: int,
        quantity: int,
        total_amount: float,
        status: str,
        invoice_reference: str | None,
    ):
        """[DOMAIN: TELCO] Tworzenie zamówienia ze statusem i opcjonalną referencją faktury."""
        order = order_service.create(
            OrderCreate(
                customer_id=customer_id,
                product_id=product_id,
                quantity=quantity,
                total_amount=total_amount,
                status=status,
                invoice_reference=invoice_reference,
            )
        )

        assert order.customer_id == customer_id
        assert order.product_id == product_id
        assert order.quantity == quantity
        assert order.total_amount == total_amount
        assert order.status == status
        assert order.invoice_reference == invoice_reference

        fetched = order_service.get(order.id)
        assert fetched.invoice_reference == invoice_reference
