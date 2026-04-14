"""
auth_service.py
Service Object dla endpointow autoryzacji.
"""
from api.base_client import BaseClient


class AuthService(BaseClient):
    ENDPOINT_LOGIN = "/auth/login"
    ENDPOINT_LOGOUT = "/auth/logout"

    def login(self, username: str, password: str):
        """Zwraca response z tokenem JWT lub bledem autoryzacji."""
        return self.post(self.ENDPOINT_LOGIN, {
            "username": username,
            "password": password
        })

    def logout(self):
        return self.post(self.ENDPOINT_LOGOUT, {})
