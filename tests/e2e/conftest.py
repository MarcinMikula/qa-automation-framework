"""Fixtures for E2E tests.

E2E tests should be self-contained by default.

This file starts the small local services required by browser tests when they
are not already running.
"""

from __future__ import annotations

import subprocess
import sys
import time
from collections.abc import Generator

import httpx
import pytest

from testdata.settings import USERS_BASE_URL

DEMO_SHOP_BASE_URL = "http://localhost:8010"
_STARTUP_TIMEOUT_S = 30
_POLL_INTERVAL_S = 0.5


def _is_service_up(base_url: str, health_path: str = "/health") -> bool:
    """Return True when a local HTTP service responds to its health endpoint."""
    try:
        response = httpx.get(f"{base_url.rstrip('/')}{health_path}", timeout=2.0)
        return response.status_code == 200
    except httpx.HTTPError:
        return False


def _wait_for_service(
    base_url: str,
    health_path: str = "/health",
    timeout_s: float = _STARTUP_TIMEOUT_S,
) -> None:
    """Wait until a local HTTP service becomes available."""
    deadline = time.time() + timeout_s

    while time.time() < deadline:
        if _is_service_up(base_url, health_path=health_path):
            return
        time.sleep(_POLL_INTERVAL_S)

    raise RuntimeError(
        f"Service did not start within {timeout_s}s: {base_url}{health_path}"
    )


def _terminate_process(process: subprocess.Popen | None) -> None:
    """Terminate a process started by the fixture."""
    if process is None:
        return

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture(scope="session")
def demo_shop_app() -> Generator[str, None, None]:
    """Start the local demo shop unless it is already running."""
    process: subprocess.Popen | None = None

    if not _is_service_up(DEMO_SHOP_BASE_URL, health_path="/shop/health"):
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "services.demo_shop.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8010",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    _wait_for_service(DEMO_SHOP_BASE_URL, health_path="/shop/health")

    yield f"{DEMO_SHOP_BASE_URL}/shop"

    _terminate_process(process)


@pytest.fixture
def clean_demo_shop(demo_shop_app: str) -> Generator[None, None, None]:
    """Reset demo shop state before and after each E2E test."""
    httpx.post(f"{DEMO_SHOP_BASE_URL}/shop/reset", timeout=5.0)
    yield
    httpx.post(f"{DEMO_SHOP_BASE_URL}/shop/reset", timeout=5.0)


@pytest.fixture(scope="session")
def users_service_for_swagger() -> Generator[str, None, None]:
    """Start the local users service required by Swagger UI smoke tests."""
    process: subprocess.Popen | None = None

    if not _is_service_up(USERS_BASE_URL):
        process = subprocess.Popen(
            [sys.executable, "-m", "services.users.main"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    _wait_for_service(USERS_BASE_URL)

    yield USERS_BASE_URL

    _terminate_process(process)
