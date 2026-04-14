"""
mock_responses.py
Statyczne mockowane odpowiedzi API — uzywane w testach izolowanych od backendu.
Wzorzec: slowniki gotowe do wstrzyklniecia przez Playwright route() lub httpx mock.
"""

MOCK_CUSTOMER_ACTIVE = {
    "msisdn": "48100200301",
    "full_name": "Jan Kowalski",
    "contract_type": "POSTPAID",
    "plan": "BiznesMAX_50GB",
    "account_status": "ACTIVE"
}

MOCK_CUSTOMER_SUSPENDED = {
    "msisdn": "48100200303",
    "full_name": "Piotr Wisniewski",
    "contract_type": "POSTPAID",
    "plan": "BiznesMAX_100GB",
    "account_status": "SUSPENDED"
}

MOCK_INVOICE_OVERDUE = {
    "invoice_id": "INV-2025-003",
    "customer_id": 3,
    "amount": 249.99,
    "due_date": "2025-06-15",
    "status": "OVERDUE"
}

MOCK_LOGIN_SUCCESS = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock",
    "role": "AGENT",
    "expires_in": 3600
}

MOCK_LOGIN_FAILURE = {
    "error": "INVALID_CREDENTIALS",
    "message": "Nieprawidlowy login lub haslo."
}
