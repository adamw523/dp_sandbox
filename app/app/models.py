from datetime import date
from sqlmodel import Field, Relationship, SQLModel
import uuid


class CustomerBase(SQLModel):
    name: str
    email: str


class Customer(CustomerBase, table=True):
    __tablename__ = "customers"
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, nullable=False
    )


class CustomerCreate(CustomerBase):
    pass


class InvoiceBase(SQLModel):
    customer_id: uuid.UUID
    invoice_date: date
    total_amount_cents: int
    status: str


class Invoice(InvoiceBase, table=True):
    __tablename__ = "invoices"
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, nullable=False
    )

    invoice_line_items: list["InvoiceLineItem"] = Relationship(back_populates="invoice")


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceLineItemBase(SQLModel):
    product_id: uuid.UUID
    quantity: int
    unit_price_cents: int


class InvoiceLineItem(InvoiceLineItemBase, table=True):
    __tablename__ = "invoice_line_items"
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, nullable=False
    )
    invoice_id: uuid.UUID | None = Field(default=None, foreign_key="invoices.id")
    invoice: Invoice | None = Relationship(back_populates="invoice_line_items")


class InvoiceLineItemCreate(InvoiceLineItemBase):
    pass
