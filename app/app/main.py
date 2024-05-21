from fastapi import FastAPI
from typing import Union
import uuid

from models import Customer, CustomerCreate
import repository

app = FastAPI()


@app.post("/customers/")
def create_customer(customer: CustomerCreate) -> Customer:
    customer = repository.create_customer(customer)
    return customer


@app.get("/customers/{customer_id}")
def get_customer(customer_id: uuid.UUID) -> Customer:
    customer = repository.get_customer(customer_id)
    return customer
