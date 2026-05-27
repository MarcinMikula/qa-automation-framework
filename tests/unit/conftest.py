"""
conftest.py — fixtures dla testów jednostkowych testdb (izolacja :memory:).
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import testdata.testdb as testdb
from testdata.testdb import init_db


@pytest.fixture
def memory_engine(monkeypatch):
    """Współdzielona baza SQLite w pamięci — jeden engine na test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    monkeypatch.setattr(testdb, "engine", engine)
    monkeypatch.setattr(testdb, "Session", sessionmaker(bind=engine))
    yield engine
    engine.dispose()


@pytest.fixture
def empty_db(memory_engine):
    """Tabele utworzone, bez danych seed."""
    testdb.Base.metadata.create_all(memory_engine)
    return memory_engine


@pytest.fixture
def seeded_db(memory_engine):
    """Tabele utworzone i init_db() wywołane raz."""
    init_db()
    return memory_engine


@pytest.fixture
def db_session(memory_engine):
    """Sesja ORM powiązana z izolowanym engine."""
    session = testdb.Session()
    yield session
    session.close()
