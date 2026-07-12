"""Unit tests for local microservice Pydantic models."""

import pytest
from pydantic import ValidationError

from services.orders.main import OrderCreate, OrderUpdate
from services.products.main import ProductCreate, ProductUpdate
from services.users.main import UserCreate, UserUpdate


class TestUserModels:
    def test_user_create_defaults_account_status_to_active(self):
        user = UserCreate(
            full_name="Jan Kowalski",
            msisdn="48100200301",
        )

        assert user.account_status == "ACTIVE"
        assert user.email is None
        assert user.contract_type is None

    def test_user_create_rejects_invalid_account_status(self):
        with pytest.raises(ValidationError):
            UserCreate(
                full_name="Jan Kowalski",
                msisdn="48100200301",
                account_status="BLOCKED",
            )

    def test_user_update_allows_partial_payload(self):
        update = UserUpdate(plan="BiznesMAX_100GB")

        assert update.model_dump(exclude_unset=True) == {"plan": "BiznesMAX_100GB"}


class TestOrderModels:
    def test_order_create_defaults_status_and_quantity(self):
        order = OrderCreate(
            customer_id=1,
            product_id=10,
            total_amount=129.99,
        )

        assert order.quantity == 1
        assert order.status == "NEW"
        assert order.invoice_reference is None

    def test_order_create_rejects_zero_quantity(self):
        with pytest.raises(ValidationError):
            OrderCreate(
                customer_id=1,
                product_id=10,
                quantity=0,
                total_amount=129.99,
            )

    def test_order_create_rejects_negative_total_amount(self):
        with pytest.raises(ValidationError):
            OrderCreate(
                customer_id=1,
                product_id=10,
                total_amount=-1.0,
            )

    def test_order_update_allows_partial_status_change(self):
        update = OrderUpdate(status="CONFIRMED")

        assert update.model_dump(exclude_unset=True) == {"status": "CONFIRMED"}


class TestProductModels:
    def test_product_create_accepts_minimal_valid_payload(self):
        product = ProductCreate(
            name="SIM Card",
            sku="SIM-001",
            price=9.99,
        )

        assert product.name == "SIM Card"
        assert product.sku == "SIM-001"
        assert product.price == 9.99
        assert product.category is None
        assert product.description is None

    def test_product_create_rejects_negative_price(self):
        with pytest.raises(ValidationError):
            ProductCreate(
                name="Invalid",
                sku="BAD-001",
                price=-0.01,
            )

    def test_product_update_allows_partial_price_change(self):
        update = ProductUpdate(price=19.99)

        assert update.model_dump(exclude_unset=True) == {"price": 19.99}
