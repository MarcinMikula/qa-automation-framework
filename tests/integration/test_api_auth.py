"""
test_api_auth.py
Testy API warstwy autoryzacji — Service Object Model.
Weryfikacja tokenow, rol i scenariuszy nieautoryzowanego dostepu.
"""
import pytest
from api.auth_service import AuthService
from testdata.settings import AGENT_USER, AGENT_PASS
pytestmark = pytest.mark.external


class TestApiAuth:

    def test_valid_credentials_return_token(self):
        auth = AuthService()
        response = auth.login(AGENT_USER, AGENT_PASS)
        assert response.status_code == 200
        assert "token" in response.json()

    def test_invalid_credentials_return_401(self):
        auth = AuthService()
        response = auth.login("fake_user", "fake_pass")
        assert response.status_code == 401

    def test_token_contains_role(self):
        auth = AuthService()
        response = auth.login(AGENT_USER, AGENT_PASS)
        data = response.json()
        assert data.get("role") in ("AGENT", "SUPERVISOR", "ADMIN")
