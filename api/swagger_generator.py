"""Generate a simple Service Object skeleton from an OpenAPI JSON file.

This helper is intentionally lightweight. It is meant to speed up first-draft
Service Object creation, not to produce finished test design.

Usage:
    python api/swagger_generator.py --swagger path/to/swagger.json --tag customers

Output:
    Python source code printed to stdout.

Review generated code before copying it into the framework.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


HTTP_METHODS_WITH_BODY = {"post", "put", "patch"}
HTTP_METHODS_WITHOUT_BODY = {"get", "delete"}
SUPPORTED_HTTP_METHODS = HTTP_METHODS_WITH_BODY | HTTP_METHODS_WITHOUT_BODY


def snake_case(text: str) -> str:
    """Convert a path, operationId, or label into a simple snake_case name."""
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_").lower()


def class_name_from_tag(tag: str) -> str:
    """Convert an OpenAPI tag into a Service Object class name."""
    parts = [part for part in re.split(r"[^a-zA-Z0-9]+", tag) if part]
    return "".join(part[:1].upper() + part[1:] for part in parts) + "Service"


def load_openapi_spec(swagger_path: str | Path) -> dict[str, Any]:
    """Load an OpenAPI/Swagger JSON specification from disk."""
    path = Path(swagger_path)

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def operation_matches_tag(details: dict[str, Any], tag_filter: str) -> bool:
    """Return True when an operation contains the requested OpenAPI tag."""
    tags = details.get("tags", [])
    normalized_tags = {str(tag).lower() for tag in tags}
    return tag_filter.lower() in normalized_tags


def method_name_for_operation(
    http_method: str,
    path: str,
    details: dict[str, Any],
) -> str:
    """Return a stable Python method name for an OpenAPI operation."""
    operation_id = details.get("operationId")

    if operation_id:
        return snake_case(str(operation_id))

    return snake_case(f"{http_method}_{path}")


def render_method(http_method: str, path: str, details: dict[str, Any]) -> str:
    """Render one Service Object method as Python source text."""
    method_name = method_name_for_operation(http_method, path, details)
    summary = str(details.get("summary", "")).replace('"""', r'\"\"\"')
    has_body = http_method in HTTP_METHODS_WITH_BODY

    args = "self, payload: dict" if has_body else "self"
    body_arg = ", payload" if has_body else ""

    method_lines = [
        f"    def {method_name}({args}):",
        f'        """{summary}"""',
        f'        return self.{http_method}("{path}"{body_arg})',
        "",
    ]
    return "\n".join(method_lines)


def generate_service_class(swagger_path: str | Path, tag_filter: str) -> str:
    """Generate Python source code for one Service Object class."""
    spec = load_openapi_spec(swagger_path)
    class_name = class_name_from_tag(tag_filter)

    rendered_methods: list[str] = []

    for path, methods_dict in spec.get("paths", {}).items():
        for http_method, details in methods_dict.items():
            http_method = str(http_method).lower()

            if http_method not in SUPPORTED_HTTP_METHODS:
                continue

            if not operation_matches_tag(details, tag_filter):
                continue

            rendered_methods.append(render_method(http_method, path, details))

    methods_source = "\n".join(rendered_methods) if rendered_methods else "    pass\n"

    class_lines = [
        "from api.base_client import BaseClient",
        "",
        "",
        f"class {class_name}(BaseClient):",
        f'    """Generated from {swagger_path} using OpenAPI tag: {tag_filter}."""',
        "",
        methods_source,
    ]
    return "\n".join(class_lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Service Object skeleton from an OpenAPI JSON file."
    )
    parser.add_argument(
        "--swagger",
        required=True,
        help="Path to an OpenAPI/Swagger JSON file.",
    )
    parser.add_argument(
        "--tag",
        required=True,
        help="OpenAPI tag used to select operations.",
    )

    args = parser.parse_args()
    print(generate_service_class(args.swagger, args.tag))


if __name__ == "__main__":
    main()
