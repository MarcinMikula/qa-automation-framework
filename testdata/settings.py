"""
settings.py
Centralna konfiguracja środowiska.
Zmienne środowiskowe nadpisują wartości domyślne — bezpieczne dla CI/CD.
"""
import os

# --- URLs -------------------------------------------------------------------
BASE_URL = os.getenv("BASE_URL", "https://automationintesting.online")
API_BASE_URL = os.getenv("API_BASE_URL", "https://restful-booker.herokuapp.com")

# --- Credentials ------------------------------------------------------------
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "password123")

AGENT_USER = os.getenv("AGENT_USER", "admin")
AGENT_PASS = os.getenv("AGENT_PASS", "password123")

SUPERVISOR_USER = os.getenv("SUPERVISOR_USER", "admin")
SUPERVISOR_PASS = os.getenv("SUPERVISOR_PASS", "password123")

# --- Timeouts ---------------------------------------------------------------
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))  # ms, Playwright
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))             # s, httpx