# dp_sandbox
A sandbox for Data Engineering related projects

## Environment variables

Create a file `~/env/dp_sandbox.env` with the contents:

```
POSTGRES_USER={value}
POSTGRES_PASSWORD={value}
POSTGRES_DB={value}
SNOWSQL_ACCOUNT={value}
SNOWSQL_DATABASE={value}
SNOWSQL_SCHEMA={value}
SNOWSQL_WAREHOUSE={value}
SNOWSQL_USER={value}
SNOWSQL_PWD=32#&{value}
SNOWSQL_ROLE={value}
```

## Running Stuff

### Set environment variables

```bash
source ./scripts/load_env.sh
```

### Postgres Server

```bash
make pg_start
make pg_stop
```

### Migrate Database

```bash
make app_migrations_apply
make app_migrations_rollback
```

### API Server

```bash
make app_start
make app_stop

# Tail logs
docker compose logs -f app
```

### Fake Some Data

```bash
docker compose run client python make_fakes.py --object_type customer --count 10
docker compose run client python make_fakes.py --object_type invoice --count 50
```


### Sync to Snowflake

```bash
make snow_sync
```
