"""Integration tests for a small multi-service SOM workflow.

These tests intentionally exercise Service Objects together instead of testing
one CRUD endpoint in isolation.

They do not prove that the demo services enforce cross-service referential
integrity. The local services are intentionally simple.

They do prove that the framework can express a business-readable API workflow:

customer
→ product
→ order
→ order status change
"""

from api.orders_service import OrderCreate, OrderUpdate, OrderService
from api.products_service import ProductCreate, ProductService
from api.users_service import UserCreate, UserService


class TestTelcoOrderWorkflow:
    """[DOMAIN: TELCO] Multi-service workflow expressed through SOM objects."""

    def test_customer_can_order_mobile_plan(
        self,
        clean_users,
        clean_products,
        clean_orders,
        user_service: UserService,
        product_service: ProductService,
        order_service: OrderService,
    ):
        """Create customer, product, and order through Service Objects."""
        customer = user_service.create(
            UserCreate(
                full_name="Marcin Testowy",
                msisdn="48100123456",
                contract_type="POSTPAID",
                plan="BiznesMAX_50GB",
                account_status="ACTIVE",
            )
        )

        product = product_service.create(
            ProductCreate(
                name="Plan BiznesMAX 50GB",
                sku="SKU-BIZ-50-WORKFLOW",
                price=129.99,
                category="business",
                description="Postpaid mobile plan for business customers",
            )
        )

        order = order_service.create(
            OrderCreate(
                customer_id=customer.id,
                product_id=product.id,
                quantity=1,
                total_amount=product.price,
            )
        )

        assert order.customer_id == customer.id
        assert order.product_id == product.id
        assert order.quantity == 1
        assert order.total_amount == product.price
        assert order.status == "NEW"
        assert order.invoice_reference is None

        fetched_customer = user_service.get(customer.id)
        fetched_product = product_service.get(product.id)
        fetched_order = order_service.get(order.id)

        assert fetched_customer.msisdn == "48100123456"
        assert fetched_product.sku == "SKU-BIZ-50-WORKFLOW"
        assert fetched_order.id == order.id

    def test_order_can_be_confirmed_with_billing_reference(
        self,
        clean_users,
        clean_products,
        clean_orders,
        user_service: UserService,
        product_service: ProductService,
        order_service: OrderService,
    ):
        """Confirm an order and attach a billing/invoice reference."""
        customer = user_service.create(
            UserCreate(
                full_name="Anna Workflow",
                msisdn="48100654321",
                contract_type="PREPAID",
                plan="StartGO_10GB",
                account_status="ACTIVE",
            )
        )

        product = product_service.create(
            ProductCreate(
                name="Plan StartGO 10GB",
                sku="SKU-START-10-WORKFLOW",
                price=29.99,
                category="mobile",
                description="Prepaid mobile package",
            )
        )

        order = order_service.create(
            OrderCreate(
                customer_id=customer.id,
                product_id=product.id,
                quantity=1,
                total_amount=product.price,
                status="NEW",
            )
        )

        confirmed_order = order_service.update(
            order.id,
            OrderUpdate(
                status="CONFIRMED",
                invoice_reference="INV-WORKFLOW-001",
            ),
        )

        assert confirmed_order.status == "CONFIRMED"
        assert confirmed_order.invoice_reference == "INV-WORKFLOW-001"
        assert confirmed_order.customer_id == customer.id
        assert confirmed_order.product_id == product.id

        # The workflow keeps the Service Object boundary explicit:
        # the test verifies related resources through their own services.
        assert user_service.get(customer.id).account_status == "ACTIVE"
        assert product_service.get(product.id).sku == "SKU-START-10-WORKFLOW"
