"""Small domain-neutral SQLAlchemy test-data example."""

from __future__ import annotations

import datetime

from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///testdata/testdb.db"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    """Example user record used by test-data unit tests."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String)
    status = Column(String, default="ACTIVE")


class Order(Base):
    """Example order record related to a user."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    created_date = Column(Date, nullable=False)
    status = Column(String, default="NEW")
    external_reference = Column(String)


def init_db() -> None:
    """Create tables and seed deterministic example data once."""
    Base.metadata.create_all(engine)
    session = Session()

    try:
        if session.query(User).count() == 0:
            users = [
                User(
                    external_id="USR-001",
                    full_name="Alex Morgan",
                    email="alex@example.com",
                ),
                User(
                    external_id="USR-002",
                    full_name="Taylor Reed",
                    status="INACTIVE",
                ),
                User(
                    external_id="USR-003",
                    full_name="Jordan Lee",
                    email="jordan@example.com",
                    status="SUSPENDED",
                ),
            ]
            session.add_all(users)

            orders = [
                Order(
                    user_id=1,
                    total_amount=49.99,
                    created_date=datetime.date(2026, 1, 15),
                    status="NEW",
                ),
                Order(
                    user_id=1,
                    total_amount=99.99,
                    created_date=datetime.date(2026, 1, 10),
                    status="COMPLETED",
                    external_reference="EXT-ORDER-001",
                ),
                Order(
                    user_id=3,
                    total_amount=24.99,
                    created_date=datetime.date(2026, 1, 5),
                    status="CANCELLED",
                    external_reference="EXT-ORDER-002",
                ),
            ]
            session.add_all(orders)
            session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    print("Test database initialized.")
