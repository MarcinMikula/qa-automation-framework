"""
conftest.py
Fixtures dla testów integracyjnych — cykl życia mikroserwisów i izolacja danych.

Uruchomienie:
    pytest tests/integration/ -v
"""
import subprocess
import sys
import time
from collections.abc import Generator

import httpx
import pytest

from api.orders_service import OrderService
from api.products_service import ProductService
from api.users_service import UserService
from testdata.settings import ORDERS_BASE_URL, PRODUCTS_BASE_URL, USERS_BASE_URL

# [DOMAIN: GENERIC] — konfiguracja lokalnych mikroserwisów
_MICROSERVICES = (
    (USERS_BASE_URL, "services.users.main"),
    (ORDERS_BASE_URL, "services.orders.main"),
    (PRODUCTS_BASE_URL, "services.products.main"),
)
_STARTUP_TIMEOUT_S = 30
_POLL_INTERVAL_S = 0.5


def _is_service_up(base_url: str) -> bool:
    """Sprawdza, czy mikroserwis odpowiada na /health."""
    try:
        response = httpx.get(f"{base_url.rstrip('/')}/health", timeout=2.0)
        return response.status_code == 200
    except httpx.HTTPError:
        return False


def _wait_for_service(base_url: str, timeout_s: float = _STARTUP_TIMEOUT_S) -> None:
    """Czeka aż mikroserwis będzie gotowy (endpoint /health)."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if _is_service_up(base_url):
            return
        time.sleep(_POLL_INTERVAL_S)
    raise RuntimeError(f"Mikroserwis nie wystartował w czasie {timeout_s}s: {base_url}")


def _clear_resource(service) -> None:
    """[DOMAIN: GENERIC] Usuwa wszystkie rekordy z magazynu in-memory serwisu."""
    for item in service.get_all():
        service.delete(item.id)


@pytest.fixture(scope="session")
def microservices() -> Generator[None, None, None]:
    """
    [DOMAIN: GENERIC] Uruchamia users (8001), orders (8002), products (8003)
    przed sesją testową i zatrzymuje procesy po zakończeniu.
    Jeśli serwisy już działają — nie startuje ich ponownie.
    """
    processes: list[subprocess.Popen] = []

    for base_url, module in _MICROSERVICES:
        if not _is_service_up(base_url):
            process = subprocess.Popen(
                [sys.executable, "-m", module],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            processes.append(process)
            _wait_for_service(base_url)
        else:
            _wait_for_service(base_url)

    yield

    for process in processes:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture(scope="session")
def user_service(microservices) -> UserService:
    """[DOMAIN: TELCO] Klient SOM dla mikroserwisu użytkowników (klienci telco)."""
    return UserService()


@pytest.fixture(scope="session")
def order_service(microservices) -> OrderService:
    """[DOMAIN: GENERIC] Klient SOM dla mikroserwisu zamówień."""
    return OrderService()


@pytest.fixture(scope="session")
def product_service(microservices) -> ProductService:
    """[DOMAIN: GENERIC] Klient SOM dla mikroserwisu produktów."""
    return ProductService()


@pytest.fixture
def clean_users(user_service: UserService) -> Generator[None, None, None]:
    """[DOMAIN: TELCO] Czyści dane users przed testem — izolacja scenariuszy abonentów."""
    _clear_resource(user_service)
    yield


@pytest.fixture
def clean_orders(order_service: OrderService) -> Generator[None, None, None]:
    """[DOMAIN: GENERIC] Czyści dane orders przed testem."""
    _clear_resource(order_service)
    yield


@pytest.fixture
def clean_products(product_service: ProductService) -> Generator[None, None, None]:
    """[DOMAIN: GENERIC] Czyści dane products przed testem."""
    _clear_resource(product_service)
    yield
