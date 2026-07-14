"""Fixtures for local demo shop E2E tests."""

from __future__ import annotations

import subprocess
import sys
import time
from collections.abc import Generator

import httpx
import pytest

DEMO_SHOP_BASE_URL = "http://localhost:8010"
_STARTUP_TIMEOUT_S = 30
_POLL_INTERVAL_S = 0.5


def _is_demo_shop_up() -> bool:
    try:
        response = httpx.get(f"{DEMO_SHOP_BASE_URL}/shop/health", timeout=2.0)
        return response.status_code == 200
    except httpx.HTTPError:
        return False


def _wait_for_demo_shop(timeout_s: float = _STARTUP_TIMEOUT_S) -> None:
    deadline = time.time() + timeout_s

    while time.time() < deadline:
        if _is_demo_shop_up():
            return
        time.sleep(_POLL_INTERVAL_S)

    raise RuntimeError(f"Demo shop did not start within {timeout_s}s")


@pytest.fixture(scope="session")
def demo_shop_app() -> Generator[str, None, None]:
    """Start the local demo shop unless it is already running."""
    process: subprocess.Popen | None = None

    if not _is_demo_shop_up():
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

    _wait_for_demo_shop()

    yield f"{DEMO_SHOP_BASE_URL}/shop"

    if process is not None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture
def clean_demo_shop(demo_shop_app: str) -> Generator[None, None, None]:
    """Reset demo shop state before and after each E2E test."""
    httpx.post(f"{DEMO_SHOP_BASE_URL}/shop/reset", timeout=5.0)
    yield
    httpx.post(f"{DEMO_SHOP_BASE_URL}/shop/reset", timeout=5.0)
