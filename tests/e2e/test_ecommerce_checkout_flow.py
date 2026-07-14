"""E2E POM case study for a small local e-commerce flow."""

from playwright.sync_api import Page

from pages.ecommerce_cart_page import EcommerceCartPage
from pages.ecommerce_checkout_page import EcommerceCheckoutPage
from pages.ecommerce_order_confirmation_page import EcommerceOrderConfirmationPage
from pages.ecommerce_product_page import EcommerceProductPage
from pages.ecommerce_search_page import EcommerceSearchPage


class TestEcommerceCheckoutFlow:
    """Business-readable browser flow expressed through Page Objects."""

    def test_customer_can_buy_available_product(
        self,
        page: Page,
        demo_shop_app: str,
        clean_demo_shop,
    ):
        search_page = EcommerceSearchPage(page, base_url=demo_shop_app)
        product_page = EcommerceProductPage(page)
        cart_page = EcommerceCartPage(page)
        checkout_page = EcommerceCheckoutPage(page)
        order_confirmation = EcommerceOrderConfirmationPage(page)

        search_page.open()
        search_page.search_for("Samsung 65 OLED")

        assert search_page.result_names() == ["Samsung 65 OLED"]

        search_page.open_product("samsung-65-oled")

        assert product_page.product_name() == "Samsung 65 OLED"
        assert product_page.price() == "4999.00 PLN"
        assert product_page.availability() == "Available"

        product_page.add_to_cart()

        assert cart_page.item_names() == ["Samsung 65 OLED"]
        assert cart_page.total() == "4999.00 PLN"

        cart_page.proceed_to_checkout()

        assert checkout_page.total() == "4999.00 PLN"

        checkout_page.place_order(customer_name="Marcin Testowy")

        assert order_confirmation.order_id().startswith("DEMO-")
        assert order_confirmation.status() == "Order confirmed"
        assert order_confirmation.customer_name() == "Marcin Testowy"
        assert order_confirmation.item_names() == ["Samsung 65 OLED × 1"]
        assert order_confirmation.total() == "4999.00 PLN"
