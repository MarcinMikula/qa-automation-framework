"""
test_testdb.py
Unit testy modułu testdata/testdb.py — modele, constrainty, seed, idempotentność.

Uruchomienie (bez ładowania tests/conftest.py z Playwright/API):
    pytest tests/unit/ --confcutdir=tests/unit -v
"""
import datetime
from unittest.mock import MagicMock

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

import testdata.testdb as testdb
from testdata.testdb import Customer, Invoice, init_db


class TestSchema:
    def test_customer_table_is_created(self, seeded_db):
        assert "customers" in inspect(seeded_db).get_table_names()

    def test_invoice_table_is_created(self, seeded_db):
        assert "invoices" in inspect(seeded_db).get_table_names()


class TestModelDefaults:
    def test_customer_default_account_status_is_active(self, empty_db, db_session):
        customer = Customer(msisdn="48999000001", full_name="Test User")
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
        assert customer.account_status == "ACTIVE"

    def test_invoice_default_status_is_unpaid(self, empty_db, db_session):
        customer = Customer(msisdn="48999000002", full_name="Invoice Owner")
        db_session.add(customer)
        db_session.flush()
        invoice = Invoice(
            customer_id=customer.id,
            amount=50.0,
            due_date=datetime.date(2025, 1, 1),
        )
        db_session.add(invoice)
        db_session.commit()
        db_session.refresh(invoice)
        assert invoice.status == "UNPAID"


class TestModelConstraints:
    def test_customer_msisdn_must_be_unique(self, empty_db, db_session):
        db_session.add(Customer(msisdn="48111111111", full_name="First"))
        db_session.add(Customer(msisdn="48111111111", full_name="Second"))
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_customer_msisdn_cannot_be_null(self, empty_db, db_session):
        db_session.add(Customer(full_name="No MSISDN"))
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_customer_full_name_cannot_be_null(self, empty_db, db_session):
        db_session.add(Customer(msisdn="48122222222"))
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_invoice_amount_cannot_be_null(self, empty_db, db_session):
        customer = Customer(msisdn="48133333333", full_name="Owner")
        db_session.add(customer)
        db_session.flush()
        db_session.add(
            Invoice(customer_id=customer.id, due_date=datetime.date(2025, 1, 1))
        )
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_invoice_due_date_cannot_be_null(self, empty_db, db_session):
        customer = Customer(msisdn="48144444444", full_name="Owner")
        db_session.add(customer)
        db_session.flush()
        db_session.add(Invoice(customer_id=customer.id, amount=10.0))
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()


