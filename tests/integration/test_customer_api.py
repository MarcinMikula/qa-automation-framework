"""
test_customer_api.py
Testy API zarzadzania klientem — data-driven, kontekst billingowy telco.
"""
import pytest
from api.customer_service import CustomerService


MSISDN_ACTIVE = "48100200301"
MSISDN_SUSPENDED = "48100200303"


class TestCustomerApi:

    def test_get_active_customer_returns_200(self, api_token):
        service = CustomerService(token=api_token)
        response = service.get_customer_by_msisdn(MSISDN_ACTIVE)
        assert response.status_code == 200
        assert response.json()["account_status"] == "ACTIVE"

    def test_suspended_customer_has_correct_status(self, api_token):
        service = CustomerService(token=api_token)
        response = service.get_customer_by_msisdn(MSISDN_SUSPENDED)
        assert response.status_code == 200
        assert response.json()["account_status"] == "SUSPENDED"

    def test_nonexistent_msisdn_returns_404(self, api_token):
        service = CustomerService(token=api_token)
        response = service.get_customer_by_msisdn("48000000000")
        assert response.status_code == 404

    @pytest.mark.parametrize("msisdn,new_plan", [
        ("48100200301", "BiznesMAX_100GB"),
        ("48100200301", "StartGO_10GB"),
    ])
    def test_plan_change_returns_200(self, api_token, msisdn, new_plan):
        service = CustomerService(token=api_token)
        response = service.change_plan(msisdn, new_plan)
        assert response.status_code == 200
