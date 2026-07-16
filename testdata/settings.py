"""Central configuration for local example services and shared timeouts.

Environment variables may override the deterministic local defaults.
Application-specific URLs and credentials should be added during project
adaptation, not shipped as unrelated placeholders.
"""

import os


# Local FastAPI example services
USERS_BASE_URL = os.getenv("USERS_BASE_URL", "http://localhost:8001")
ORDERS_BASE_URL = os.getenv("ORDERS_BASE_URL", "http://localhost:8002")
PRODUCTS_BASE_URL = os.getenv("PRODUCTS_BASE_URL", "http://localhost:8003")


# Shared timeouts
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))  # ms, Playwright
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))  # s, httpx
