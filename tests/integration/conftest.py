"""Integration fixtures for local Service Object examples."""

from __future__ import annotations

import subprocess
import sys
import time
from collections.abc import Generator
from typing import Any

import httpx
import pytest

from api.orders_service import OrderService
from api.products_service import ProductService
from api.users_service import UserService
from testdata.settings import (
    ORDERS_BASE_URL,
    PRODUCTS_BASE_URL,
    USERS_BASE_URL,
)


_MICROSERVICES = (
    (USERS_BASE_URL, "services.users.main"),
    (ORDERS_BASE_URL, "services.orders.main"),
    (PRODUCTS_BASE_URL, "services.products.main"),
)
_STARTUP_TIMEOUT_S = 30
_POLL_INTERVAL_S = 0.5


def _is_service_up(base_url: str) -> bool:
    """Return whether a local service responds successfully to /health."""
    try:
        response = httpx.get(
            f"{base_url.rstrip('/')}/health",
            timeout=2.0,
        )
        return response.status_code == 200
    except httpx.HTTPError:
        return False


def _wait_for_service(
    base_url: str,
    timeout_s: float = _STARTUP_TIMEOUT_S,
) -> None:
    """Wait until a local service is ready."""
    deadline = time.time() + timeout_s

    while time.time() < deadline:
        if _is_service_up(base_url):
            return
        time.sleep(_POLL_INTERVAL_S)

    raise RuntimeError(
        f"Service did not start within {timeout_s}s: {base_url}"
    )


def _clear_resource(service: Any) -> None:
    """Remove all records from a local in-memory service."""
    for item in service.get_all():
        service.delete(item.id)


@pytest.fixture(scope="session")
def microservices() -> Generator[None, None, None]:
    """Start local users, orders, and products services for the test session."""
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

    yield

    for process in processes:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture(scope="session")
def user_service(microservices) -> UserService:
    """Return the SOM adapter for the local users service."""
    return UserService()


@pytest.fixture(scope="session")
def order_service(microservices) -> OrderService:
    """Return the SOM adapter for the local orders service."""
    return OrderService()


@pytest.fixture(scope="session")
def product_service(microservices) -> ProductService:
    """Return the SOM adapter for the local products service."""
    return ProductService()


@pytest.fixture
def clean_users(
    user_service: UserService,
) -> Generator[None, None, None]:
    """Clear user records before each test."""
    _clear_resource(user_service)
    yield


@pytest.fixture
def clean_orders(
    order_service: OrderService,
) -> Generator[None, None, None]:
    """Clear order records before each test."""
    _clear_resource(order_service)
    yield


@pytest.fixture
def clean_products(
    product_service: ProductService,
) -> Generator[None, None, None]:
    """Clear product records before each test."""
    _clear_resource(product_service)
    yield
