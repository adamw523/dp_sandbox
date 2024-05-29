FROM python:3.11-slim

RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev postgresql postgresql-contrib

WORKDIR /pgwarehosue

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
