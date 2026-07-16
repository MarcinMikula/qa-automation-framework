"""Unit tests for the domain-neutral SQLAlchemy test-data example."""

import datetime
from unittest.mock import MagicMock

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

import testdata.testdb as testdb
from testdata.testdb import Order, User, init_db


class TestSchema:
    def test_user_table_is_created(self, seeded_db) -> None:
        assert "users" in inspect(seeded_db).get_table_names()

    def test_order_table_is_created(self, seeded_db) -> None:
        assert "orders" in inspect(seeded_db).get_table_names()


class TestModelDefaults:
    def test_user_default_status_is_active(
        self,
        empty_db,
        db_session,
    ) -> None:
        user = User(
            external_id="USR-DEFAULT",
            full_name="Test User",
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.status == "ACTIVE"

    def test_order_default_status_is_new(
        self,
        empty_db,
        db_session,
    ) -> None:
        user = User(
            external_id="USR-ORDER-OWNER",
            full_name="Order Owner",
        )
        db_session.add(user)
        db_session.flush()

        order = Order(
            user_id=user.id,
            total_amount=50.0,
            created_date=datetime.date(2026, 1, 1),
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        assert order.status == "NEW"


class TestModelConstraints:
    def test_user_external_id_must_be_unique(
        self,
        empty_db,
        db_session,
    ) -> None:
        db_session.add(
            User(
                external_id="USR-DUPLICATE",
                full_name="First User",
            )
        )
        db_session.add(
            User(
                external_id="USR-DUPLICATE",
                full_name="Second User",
            )
        )

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()

    def test_user_external_id_cannot_be_null(
        self,
        empty_db,
        db_session,
    ) -> None:
        db_session.add(User(full_name="No External ID"))

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()

    def test_user_full_name_cannot_be_null(
        self,
        empty_db,
        db_session,
    ) -> None:
        db_session.add(User(external_id="USR-NO-NAME"))

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()

    def test_order_total_amount_cannot_be_null(
        self,
        empty_db,
        db_session,
    ) -> None:
        user = User(
            external_id="USR-AMOUNT",
            full_name="Order Owner",
        )
        db_session.add(user)
        db_session.flush()
        db_session.add(
            Order(
                user_id=user.id,
                created_date=datetime.date(2026, 1, 1),
            )
        )

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()

    def test_order_created_date_cannot_be_null(
        self,
        empty_db,
        db_session,
    ) -> None:
        user = User(
            external_id="USR-DATE",
            full_name="Order Owner",
        )
        db_session.add(user)
        db_session.flush()
        db_session.add(
            Order(
                user_id=user.id,
                total_amount=10.0,
            )
        )

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()


class TestInitDbSeed:
    def test_init_db_seeds_exactly_three_users(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            assert session.query(User).count() == 3
        finally:
            session.close()

    def test_init_db_seeds_exactly_three_orders(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            assert session.query(Order).count() == 3
        finally:
            session.close()

    def test_seeded_active_user_attributes(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            user = (
                session.query(User)
                .filter_by(external_id="USR-001")
                .one()
            )
            assert user.full_name == "Alex Morgan"
            assert user.email == "alex@example.com"
            assert user.status == "ACTIVE"
        finally:
            session.close()

    def test_seeded_user_can_be_inactive(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            user = (
                session.query(User)
                .filter_by(external_id="USR-002")
                .one()
            )
            assert user.status == "INACTIVE"
            assert user.email is None
        finally:
            session.close()

    def test_seeded_user_can_be_suspended(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            user = (
                session.query(User)
                .filter_by(external_id="USR-003")
                .one()
            )
            assert user.status == "SUSPENDED"
        finally:
            session.close()

    def test_seeded_new_order_for_user_1(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            order = (
                session.query(Order)
                .filter_by(user_id=1, status="NEW")
                .one()
            )
            assert order.total_amount == 49.99
            assert order.created_date == datetime.date(2026, 1, 15)
            assert order.external_reference is None
        finally:
            session.close()

    def test_seeded_completed_order_for_user_1(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            order = (
                session.query(Order)
                .filter_by(user_id=1, status="COMPLETED")
                .one()
            )
            assert order.total_amount == 99.99
            assert order.external_reference == "EXT-ORDER-001"
        finally:
            session.close()

    def test_seeded_cancelled_order_for_user_3(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            order = (
                session.query(Order)
                .filter_by(user_id=3, status="CANCELLED")
                .one()
            )
            assert order.total_amount == 24.99
            assert order.external_reference == "EXT-ORDER-002"
        finally:
            session.close()

    def test_user_2_has_no_orders(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            assert session.query(Order).filter_by(user_id=2).count() == 0
        finally:
            session.close()

    def test_user_1_has_two_orders(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            assert session.query(Order).filter_by(user_id=1).count() == 2
        finally:
            session.close()


class TestInitDbIdempotency:
    def test_init_db_is_idempotent_for_users(self, seeded_db) -> None:
        init_db()
        session = testdb.Session()
        try:
            assert session.query(User).count() == 3
        finally:
            session.close()

    def test_init_db_is_idempotent_for_orders(self, seeded_db) -> None:
        init_db()
        session = testdb.Session()
        try:
            assert session.query(Order).count() == 3
        finally:
            session.close()

    def test_init_db_does_not_modify_existing_user_data(
        self,
        seeded_db,
    ) -> None:
        session = testdb.Session()
        try:
            user = (
                session.query(User)
                .filter_by(external_id="USR-001")
                .one()
            )
            user.full_name = "Changed Name"
            session.commit()
        finally:
            session.close()

        init_db()

        session = testdb.Session()
        try:
            user = (
                session.query(User)
                .filter_by(external_id="USR-001")
                .one()
            )
            assert user.full_name == "Changed Name"
            assert session.query(User).count() == 3
        finally:
            session.close()


class TestDataIntegrity:
    def test_all_seeded_orders_reference_existing_users(
        self,
        seeded_db,
    ) -> None:
        session = testdb.Session()
        try:
            user_ids = {user.id for user in session.query(User).all()}
            for order in session.query(Order).all():
                assert order.user_id in user_ids
        finally:
            session.close()

    def test_seeded_external_ids_are_unique(self, seeded_db) -> None:
        session = testdb.Session()
        try:
            external_ids = [
                user.external_id for user in session.query(User).all()
            ]
            assert len(external_ids) == len(set(external_ids))
        finally:
            session.close()

    def test_seeded_order_statuses_cover_main_variants(
        self,
        seeded_db,
    ) -> None:
        session = testdb.Session()
        try:
            statuses = {
                order.status for order in session.query(Order).all()
            }
            assert statuses == {"NEW", "COMPLETED", "CANCELLED"}
        finally:
            session.close()


class TestSessionLifecycle:
    def test_init_db_closes_session(
        self,
        memory_engine,
        monkeypatch,
    ) -> None:
        mock_session = MagicMock()
        mock_session.query.return_value.count.return_value = 0
        mock_session_factory = MagicMock(return_value=mock_session)
        monkeypatch.setattr(testdb, "Session", mock_session_factory)

        init_db()

        mock_session.close.assert_called_once()
