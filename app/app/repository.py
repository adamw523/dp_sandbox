from sqlmodel import Field, Session, SQLModel, create_engine, select
import uuid

from config import Config
from models import Customer, CustomerCreate


# connect_args = {"check_same_thread": False}
connect_args = {}
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI, echo=True, connect_args=connect_args
)


def create_customer(customer: CustomerCreate) -> Customer:
    with Session(engine) as session:
        customer = Customer.model_validate(customer)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer


def get_customer(id: uuid.UUID) -> Customer:
    with Session(engine) as session:
        statement = select(Customer).where(Customer.id == id)
        result = session.exec(statement)
        customer = result.one()
        return customer
