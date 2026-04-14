"""
settings.py
Centralna konfiguracja środowiska.
Zmienne środowiskowe nadpisują wartości domyślne — bezpieczne dla CI/CD.
"""
import os

# --- URLs -------------------------------------------------------------------
BASE_URL = os.getenv("BASE_URL", "https://telcobilling.local")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.telcobilling.local/v1")

# --- Credentials (nigdy nie commituj prawdziwych danych!) -------------------
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "Admin1234!")

AGENT_USER = os.getenv("AGENT_USER", "agent01")
AGENT_PASS = os.getenv("AGENT_PASS", "Agent1234!")

SUPERVISOR_USER = os.getenv("SUPERVISOR_USER", "supervisor01")
SUPERVISOR_PASS = os.getenv("SUPERVISOR_PASS", "Super1234!")

# --- Timeouts ---------------------------------------------------------------
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))  # ms, Playwright
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))             # s, httpx
