"""
store.py
[DOMAIN: GENERIC] Magazyn w pamięci (dict) — wspólny dla wszystkich mikroserwisów.
"""
from typing import Any


class InMemoryStore:
    """Prosty magazyn klucz-wartość z autoinkrementowanym ID."""

    def __init__(self) -> None:
        self._data: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def list_all(self) -> list[dict[str, Any]]:
        return list(self._data.values())

    def get(self, item_id: int) -> dict[str, Any] | None:
        return self._data.get(item_id)

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        item = {**payload, "id": self._next_id}
        self._data[self._next_id] = item
        self._next_id += 1
        return item

    def update(self, item_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        if item_id not in self._data:
            return None
        updated = {**self._data[item_id], **payload, "id": item_id}
        self._data[item_id] = updated
        return updated

    def delete(self, item_id: int) -> bool:
        if item_id not in self._data:
            return False
        del self._data[item_id]
        return True

    def count(self) -> int:
        return len(self._data)
