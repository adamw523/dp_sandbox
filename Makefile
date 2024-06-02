SHELL := /bin/bash

set_env_vars:
	@echo "Set environment variables by running: source ./scripts/load_env.sh"

dev_configure_local_venv:
	python3.11 -m venv .venv
	.venv/bin/pip install -r app/requirements.txt -r client/requirements.txt -r snow_containers_streamlit/requirements.txt

app_start:
	docker compose start app

app_stop:
	docker compose stop app

app_migrations_apply:
	docker compose run app yoyo --batch apply

app_migrations_rollback:
	docker compose run app yoyo --batch rollback

app_migrations_list:
	docker compose run app yoyo list

pg_run_psql:
	docker compose exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} 

pg_start:
	docker compose start postgres

pg_stop:
	docker compose stop postgres

snow_sync:
	docker compose run pgwarehouse pgwarehouse sync all


.PHONY: app_migrations_apply app_migrations_list app_migrations_rollback app_configure_venv set_env_vars pg_run_psql