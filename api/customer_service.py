"""
customer_service.py
Service Object dla endpointow zarzadzania klientem.
Kontekst: CRM telco — wyszukiwanie po MSISDN, zmiana planu, zawieszenie konta.
"""
from api.base_client import BaseClient


class CustomerService(BaseClient):
    ENDPOINT_CUSTOMERS = "/customers"

    def get_customer_by_msisdn(self, msisdn: str):
        return self.get(f"{self.ENDPOINT_CUSTOMERS}/{msisdn}")

    def change_plan(self, msisdn: str, new_plan: str):
        return self.patch(f"{self.ENDPOINT_CUSTOMERS}/{msisdn}/plan", {
            "plan": new_plan
        })

    def suspend_account(self, msisdn: str, reason: str):
        return self.patch(f"{self.ENDPOINT_CUSTOMERS}/{msisdn}/status", {
            "status": "SUSPENDED",
            "reason": reason
        })
