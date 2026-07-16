"""Integration tests for UserService."""

import httpx
import pytest

from api.users_service import UserCreate, UserService, UserUpdate


class TestUserServiceHealth:
    def test_health_check_returns_ok(
        self,
        user_service: UserService,
    ) -> None:
        health = user_service.health_check()

        assert health.status == "ok"
        assert health.service == "users"
        assert health.port == 8001


class TestUserServiceCrud:
    def test_create_returns_user_with_id(
        self,
        clean_users,
        user_service: UserService,
    ) -> None:
        user = user_service.create(
            UserCreate(
                full_name="Alex Morgan",
                external_id="USR-1001",
            )
        )

        assert user.id > 0
        assert user.full_name == "Alex Morgan"
        assert user.external_id == "USR-1001"
        assert user.status == "ACTIVE"
        assert len(user_service.get_all()) == 1

    def test_get_returns_existing_user(
        self,
        clean_users,
        user_service: UserService,
    ) -> None:
        created = user_service.create(
            UserCreate(
                full_name="Taylor Reed",
                external_id="USR-1002",
            )
        )

        fetched = user_service.get(created.id)

        assert fetched.id == created.id
        assert fetched.full_name == "Taylor Reed"
        assert fetched.external_id == "USR-1002"

    def test_get_all_returns_all_users(
        self,
        clean_users,
        user_service: UserService,
    ) -> None:
        user_service.create(
            UserCreate(
                full_name="User A",
                external_id="USR-A",
            )
        )
        user_service.create(
            UserCreate(
                full_name="User B",
                external_id="USR-B",
            )
        )

        users = user_service.get_all()

        assert len(users) == 2
        external_ids = {user.external_id for user in users}
        assert external_ids == {"USR-A", "USR-B"}

    def test_update_changes_user_fields(
        self,
        clean_users,
        user_service: UserService,
    ) -> None:
        created = user_service.create(
            UserCreate(
                full_name="Alex Morgan",
                external_id="USR-1001",
            )
        )

        updated = user_service.update(
            created.id,
            UserUpdate(
                full_name="Alex Morgan Updated",
                email="alex.updated@example.com",
                status="INACTIVE",
            ),
        )

        assert updated.full_name == "Alex Morgan Updated"
        assert updated.email == "alex.updated@example.com"
        assert updated.status == "INACTIVE"
        assert updated.external_id == "USR-1001"

    def test_delete_removes_user(
        self,
        clean_users,
        user_service: UserService,
    ) -> None:
        created = user_service.create(
            UserCreate(
                full_name="Temporary User",
                external_id="USR-DELETE",
            )
        )

        user_service.delete(created.id)

        assert user_service.get_all() == []


class TestUserServiceNegative:
    def test_get_nonexistent_id_raises_404(
        self,
        clean_users,
        user_service: UserService,
    ) -> None:
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            user_service.get(9999)

        assert exc_info.value.response.status_code == 404

    def test_delete_nonexistent_id_raises_404(
        self,
        clean_users,
        user_service: UserService,
    ) -> None:
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            user_service.delete(9999)

        assert exc_info.value.response.status_code == 404


class TestUserPayloadVariants:
    @pytest.mark.parametrize(
        "full_name,external_id,email,status",
        [
            (
                "Alex Morgan",
                "USR-ACTIVE",
                "alex@example.com",
                "ACTIVE",
            ),
            (
                "Taylor Reed",
                "USR-INACTIVE",
                None,
                "INACTIVE",
            ),
            (
                "Jordan Lee",
                "USR-SUSPENDED",
                "jordan@example.com",
                "SUSPENDED",
            ),
        ],
        ids=[
            "active_with_email",
            "inactive_without_email",
            "suspended_with_email",
        ],
    )
    def test_create_user_payload_variant(
        self,
        clean_users,
        user_service: UserService,
        full_name: str,
        external_id: str,
        email: str | None,
        status: str,
    ) -> None:
        user = user_service.create(
            UserCreate(
                full_name=full_name,
                external_id=external_id,
                email=email,
                status=status,
            )
        )

        assert user.full_name == full_name
        assert user.external_id == external_id
        assert user.email == email
        assert user.status == status

        fetched = user_service.get(user.id)
        assert fetched.external_id == external_id
