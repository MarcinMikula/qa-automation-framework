"""
swagger_generator.py
Narzedzie pomocnicze — generuje szkielet klasy Service Object na podstawie
pliku OpenAPI (swagger.json).

Uzycie:
    python api/swagger_generator.py --swagger path/do/swagger.json --tag customers

Wynik: gotowy kod klasy wypisany na stdout — mozesz go skopiowac do nowego pliku.
"""
import json
import argparse


def snake_case(text: str) -> str:
    return text.lower().replace("-", "_").replace(" ", "_").replace("/", "_")


def generate_service_class(swagger_path: str, tag_filter: str):
    with open(swagger_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    class_name = tag_filter.capitalize() + "Service"
    methods = []

    for path, methods_dict in spec.get("paths", {}).items():
        for http_method, details in methods_dict.items():
            tags = details.get("tags", [])
            if tag_filter.lower() not in [t.lower() for t in tags]:
                continue

            operation_id = details.get("operationId", snake_case(f"{http_method}_{path}"))
            summary = details.get("summary", "")
            method_name = snake_case(operation_id)

            has_body = http_method in ("post", "put", "patch")
            args = "self, payload: dict" if has_body else "self"
            body_arg = ", payload" if has_body else ""

            method = (
                f"
    def {method_name}({args}):
"
                f'        """{summary}"""
'
                f'        return self.{http_method}("{path}"{body_arg})
'
            )
            methods.append(method)

    output = (
        f"from api.base_client import BaseClient


"
        f"class {class_name}(BaseClient):
"
        f'    """Wygenerowano automatycznie z: {swagger_path} (tag: {tag_filter})"""
'
    )
    for m in methods:
        output += m

    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generuj Service Object z OpenAPI JSON")
    parser.add_argument("--swagger", required=True, help="Sciezka do pliku swagger.json")
    parser.add_argument("--tag", required=True, help="Tag OpenAPI do filtrowania endpointow")
    args = parser.parse_args()
    generate_service_class(args.swagger, args.tag)
