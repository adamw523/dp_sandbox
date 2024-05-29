from sqlmodel import Field, Session, SQLModel, create_engine, func, select
import uuid

from config import Config
from models import (
    Customer,
    CustomerCreate,
    Invoice,
    InvoiceCreate,
    InvoiceLineItem,
    InvoiceLineItemCreate,
)


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


def get_random_customer() -> Customer:
    with Session(engine) as session:
        statement = select(Customer).order_by(func.random()).limit(1)
        result = session.exec(statement)
        customer = result.one()
        return customer


def get_invoice(id: uuid.UUID) -> Invoice:
    with Session(engine) as session:
        statement = select(Invoice).where(Invoice.id == id)
        result = session.exec(statement)
        invoice = result.one()
        return invoice


def get_random_invoice() -> Invoice:
    with Session(engine) as session:
        statement = select(Invoice).order_by(func.random()).limit(1)
        result = session.exec(statement)
        invoice = result.one()
        return invoice


def create_invoice(invoice: InvoiceCreate) -> Invoice:
    with Session(engine) as session:
        invoice = Invoice.model_validate(invoice)
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        return invoice


def create_invoice_line_item(
    invoice: Invoice, line_item: InvoiceLineItemCreate
) -> InvoiceLineItem:
    with Session(engine) as session:
        line_item: InvoiceLineItem = InvoiceLineItem.model_validate(line_item)
        line_item.invoice_id = invoice.id
        session.add(line_item)
        session.commit()
        session.refresh(line_item)
        return line_item


def get_invoice_line_items(invoice_id: str) -> list[InvoiceLineItem]:
    with Session(engine) as session:
        statement = select(InvoiceLineItem).where(
            InvoiceLineItem.invoice_id == invoice_id
        )
        result = session.exec(statement)
        line_items = result.all()
        return line_items
