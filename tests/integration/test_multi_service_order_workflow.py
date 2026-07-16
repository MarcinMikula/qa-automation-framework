"""Integration tests for a small multi-service SOM workflow.

The local services intentionally do not enforce cross-service referential
integrity. These tests verify that the framework can express a readable
workflow through separate Service Objects:

user → product → order → order status change
"""

from api.orders_service import OrderCreate, OrderService, OrderUpdate
from api.products_service import ProductCreate, ProductService
from api.users_service import UserCreate, UserService


class TestMultiServiceOrderWorkflow:
    def test_user_can_create_order_for_product(
        self,
        clean_users,
        clean_products,
        clean_orders,
        user_service: UserService,
        product_service: ProductService,
        order_service: OrderService,
    ) -> None:
        user = user_service.create(
            UserCreate(
                full_name="Alex Workflow",
                external_id="USR-WORKFLOW-001",
                email="alex.workflow@example.com",
            )
        )
        product = product_service.create(
            ProductCreate(
                name="Standard Product",
                sku="SKU-WORKFLOW-001",
                price=49.99,
                category="physical",
                description="Neutral product used by the SOM workflow",
            )
        )

        order = order_service.create(
            OrderCreate(
                user_id=user.id,
                product_id=product.id,
                quantity=1,
                total_amount=product.price,
            )
        )

        assert order.user_id == user.id
        assert order.product_id == product.id
        assert order.quantity == 1
        assert order.total_amount == product.price
        assert order.status == "NEW"
        assert order.external_reference is None

        fetched_user = user_service.get(user.id)
        fetched_product = product_service.get(product.id)
        fetched_order = order_service.get(order.id)

        assert fetched_user.external_id == "USR-WORKFLOW-001"
        assert fetched_product.sku == "SKU-WORKFLOW-001"
        assert fetched_order.id == order.id

    def test_order_can_be_completed_with_external_reference(
        self,
        clean_users,
        clean_products,
        clean_orders,
        user_service: UserService,
        product_service: ProductService,
        order_service: OrderService,
    ) -> None:
        user = user_service.create(
            UserCreate(
                full_name="Taylor Workflow",
                external_id="USR-WORKFLOW-002",
                status="ACTIVE",
            )
        )
        product = product_service.create(
            ProductCreate(
                name="Digital Product",
                sku="SKU-WORKFLOW-002",
                price=19.99,
                category="digital",
                description="Neutral digital product",
            )
        )
        order = order_service.create(
            OrderCreate(
                user_id=user.id,
                product_id=product.id,
                quantity=1,
                total_amount=product.price,
            )
        )

        completed_order = order_service.update(
            order.id,
            OrderUpdate(
                status="COMPLETED",
                external_reference="EXT-WORKFLOW-001",
            ),
        )

        assert completed_order.status == "COMPLETED"
        assert completed_order.external_reference == "EXT-WORKFLOW-001"
        assert completed_order.user_id == user.id
        assert completed_order.product_id == product.id

        assert user_service.get(user.id).status == "ACTIVE"
        assert product_service.get(product.id).sku == "SKU-WORKFLOW-002"