class TestInitDbSeed:
    def test_init_db_seeds_exactly_three_customers(self, seeded_db):
        session = testdb.Session()
        try:
            assert session.query(Customer).count() == 3
        finally:
            session.close()

    def test_init_db_seeds_exactly_three_invoices(self, seeded_db):
        session = testdb.Session()
        try:
            assert session.query(Invoice).count() == 3
        finally:
            session.close()

    def test_seeded_customer_jan_kowalski_attributes(self, seeded_db):
        session = testdb.Session()
        try:
            customer = session.query(Customer).filter_by(msisdn="48100200301").one()
            assert customer.full_name == "Jan Kowalski"
            assert customer.contract_type == "POSTPAID"
            assert customer.plan == "BiznesMAX_50GB"
            assert customer.account_status == "ACTIVE"
        finally:
            session.close()

    def test_seeded_customer_anna_nowak_is_prepaid(self, seeded_db):
        session = testdb.Session()
        try:
            customer = session.query(Customer).filter_by(msisdn="48100200302").one()
            assert customer.contract_type == "PREPAID"
            assert customer.plan == "StartGO_10GB"
        finally:
            session.close()

    def test_seeded_customer_piotr_is_suspended(self, seeded_db):
        session = testdb.Session()
        try:
            customer = session.query(Customer).filter_by(msisdn="48100200303").one()
            assert customer.account_status == "SUSPENDED"
        finally:
            session.close()

    def test_seeded_invoice_unpaid_for_customer_1(self, seeded_db):
        session = testdb.Session()
        try:
            invoice = (
                session.query(Invoice)
                .filter_by(customer_id=1, status="UNPAID")
                .one()
            )
            assert invoice.amount == 129.99
            assert invoice.due_date == datetime.date(2025, 8, 15)
        finally:
            session.close()

    def test_seeded_invoice_paid_for_customer_1(self, seeded_db):
        session = testdb.Session()
        try:
            invoice = (
                session.query(Invoice)
                .filter_by(customer_id=1, status="PAID")
                .one()
            )
            assert invoice.amount == 129.99
            assert invoice.due_date == datetime.date(2025, 7, 15)
        finally:
            session.close()

    def test_seeded_invoice_overdue_for_customer_3(self, seeded_db):
        session = testdb.Session()
        try:
            invoice = (
                session.query(Invoice)
                .filter_by(customer_id=3, status="OVERDUE")
                .one()
            )
            assert invoice.amount == 249.99
            assert invoice.due_date == datetime.date(2025, 6, 15)
        finally:
            session.close()

    def test_customer_2_has_no_invoices(self, seeded_db):
        session = testdb.Session()
        try:
            assert session.query(Invoice).filter_by(customer_id=2).count() == 0
        finally:
            session.close()

    def test_customer_1_has_two_invoices(self, seeded_db):
        session = testdb.Session()
        try:
            assert session.query(Invoice).filter_by(customer_id=1).count() == 2
        finally:
            session.close()


class TestInitDbIdempotency:
    def test_init_db_is_idempotent_for_customers(self, seeded_db):
        init_db()
        session = testdb.Session()
        try:
            assert session.query(Customer).count() == 3
        finally:
            session.close()

    def test_init_db_is_idempotent_for_invoices(self, seeded_db):
        init_db()
        session = testdb.Session()
        try:
            assert session.query(Invoice).count() == 3
        finally:
            session.close()

    def test_init_db_does_not_modify_existing_customer_data(self, seeded_db):
        session = testdb.Session()
        try:
            customer = session.query(Customer).filter_by(msisdn="48100200301").one()
            customer.full_name = "Zmienione Imie"
            session.commit()
        finally:
            session.close()

        init_db()

        session = testdb.Session()
        try:
            customer = session.query(Customer).filter_by(msisdn="48100200301").one()
            assert customer.full_name == "Zmienione Imie"
            assert session.query(Customer).count() == 3
        finally:
            session.close()


class TestDataIntegrity:
    def test_all_seeded_invoices_reference_existing_customers(self, seeded_db):
        session = testdb.Session()
        try:
            customer_ids = {c.id for c in session.query(Customer).all()}
            for invoice in session.query(Invoice).all():
                assert invoice.customer_id in customer_ids
        finally:
            session.close()

    def test_seeded_msisdns_are_unique(self, seeded_db):
        session = testdb.Session()
        try:
            msisdns = [c.msisdn for c in session.query(Customer).all()]
            assert len(msisdns) == len(set(msisdns))
        finally:
            session.close()

    def test_seeded_invoice_statuses_cover_unpaid_paid_overdue(self, seeded_db):
        session = testdb.Session()
        try:
            statuses = {i.status for i in session.query(Invoice).all()}
            assert statuses == {"UNPAID", "PAID", "OVERDUE"}
        finally:
            session.close()


class TestSessionLifecycle:
    def test_init_db_closes_session(self, memory_engine, monkeypatch):
        mock_session = MagicMock()
        mock_session.query.return_value.count.return_value = 0
        mock_session_factory = MagicMock(return_value=mock_session)
        monkeypatch.setattr(testdb, "Session", mock_session_factory)

        init_db()

        mock_session.close.assert_called_once()
