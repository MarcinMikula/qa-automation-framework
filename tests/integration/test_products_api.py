"""Integration tests for ProductService."""

import httpx
import pytest

from api.products_service import (
    ProductCreate,
    ProductService,
    ProductUpdate,
)


class TestProductServiceHealth:
    def test_health_check_returns_ok(
        self,
        product_service: ProductService,
    ) -> None:
        health = product_service.health_check()

        assert health.status == "ok"
        assert health.service == "products"
        assert health.port == 8003


class TestProductServiceCrud:
    def test_create_returns_product_with_id(
        self,
        clean_products,
        product_service: ProductService,
    ) -> None:
        product = product_service.create(
            ProductCreate(
                name="Standard Product",
                sku="SKU-STANDARD-001",
                price=49.99,
            )
        )

        assert product.id > 0
        assert product.name == "Standard Product"
        assert product.sku == "SKU-STANDARD-001"
        assert product.price == 49.99
        assert len(product_service.get_all()) == 1

    def test_get_returns_existing_product(
        self,
        clean_products,
        product_service: ProductService,
    ) -> None:
        created = product_service.create(
            ProductCreate(
                name="Physical Product",
                sku="SKU-PHYSICAL-001",
                price=79.99,
                category="physical",
            )
        )

        fetched = product_service.get(created.id)

        assert fetched.id == created.id
        assert fetched.category == "physical"

    def test_get_all_returns_all_products(
        self,
        clean_products,
        product_service: ProductService,
    ) -> None:
        product_service.create(
            ProductCreate(
                name="Product A",
                sku="SKU-A",
                price=10.0,
            )
        )
        product_service.create(
            ProductCreate(
                name="Product B",
                sku="SKU-B",
                price=20.0,
            )
        )

        products = product_service.get_all()

        assert len(products) == 2
        skus = {product.sku for product in products}
        assert skus == {"SKU-A", "SKU-B"}

    def test_update_changes_product_fields(
        self,
        clean_products,
        product_service: ProductService,
    ) -> None:
        created = product_service.create(
            ProductCreate(
                name="Service Product",
                sku="SKU-SERVICE-001",
                price=99.99,
                category="service",
            )
        )

        updated = product_service.update(
            created.id,
            ProductUpdate(
                name="Premium Service Product",
                price=149.99,
                category="premium-service",
            ),
        )

        assert updated.name == "Premium Service Product"
        assert updated.price == 149.99
        assert updated.category == "premium-service"
        assert updated.sku == "SKU-SERVICE-001"

    def test_delete_removes_product(
        self,
        clean_products,
        product_service: ProductService,
    ) -> None:
        created = product_service.create(
            ProductCreate(
                name="Temporary Product",
                sku="SKU-DELETE",
                price=1.0,
            )
        )

        product_service.delete(created.id)

        assert product_service.get_all() == []


class TestProductServiceNegative:
    def test_get_nonexistent_id_raises_404(
        self,
        clean_products,
        product_service: ProductService,
    ) -> None:
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            product_service.get(9999)

        assert exc_info.value.response.status_code == 404

    def test_delete_nonexistent_id_raises_404(
        self,
        clean_products,
        product_service: ProductService,
    ) -> None:
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            product_service.delete(9999)

        assert exc_info.value.response.status_code == 404


class TestProductPayloadVariants:
    @pytest.mark.parametrize(
        "name,sku,price,category,description",
        [
            (
                "Physical Product",
                "SKU-PHYSICAL",
                49.99,
                "physical",
                "A product delivered in physical form",
            ),
            (
                "Digital Product",
                "SKU-DIGITAL",
                19.99,
                "digital",
                "A product delivered digitally",
            ),
            (
                "Service Product",
                "SKU-SERVICE",
                99.0,
                "service",
                None,
            ),
        ],
        ids=[
            "physical_with_description",
            "digital_with_description",
            "service_without_description",
        ],
    )
    def test_create_product_payload_variant(
        self,
        clean_products,
        product_service: ProductService,
        name: str,
        sku: str,
        price: float,
        category: str,
        description: str | None,
    ) -> None:
        product = product_service.create(
            ProductCreate(
                name=name,
                sku=sku,
                price=price,
                category=category,
                description=description,
            )
        )

        assert product.name == name
        assert product.sku == sku
        assert product.price == price
        assert product.category == category
        assert product.description == description

        fetched = product_service.get(product.id)
        assert fetched.sku == sku
