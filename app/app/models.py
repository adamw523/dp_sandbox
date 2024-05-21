from typing import Optional
from sqlmodel import SQLModel, Field
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
