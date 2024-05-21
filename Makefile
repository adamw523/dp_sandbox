SHELL := /bin/bash

set_env_vars:
	@echo "Set environment variables by running: source ./scripts/load_env.sh"

dev_configure_local_venv:
	python3 -m venv .venv
	.venv/bin/pip install -r app/requirements.txt

app_migrations_apply:
	@docker compose run app yoyo --batch apply

app_migrations_rollback:
	@docker compose run app yoyo --batch rollback

app_migrations_list:
	docker compose run app yoyo list

.PHONY: app_migrations_apply app_migrations_list app_migrations_rollback app_configure_venv set_env_vars