"""Unit tests for the reusable in-memory service store."""

from services.common.store import InMemoryStore


class TestInMemoryStoreCreateAndRead:
    def test_new_store_starts_empty(self):
        store = InMemoryStore()

        assert store.list_all() == []
        assert store.count() == 0

    def test_create_assigns_incrementing_ids(self):
        store = InMemoryStore()

        first = store.create({"name": "First"})
        second = store.create({"name": "Second"})

        assert first == {"name": "First", "id": 1}
        assert second == {"name": "Second", "id": 2}
        assert store.count() == 2

    def test_get_returns_existing_item(self):
        store = InMemoryStore()
        created = store.create({"name": "Existing"})

        assert store.get(created["id"]) == created

    def test_get_returns_none_for_missing_item(self):
        store = InMemoryStore()

        assert store.get(999) is None


class TestInMemoryStoreUpdate:
    def test_update_merges_payload_and_preserves_id(self):
        store = InMemoryStore()
        created = store.create({"name": "Old", "status": "NEW"})

        updated = store.update(created["id"], {"name": "New"})

        assert updated == {"name": "New", "status": "NEW", "id": created["id"]}
        assert store.get(created["id"]) == updated

    def test_update_returns_none_for_missing_item(self):
        store = InMemoryStore()

        assert store.update(999, {"name": "Missing"}) is None


class TestInMemoryStoreDelete:
    def test_delete_removes_existing_item(self):
        store = InMemoryStore()
        created = store.create({"name": "To delete"})

        deleted = store.delete(created["id"])

        assert deleted is True
        assert store.get(created["id"]) is None
        assert store.count() == 0

    def test_delete_returns_false_for_missing_item(self):
        store = InMemoryStore()

        assert store.delete(999) is False

    def test_delete_does_not_reuse_ids(self):
        store = InMemoryStore()
        first = store.create({"name": "First"})
        store.delete(first["id"])

        second = store.create({"name": "Second"})

        assert second["id"] == 2
