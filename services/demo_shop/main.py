"""Small local e-commerce demo UI for the POM case study.

This is not a production shop and not framework core.

Its only purpose is to provide a deterministic, replaceable browser target for
Page Object Model tests.
"""

from __future__ import annotations

from html import escape
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="Demo Shop UI")

PRODUCTS: list[dict[str, Any]] = [
    {
        "slug": "samsung-65-oled",
        "name": "Samsung 65 OLED",
        "price": 4999.00,
        "availability": "Available",
        "category": "TV",
    },
    {
        "slug": "bosch-washing-machine",
        "name": "Bosch Washing Machine",
        "price": 2199.00,
        "availability": "Available",
        "category": "AGD",
    },
    {
        "slug": "sony-soundbar",
        "name": "Sony Soundbar",
        "price": 1299.00,
        "availability": "Available",
        "category": "Audio",
    },
]

_cart: list[dict[str, Any]] = []
_orders: list[dict[str, Any]] = []


def _layout(title: str, body: str) -> str:
    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>{escape(title)}</title>
      </head>
      <body>
        <header data-testid="header-navigation">
          <a data-testid="home-link" href="/shop">Demo Shop</a>
          <a data-testid="cart-link" href="/shop/cart">Cart ({len(_cart)})</a>
        </header>
        <main>
          {body}
        </main>
      </body>
    </html>
    """


def _format_price(value: float) -> str:
    return f"{value:.2f} PLN"


def _find_product(slug: str) -> dict[str, Any] | None:
    return next((product for product in PRODUCTS if product["slug"] == slug), None)


@app.get("/shop/health")
def health_check() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "demo-shop-ui",
        "products_count": len(PRODUCTS),
        "cart_items_count": len(_cart),
        "orders_count": len(_orders),
    }


@app.post("/shop/reset")
def reset_state() -> dict[str, str]:
    _cart.clear()
    _orders.clear()
    return {"status": "reset"}


@app.get("/shop", response_class=HTMLResponse)
def search_page(q: str = "") -> HTMLResponse:
    normalized_query = q.strip().lower()
    products = [
        product
        for product in PRODUCTS
        if not normalized_query or normalized_query in product["name"].lower()
    ]

    results_html = "\n".join(
        f"""
        <article data-testid="product-card">
          <h2 data-testid="product-card-name">{escape(product["name"])}</h2>
          <p data-testid="product-card-price">{_format_price(product["price"])}</p>
          <p data-testid="product-card-availability">{escape(product["availability"])}</p>
          <a data-testid="open-product-{escape(product["slug"])}"
             href="/shop/products/{escape(product["slug"])}">
             View product
          </a>
        </article>
        """
        for product in products
    )

    if not results_html:
        results_html = '<p data-testid="empty-results">No products found</p>'

    body = f"""
      <h1 data-testid="page-title">Product search</h1>
      <form action="/shop" method="get">
        <label for="search-input">Search</label>
        <input id="search-input" data-testid="search-input" name="q" value="{escape(q)}" />
        <button data-testid="search-submit" type="submit">Search</button>
      </form>
      <section data-testid="search-results">
        {results_html}
      </section>
    """

    return HTMLResponse(_layout("Demo Shop - Product search", body))


@app.get("/shop/products/{slug}", response_class=HTMLResponse)
def product_page(slug: str) -> HTMLResponse:
    product = _find_product(slug)
    if product is None:
        body = """
          <h1 data-testid="page-title">Product not found</h1>
          <a data-testid="back-to-search" href="/shop">Back to search</a>
        """
        return HTMLResponse(_layout("Demo Shop - Product not found", body), status_code=404)

    body = f"""
      <h1 data-testid="product-name">{escape(product["name"])}</h1>
      <p data-testid="product-category">{escape(product["category"])}</p>
      <p data-testid="product-price">{_format_price(product["price"])}</p>
      <p data-testid="product-availability">{escape(product["availability"])}</p>
      <a data-testid="add-to-cart" href="/shop/cart/add/{escape(product["slug"])}">
        Add to cart
      </a>
    """

    return HTMLResponse(_layout(f"Demo Shop - {product['name']}", body))


@app.get("/shop/cart/add/{slug}")
def add_to_cart(slug: str) -> RedirectResponse:
    product = _find_product(slug)
    if product is not None:
        _cart.append({"slug": product["slug"], "name": product["name"], "price": product["price"], "quantity": 1})
    return RedirectResponse("/shop/cart", status_code=303)


@app.get("/shop/cart", response_class=HTMLResponse)
def cart_page() -> HTMLResponse:
    total = sum(item["price"] * item["quantity"] for item in _cart)

    items_html = "\n".join(
        f"""
        <tr data-testid="cart-row">
          <td data-testid="cart-item-name">{escape(item["name"])}</td>
          <td data-testid="cart-item-quantity">{item["quantity"]}</td>
          <td data-testid="cart-item-price">{_format_price(item["price"])}</td>
        </tr>
        """
        for item in _cart
    )

    if not items_html:
        items_html = '<tr data-testid="empty-cart"><td colspan="3">Cart is empty</td></tr>'

    body = f"""
      <h1 data-testid="page-title">Cart</h1>
      <table data-testid="cart-table">
        <tbody>
          {items_html}
        </tbody>
      </table>
      <section data-testid="price-summary">
        <p>Total: <span data-testid="cart-total">{_format_price(total)}</span></p>
      </section>
      <a data-testid="continue-to-checkout" href="/shop/checkout">Continue to checkout</a>
    """

    return HTMLResponse(_layout("Demo Shop - Cart", body))


@app.get("/shop/checkout", response_class=HTMLResponse)
def checkout_page() -> HTMLResponse:
    total = sum(item["price"] * item["quantity"] for item in _cart)

    body = f"""
      <h1 data-testid="page-title">Checkout</h1>
      <section data-testid="checkout-summary">
        <p>Total: <span data-testid="checkout-total">{_format_price(total)}</span></p>
      </section>
      <form action="/shop/orders/create" method="get">
        <label for="customer-name">Customer name</label>
        <input id="customer-name" data-testid="customer-name" name="customer_name" value="" />
        <button data-testid="place-order" type="submit">Place order</button>
      </form>
    """

    return HTMLResponse(_layout("Demo Shop - Checkout", body))


@app.get("/shop/orders/create")
def create_order(customer_name: str = "Guest") -> RedirectResponse:
    order_id = f"DEMO-{len(_orders) + 1:04d}"
    total = sum(item["price"] * item["quantity"] for item in _cart)
    order = {
        "id": order_id,
        "customer_name": customer_name,
        "items": list(_cart),
        "total": total,
        "status": "Order confirmed",
    }
    _orders.append(order)
    _cart.clear()

    return RedirectResponse(f"/shop/orders/{order_id}", status_code=303)


@app.get("/shop/orders/{order_id}", response_class=HTMLResponse)
def order_confirmation_page(order_id: str) -> HTMLResponse:
    order = next((item for item in _orders if item["id"] == order_id), None)

    if order is None:
        body = """
          <h1 data-testid="page-title">Order not found</h1>
          <a data-testid="back-to-search" href="/shop">Back to search</a>
        """
        return HTMLResponse(_layout("Demo Shop - Order not found", body), status_code=404)

    items_html = "\n".join(
        f"""
        <li data-testid="confirmed-order-item">
          {escape(item["name"])} × {item["quantity"]}
        </li>
        """
        for item in order["items"]
    )

    body = f"""
      <h1 data-testid="page-title">Order confirmation</h1>
      <p>Order ID: <span data-testid="order-id">{escape(order["id"])}</span></p>
      <p>Status: <span data-testid="order-status">{escape(order["status"])}</span></p>
      <p>Customer: <span data-testid="order-customer">{escape(order["customer_name"])}</span></p>
      <ul data-testid="confirmed-order-items">
        {items_html}
      </ul>
      <p>Total: <span data-testid="order-total">{_format_price(order["total"])}</span></p>
    """

    return HTMLResponse(_layout("Demo Shop - Order confirmation", body))
