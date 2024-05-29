import click
import faker
import requests

fake_genertor = faker.Faker()

MAX_ITEMS_PER_INVOICE = 10


@click.command()
@click.option(
    "--object_type", prompt="Type of object to fake", help="customer, invoice"
)
@click.option(
    "--count", prompt="Number of objects to fake", help="Number of objects", type=int
)
def fake(object_type: str, count: int):
    click.echo(f"creating {count} {object_type} objects")

    if object_type == "customer":
        for i in range(count):
            create_customer()
    elif object_type == "invoice":
        for i in range(count):
            create_invoice()


def create_customer():
    name = fake_genertor.name()
    email = fake_genertor.email()

    print(f"Creating customer {name} with email {email}")
    r = requests.post(
        "http://app:8000/customers/",
        json={"name": name, "email": email},
    )
    print(f"return code: {r.status_code}")


def create_invoice():
    customer_id = get_random_customer_id()
    total_amount_cents = fake_genertor.random_int(100, 100000)
    status = fake_genertor.random_element(elements=("pending", "sent", "paid"))
    invoice_date = fake_genertor.date_time_this_decade().strftime("%Y-%m-%d")

    print(
        f"Creating invoice {customer_id=}, {total_amount_cents=}, {status=}, {invoice_date=}"
    )
    r = requests.post(
        "http://app:8000/invoices/",
        json={
            "customer_id": customer_id,
            "total_amount_cents": total_amount_cents,
            "status": status,
            "invoice_date": invoice_date,
        },
    )
    invoice_id = r.json()["id"]
    print(f"return code: {r.status_code}, {invoice_id=}")

    for _ in range(fake_genertor.random_int(1, MAX_ITEMS_PER_INVOICE)):
        product_id = fake_genertor.uuid4()
        quantity = fake_genertor.random_int(1, 10)
        unit_price_cents = fake_genertor.random_int(100, 10000)

        print(f"Adding line item {product_id=}, {quantity=}, {unit_price_cents=}")
        r = requests.post(
            f"http://app:8000/invoices/{invoice_id}/line_items/",
            json={
                "product_id": product_id,
                "quantity": quantity,
                "unit_price_cents": unit_price_cents,
            },
        )
        print(f"return code: {r.status_code}")


def get_random_customer_id():
    r = requests.get("http://app:8000/customers/random")
    return r.json()["id"]


if __name__ == "__main__":
    fake()
