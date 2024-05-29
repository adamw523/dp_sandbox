from fastapi import FastAPI
import uuid

from models import (
    Customer,
    CustomerCreate,
    Invoice,
    InvoiceCreate,
    InvoiceLineItem,
    InvoiceLineItemCreate,
)
import repository

app = FastAPI()


@app.post("/customers/")
def create_customer(customer: CustomerCreate) -> Customer:
    customer = repository.create_customer(customer)
    return customer


@app.get("/customers/random")
def get_random_customer() -> Customer:

    created_customer = repository.get_random_customer()
    return created_customer


@app.get("/customers/{customer_id}")
def get_customer(customer_id: uuid.UUID) -> Customer:
    customer = repository.get_customer(customer_id)
    return customer


@app.get("/invoices/random")
def get_random_invoice() -> Invoice:
    invoice = repository.get_random_invoice()
    return invoice


@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: uuid.UUID) -> Invoice:
    invoice = repository.get_invoice(invoice_id)
    return invoice


@app.post("/invoices/")
def create_invoice(invoice: InvoiceCreate) -> Invoice:
    created_invoice = repository.create_invoice(invoice)
    return created_invoice


@app.post("/invoices/{invoice_id}/line_items/")
def create_line_item(
    line_item: InvoiceLineItemCreate, invoice_id: str
) -> InvoiceLineItem:
    invoice = repository.get_invoice(invoice_id)
    created_invoice_line_item = repository.create_invoice_line_item(invoice, line_item)
    return created_invoice_line_item


@app.get("/invoices/{invoice_id}/line_items")
def get_invoice_line_items(invoice_id: str) -> list[InvoiceLineItem]:
    line_items = repository.get_invoice_line_items(invoice_id)

    return line_items
