"""
test_users_api.py
Testy integracyjne UserService — mikroserwis users (port 8001).

Uruchomienie:
    pytest tests/integration/test_users_api.py -v
"""
import httpx
import pytest

from api.users_service import UserCreate, UserService, UserUpdate


class TestUserServiceHealth:
    """Testy endpointu /health."""

    def test_health_check_returns_ok(self, user_service: UserService):
        """health_check zwraca status ok i nazwę serwisu users."""
        health = user_service.health_check()

        assert health.status == "ok"
        assert health.service == "users"
        assert health.port == 8001


class TestUserServiceCrud:
    """[DOMAIN: GENERIC] Testy pełnego cyklu CRUD przez SOM."""

    def test_create_returns_user_with_id(self, clean_users, user_service: UserService):
        """create dodaje użytkownika i zwraca model z nadanym id."""
        user = user_service.create(
            UserCreate(full_name="Jan Kowalski", msisdn="48100200301")
        )

        assert user.id > 0
        assert user.full_name == "Jan Kowalski"
        assert user.msisdn == "48100200301"
        assert len(user_service.get_all()) == 1

    def test_get_returns_existing_user(self, clean_users, user_service: UserService):
        """get pobiera użytkownika po id."""
        created = user_service.create(
            UserCreate(full_name="Anna Nowak", msisdn="48100200302")
        )

        fetched = user_service.get(created.id)

        assert fetched.id == created.id
        assert fetched.full_name == "Anna Nowak"

    def test_get_all_returns_all_users(self, clean_users, user_service: UserService):
        """get_all zwraca listę wszystkich użytkowników."""
        user_service.create(UserCreate(full_name="User A", msisdn="48100111111"))
        user_service.create(UserCreate(full_name="User B", msisdn="48100222222"))

        users = user_service.get_all()

        assert len(users) == 2
        msisdns = {u.msisdn for u in users}
        assert msisdns == {"48100111111", "48100222222"}

    def test_update_changes_user_fields(self, clean_users, user_service: UserService):
        """update modyfikuje pola użytkownika (PUT)."""
        created = user_service.create(
            UserCreate(
                full_name="Jan Kowalski",
                msisdn="48100200301",
                plan="StartGO_10GB",
            )
        )

        updated = user_service.update(
            created.id,
            UserUpdate(full_name="Jan Kowalski Zmieniony", plan="BiznesMAX_50GB"),
        )

        assert updated.full_name == "Jan Kowalski Zmieniony"
        assert updated.plan == "BiznesMAX_50GB"
        assert updated.msisdn == "48100200301"

    def test_delete_removes_user(self, clean_users, user_service: UserService):
        """delete usuwa użytkownika — get_all jest puste po usunięciu."""
        created = user_service.create(
            UserCreate(full_name="Do usunięcia", msisdn="48100999999")
        )

        user_service.delete(created.id)

        assert user_service.get_all() == []


class TestUserServiceNegative:
    """[DOMAIN: GENERIC] Scenariusze negatywne — nieistniejące zasoby."""

    def test_get_nonexistent_id_raises_404(self, clean_users, user_service: UserService):
        """get nieistniejącego id zwraca HTTP 404."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            user_service.get(9999)

        assert exc_info.value.response.status_code == 404

    def test_delete_nonexistent_id_raises_404(self, clean_users, user_service: UserService):
        """delete nieistniejącego id zwraca HTTP 404."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            user_service.delete(9999)

        assert exc_info.value.response.status_code == 404


class TestTelcoUserProfiles:
    """[DOMAIN: TELCO] Profile abonentów — prepaid/postpaid, plany, status konta."""

    @pytest.mark.parametrize(
        "full_name,msisdn,contract_type,plan,account_status",
        [
            ("Jan Kowalski", "48100200301", "POSTPAID", "BiznesMAX_50GB", "ACTIVE"),
            ("Anna Nowak", "48100200302", "PREPAID", "StartGO_10GB", "ACTIVE"),
            ("Piotr Wisniewski", "48100200303", "POSTPAID", "BiznesMAX_100GB", "SUSPENDED"),
        ],
        ids=["postpaid_active", "prepaid_active", "postpaid_suspended"],
    )
    def test_create_telco_user_profile(
        self,
        clean_users,
        user_service: UserService,
        full_name: str,
        msisdn: str,
        contract_type: str,
        plan: str,
        account_status: str,
    ):
        """[DOMAIN: TELCO] Tworzenie abonenta z polami MSISDN, planem i statusem konta."""
        user = user_service.create(
            UserCreate(
                full_name=full_name,
                msisdn=msisdn,
                contract_type=contract_type,
                plan=plan,
                account_status=account_status,
            )
        )

        assert user.contract_type == contract_type
        assert user.plan == plan
        assert user.account_status == account_status
        assert user.msisdn == msisdn

        fetched = user_service.get(user.id)
        assert fetched.full_name == full_name
