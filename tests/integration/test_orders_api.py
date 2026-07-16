"""Integration tests for OrderService."""

import httpx
import pytest

from api.orders_service import OrderCreate, OrderService, OrderUpdate


class TestOrderServiceHealth:
    def test_health_check_returns_ok(
        self,
        order_service: OrderService,
    ) -> None:
        health = order_service.health_check()

        assert health.status == "ok"
        assert health.service == "orders"
        assert health.port == 8002


class TestOrderServiceCrud:
    def test_create_returns_order_with_id(
        self,
        clean_orders,
        order_service: OrderService,
    ) -> None:
        order = order_service.create(
            OrderCreate(
                user_id=1,
                product_id=1,
                total_amount=49.99,
            )
        )

        assert order.id > 0
        assert order.user_id == 1
        assert order.product_id == 1
        assert order.total_amount == 49.99
        assert order.status == "NEW"
        assert len(order_service.get_all()) == 1

    def test_get_returns_existing_order(
        self,
        clean_orders,
        order_service: OrderService,
    ) -> None:
        created = order_service.create(
            OrderCreate(
                user_id=2,
                product_id=3,
                total_amount=39.98,
                quantity=2,
            )
        )

        fetched = order_service.get(created.id)

        assert fetched.id == created.id
        assert fetched.quantity == 2

    def test_get_all_returns_all_orders(
        self,
        clean_orders,
        order_service: OrderService,
    ) -> None:
        order_service.create(
            OrderCreate(
                user_id=1,
                product_id=1,
                total_amount=100.0,
            )
        )
        order_service.create(
            OrderCreate(
                user_id=2,
                product_id=2,
                total_amount=200.0,
            )
        )

        orders = order_service.get_all()

        assert len(orders) == 2
        amounts = {order.total_amount for order in orders}
        assert amounts == {100.0, 200.0}

    def test_update_changes_order_fields(
        self,
        clean_orders,
        order_service: OrderService,
    ) -> None:
        created = order_service.create(
            OrderCreate(
                user_id=1,
                product_id=1,
                total_amount=49.99,
            )
        )

        updated = order_service.update(
            created.id,
            OrderUpdate(
                status="CONFIRMED",
                total_amount=59.99,
            ),
        )

        assert updated.status == "CONFIRMED"
        assert updated.total_amount == 59.99
        assert updated.user_id == 1

    def test_delete_removes_order(
        self,
        clean_orders,
        order_service: OrderService,
    ) -> None:
        created = order_service.create(
            OrderCreate(
                user_id=9,
                product_id=9,
                total_amount=9.99,
            )
        )

        order_service.delete(created.id)

        assert order_service.get_all() == []


class TestOrderServiceNegative:
    def test_get_nonexistent_id_raises_404(
        self,
        clean_orders,
        order_service: OrderService,
    ) -> None:
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            order_service.get(9999)

        assert exc_info.value.response.status_code == 404

    def test_delete_nonexistent_id_raises_404(
        self,
        clean_orders,
        order_service: OrderService,
    ) -> None:
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            order_service.delete(9999)

        assert exc_info.value.response.status_code == 404


class TestOrderPayloadVariants:
    @pytest.mark.parametrize(
        (
            "user_id,product_id,quantity,total_amount,"
            "status,external_reference"
        ),
        [
            (1, 1, 1, 49.99, "NEW", None),
            (
                1,
                2,
                1,
                99.99,
                "CONFIRMED",
                "EXT-ORDER-001",
            ),
            (
                3,
                1,
                2,
                39.98,
                "COMPLETED",
                "EXT-ORDER-002",
            ),
            (
                3,
                3,
                1,
                24.99,
                "CANCELLED",
                "EXT-ORDER-003",
            ),
        ],
        ids=[
            "new_without_reference",
            "confirmed_with_reference",
            "completed_with_reference",
            "cancelled_with_reference",
        ],
    )
    def test_create_order_payload_variant(
        self,
        clean_orders,
        order_service: OrderService,
        user_id: int,
        product_id: int,
        quantity: int,
        total_amount: float,
        status: str,
        external_reference: str | None,
    ) -> None:
        order = order_service.create(
            OrderCreate(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                total_amount=total_amount,
                status=status,
                external_reference=external_reference,
            )
        )

        assert order.user_id == user_id
        assert order.product_id == product_id
        assert order.quantity == quantity
        assert order.total_amount == total_amount
        assert order.status == status
        assert order.external_reference == external_reference

        fetched = order_service.get(order.id)
        assert fetched.external_reference == external_reference
