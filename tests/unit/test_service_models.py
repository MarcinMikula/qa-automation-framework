"""Unit tests for local microservice Pydantic models."""

import pytest
from pydantic import ValidationError

from services.orders.main import OrderCreate, OrderUpdate
from services.products.main import ProductCreate, ProductUpdate
from services.users.main import UserCreate, UserUpdate


class TestUserModels:
    def test_user_create_defaults_status_to_active(self) -> None:
        user = UserCreate(
            full_name="Alex Morgan",
            external_id="USR-001",
        )

        assert user.status == "ACTIVE"
        assert user.email is None

    def test_user_create_rejects_invalid_status(self) -> None:
        with pytest.raises(ValidationError):
            UserCreate(
                full_name="Alex Morgan",
                external_id="USR-001",
                status="BLOCKED",
            )

    def test_user_update_allows_partial_payload(self) -> None:
        update = UserUpdate(status="INACTIVE")

        assert update.model_dump(exclude_unset=True) == {
            "status": "INACTIVE"
        }


class TestOrderModels:
    def test_order_create_defaults_status_and_quantity(self) -> None:
        order = OrderCreate(
            user_id=1,
            product_id=10,
            total_amount=49.99,
        )

        assert order.quantity == 1
        assert order.status == "NEW"
        assert order.external_reference is None

    def test_order_create_rejects_zero_quantity(self) -> None:
        with pytest.raises(ValidationError):
            OrderCreate(
                user_id=1,
                product_id=10,
                quantity=0,
                total_amount=49.99,
            )

    def test_order_create_rejects_negative_total_amount(self) -> None:
        with pytest.raises(ValidationError):
            OrderCreate(
                user_id=1,
                product_id=10,
                total_amount=-1.0,
            )

    def test_order_update_allows_partial_status_change(self) -> None:
        update = OrderUpdate(status="COMPLETED")

        assert update.model_dump(exclude_unset=True) == {
            "status": "COMPLETED"
        }


class TestProductModels:
    def test_product_create_accepts_minimal_valid_payload(self) -> None:
        product = ProductCreate(
            name="Standard Product",
            sku="SKU-001",
            price=9.99,
        )

        assert product.name == "Standard Product"
        assert product.sku == "SKU-001"
        assert product.price == 9.99
        assert product.category is None
        assert product.description is None

    def test_product_create_rejects_negative_price(self) -> None:
        with pytest.raises(ValidationError):
            ProductCreate(
                name="Invalid Product",
                sku="BAD-001",
                price=-0.01,
            )

    def test_product_update_allows_partial_price_change(self) -> None:
        update = ProductUpdate(price=19.99)

        assert update.model_dump(exclude_unset=True) == {
            "price": 19.99
        }
