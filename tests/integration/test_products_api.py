"""
test_products_api.py
Testy integracyjne ProductService — mikroserwis products (port 8003).

Uruchomienie:
    pytest tests/integration/test_products_api.py -v
"""
import httpx
import pytest

from api.products_service import ProductCreate, ProductService, ProductUpdate


class TestProductServiceHealth:
    """Testy endpointu /health."""

    def test_health_check_returns_ok(self, product_service: ProductService):
        """health_check zwraca status ok i nazwę serwisu products."""
        health = product_service.health_check()

        assert health.status == "ok"
        assert health.service == "products"
        assert health.port == 8003


class TestProductServiceCrud:
    """[DOMAIN: GENERIC] Testy pełnego cyklu CRUD przez SOM."""

    def test_create_returns_product_with_id(self, clean_products, product_service: ProductService):
        """create dodaje produkt i zwraca model z nadanym id."""
        product = product_service.create(
            ProductCreate(name="Plan StartGO", sku="SKU-START-10", price=29.99)
        )

        assert product.id > 0
        assert product.name == "Plan StartGO"
        assert product.sku == "SKU-START-10"
        assert product.price == 29.99
        assert len(product_service.get_all()) == 1

    def test_get_returns_existing_product(self, clean_products, product_service: ProductService):
        """get pobiera produkt po id."""
        created = product_service.create(
            ProductCreate(
                name="Router 5G",
                sku="SKU-HW-5G",
                price=499.0,
                category="hardware",
            )
        )

        fetched = product_service.get(created.id)

        assert fetched.id == created.id
        assert fetched.category == "hardware"

    def test_get_all_returns_all_products(self, clean_products, product_service: ProductService):
        """get_all zwraca listę wszystkich produktów."""
        product_service.create(
            ProductCreate(name="Produkt A", sku="SKU-A", price=10.0)
        )
        product_service.create(
            ProductCreate(name="Produkt B", sku="SKU-B", price=20.0)
        )

        products = product_service.get_all()

        assert len(products) == 2
        skus = {p.sku for p in products}
        assert skus == {"SKU-A", "SKU-B"}

    def test_update_changes_product_fields(self, clean_products, product_service: ProductService):
        """update modyfikuje pola produktu (PUT)."""
        created = product_service.create(
            ProductCreate(
                name="Plan BiznesMAX",
                sku="SKU-BIZ-50",
                price=129.99,
                category="mobile",
            )
        )

        updated = product_service.update(
            created.id,
            ProductUpdate(name="Plan BiznesMAX 100GB", price=199.99, category="business"),
        )

        assert updated.name == "Plan BiznesMAX 100GB"
        assert updated.price == 199.99
        assert updated.category == "business"
        assert updated.sku == "SKU-BIZ-50"

    def test_delete_removes_product(self, clean_products, product_service: ProductService):
        """delete usuwa produkt — get_all jest puste po usunięciu."""
        created = product_service.create(
            ProductCreate(name="Do usunięcia", sku="SKU-DEL", price=1.0)
        )

        product_service.delete(created.id)

        assert product_service.get_all() == []


class TestProductServiceNegative:
    """[DOMAIN: GENERIC] Scenariusze negatywne — nieistniejące zasoby."""

    def test_get_nonexistent_id_raises_404(self, clean_products, product_service: ProductService):
        """get nieistniejącego id zwraca HTTP 404."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            product_service.get(9999)

        assert exc_info.value.response.status_code == 404

    def test_delete_nonexistent_id_raises_404(self, clean_products, product_service: ProductService):
        """delete nieistniejącego id zwraca HTTP 404."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            product_service.delete(9999)

        assert exc_info.value.response.status_code == 404


class TestProductCatalogVariants:
    """[DOMAIN: GENERIC] Warianty katalogu produktów — kategorie i ceny."""

    @pytest.mark.parametrize(
        "name,sku,price,category,description",
        [
            ("Plan StartGO 10GB", "SKU-START-10", 29.99, "mobile", "Pakiet prepaid 10GB"),
            ("Plan BiznesMAX 50GB", "SKU-BIZ-50", 129.99, "business", "Pakiet postpaid dla firm"),
            ("Router 5G Pro", "SKU-HW-5G", 499.0, "hardware", None),
        ],
        ids=["mobile_prepaid", "business_postpaid", "hardware_no_description"],
    )
    def test_create_product_catalog_variant(
        self,
        clean_products,
        product_service: ProductService,
        name: str,
        sku: str,
        price: float,
        category: str,
        description: str | None,
    ):
        """[DOMAIN: GENERIC] Tworzenie produktu z różnymi kategoriami i atrybutami katalogowymi."""
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
