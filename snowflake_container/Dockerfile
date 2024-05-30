FROM python:3.11-slim

WORKDIR /snowflake_container

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY app /snowflake_container

# COPY snowflake_container /snowflake_container

ENTRYPOINT [ "flask", "--app", "snowy", "run", "--host", "0.0.0.0" ]