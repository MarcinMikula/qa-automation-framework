"""Unit tests for the lightweight OpenAPI/Swagger Service Object generator."""

import json

from api.swagger_generator import (
    class_name_from_tag,
    generate_service_class,
    method_name_for_operation,
    operation_matches_tag,
    render_method,
    snake_case,
)


class TestNameHelpers:
    def test_snake_case_normalizes_paths_and_parameters(self):
        assert snake_case("GET /customers/{customerId}/orders") == "get_customers_customerid_orders"

    def test_snake_case_collapses_repeated_separators(self):
        assert snake_case("Create---Customer__Order") == "create_customer_order"

    def test_class_name_from_tag_builds_service_class_name(self):
        assert class_name_from_tag("customer orders") == "CustomerOrdersService"


class TestOperationFiltering:
    def test_operation_matches_tag_case_insensitively(self):
        details = {"tags": ["Customers", "Orders"]}

        assert operation_matches_tag(details, "customers") is True

    def test_operation_does_not_match_missing_tag(self):
        details = {"tags": ["Customers"]}

        assert operation_matches_tag(details, "orders") is False

    def test_operation_without_tags_does_not_match(self):
        assert operation_matches_tag({}, "customers") is False


class TestMethodNameGeneration:
    def test_method_name_prefers_operation_id(self):
        details = {"operationId": "createCustomerOrder"}

        assert method_name_for_operation("post", "/orders", details) == "createcustomerorder"

    def test_method_name_falls_back_to_http_method_and_path(self):
        details = {}

        assert method_name_for_operation("get", "/customers/{id}", details) == "get_customers_id"


class TestMethodRendering:
    def test_render_get_method_without_payload(self):
        source = render_method(
            "get",
            "/customers",
            {"operationId": "listCustomers", "summary": "List customers"},
        )

        assert "def listcustomers(self):" in source
        assert '"""List customers"""' in source
        assert 'return self.get("/customers")' in source
        assert "payload" not in source

    def test_render_post_method_with_payload(self):
        source = render_method(
            "post",
            "/customers",
            {"operationId": "createCustomer", "summary": "Create customer"},
        )

        assert "def createcustomer(self, payload: dict):" in source
        assert 'return self.post("/customers", payload)' in source


class TestServiceClassGeneration:
    def test_generate_service_class_filters_by_tag_and_supported_methods(self, tmp_path):
        swagger_path = tmp_path / "openapi.json"
        swagger_path.write_text(
            json.dumps(
                {
                    "paths": {
                        "/customers": {
                            "get": {
                                "tags": ["customers"],
                                "operationId": "listCustomers",
                                "summary": "List customers",
                            },
                            "post": {
                                "tags": ["customers"],
                                "operationId": "createCustomer",
                                "summary": "Create customer",
                            },
                        },
                        "/customers/{id}": {
                            "put": {
                                "tags": ["customers"],
                                "operationId": "replaceCustomer",
                                "summary": "Replace customer",
                            },
                            "delete": {
                                "tags": ["customers"],
                                "operationId": "deleteCustomer",
                                "summary": "Delete customer",
                            },
                        },
                        "/orders": {
                            "get": {
                                "tags": ["orders"],
                                "operationId": "listOrders",
                                "summary": "List orders",
                            },
                        },
                    }
                }
            ),
            encoding="utf-8",
        )

        source = generate_service_class(swagger_path, "customers")

        assert "from api.base_client import BaseClient" in source
        assert "class CustomersService(BaseClient):" in source
        assert "def listcustomers(self):" in source
        assert 'return self.get("/customers")' in source
        assert "def createcustomer(self, payload: dict):" in source
        assert 'return self.post("/customers", payload)' in source
        assert "def replacecustomer(self, payload: dict):" in source
        assert 'return self.put("/customers/{id}", payload)' in source
        assert "def deletecustomer(self):" in source
        assert 'return self.delete("/customers/{id}")' in source
        assert "listorders" not in source

    def test_generate_service_class_ignores_unsupported_methods(self, tmp_path):
        swagger_path = tmp_path / "openapi.json"
        swagger_path.write_text(
            json.dumps(
                {
                    "paths": {
                        "/customers": {
                            "options": {
                                "tags": ["customers"],
                                "operationId": "customerOptions",
                                "summary": "Options",
                            }
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        source = generate_service_class(swagger_path, "customers")

        assert "class CustomersService(BaseClient):" in source
        assert "pass" in source
        assert "customeroptions" not in source

    def test_generate_service_class_uses_pass_when_tag_has_no_operations(self, tmp_path):
        swagger_path = tmp_path / "openapi.json"
        swagger_path.write_text(
            json.dumps(
                {
                    "paths": {
                        "/orders": {
                            "get": {
                                "tags": ["orders"],
                                "operationId": "listOrders",
                                "summary": "List orders",
                            }
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        source = generate_service_class(swagger_path, "customers")

        assert "class CustomersService(BaseClient):" in source
        assert "pass" in source
        assert "listorders" not in source
