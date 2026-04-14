"""
testdb.py
Plikowa baza danych SQLAlchemy z przykładowymi danymi testowymi.
Kontekst: system billingowy telco — klienci, kontrakty, faktury.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

DATABASE_URL = "sqlite:///testdata/testdb.db"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    msisdn = Column(String, unique=True, nullable=False)   # np. 48100200300
    full_name = Column(String, nullable=False)
    contract_type = Column(String)                          # PREPAID / POSTPAID
    plan = Column(String)                                   # np. "BiznesMAX_50GB"
    account_status = Column(String, default="ACTIVE")       # ACTIVE / SUSPENDED


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String, default="UNPAID")               # UNPAID / PAID / OVERDUE


def init_db():
    """Tworzy tabele i wstawia przykładowe dane testowe."""
    Base.metadata.create_all(engine)
    session = Session()

    if session.query(Customer).count() == 0:
        customers = [
            Customer(msisdn="48100200301", full_name="Jan Kowalski",
                     contract_type="POSTPAID", plan="BiznesMAX_50GB"),
            Customer(msisdn="48100200302", full_name="Anna Nowak",
                     contract_type="PREPAID", plan="StartGO_10GB"),
            Customer(msisdn="48100200303", full_name="Piotr Wisniewski",
                     contract_type="POSTPAID", plan="BiznesMAX_100GB",
                     account_status="SUSPENDED"),
        ]
        session.add_all(customers)

        invoices = [
            Invoice(customer_id=1, amount=129.99,
                    due_date=datetime.date(2025, 8, 15), status="UNPAID"),
            Invoice(customer_id=1, amount=129.99,
                    due_date=datetime.date(2025, 7, 15), status="PAID"),
            Invoice(customer_id=3, amount=249.99,
                    due_date=datetime.date(2025, 6, 15), status="OVERDUE"),
        ]
        session.add_all(invoices)
        session.commit()

    session.close()


if __name__ == "__main__":
    init_db()
    print("Baza danych zainicjalizowana.")
