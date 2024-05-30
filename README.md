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
SNOWSQL_PWD={value}
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


### Snowflake Container Service App

#### Compute Pool Commands

```bash
# Compute pool

snowsql -q "CREATE SECURITY INTEGRATION IF NOT EXISTS snowservices_ingress_oauth TYPE=oauth OAUTH_CLIENT=snowservices_ingress ENABLED=true;"

snowsql -q "CREATE COMPUTE POOL dp_sandbox_pool
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_XS;"

snowsql -q "DESCRIBE COMPUTE POOL DP_SANDBOX_POOL"
snowsql -q "SHOW COMPUTE POOLS;"
```

#### Repositories Commands

```bash
snowsql -q "USE ROLE dp_sandbox_role;
USE DATABASE dp_container_service;
USE WAREHOUSE dp_sandbox_wh;
show image repositories"

```



#### Repository / Container Service Commands

```bash
snowsql -q "CREATE DATABASE dp_container_service;"
snowsql -q "CREATE ROLE dp_sandbox_role;"
snowsql -q "GRANT OWNERSHIP ON DATABASE dp_container_service TO ROLE dp_sandbox_role COPY CURRENT GRANTS;"
snowsql -q "GRANT USAGE ON WAREHOUSE dp_sandbox_wh TO ROLE dp_sandbox_role;"
snowsql -q "GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO ROLE dp_sandbox_role;"
snowsql -q "GRANT USAGE, MONITOR ON COMPUTE POOL dp_sandbox_pool TO ROLE dp_sandbox_role;"
snowsql -q "GRANT ROLE dp_sandbox_role TO USER ${SNOWSQL_USER}"


snowsql -q "USE ROLE dp_sandbox_role;
USE DATABASE dp_container_service;
USE WAREHOUSE dp_sandbox_wh;

CREATE SCHEMA IF NOT EXISTS data_schema;
CREATE IMAGE REPOSITORY IF NOT EXISTS dp_sandbox_repository;
CREATE STAGE IF NOT EXISTS dp_sandbox_repository_stage
  DIRECTORY = ( ENABLE = true );"



export SNOW_REGISTRY_URL=$(snowsql -q "USE ROLE dp_sandbox_role;
USE DATABASE dp_container_service;
USE WAREHOUSE dp_sandbox_wh;
show image repositories" |grep DP_SANDBOX_REPOSITORY |cut -d '|' -f6 |awk '{$1=$1;print}')
export SNOW_REGISTRY_HOST=$(echo $SNOW_REGISTRY_URL |cut -d '/' -f1)
export SNOW_IMAGE_PATH="/${SNOW_IMAGE_NAME#*/}"
export SNOW_IMAGE_NAME=${SNOW_REGISTRY_URL}/dp_sandbox

docker build --rm --platform linux/amd64 -t ${SNOW_IMAGE_NAME}:latest snowflake_container

echo $SNOWSQL_PWD | docker login $SNOW_REGISTRY_HOST -u $SNOWSQL_USER --password-stdin

docker push ${SNOW_IMAGE_NAME}:latest


snowsql -q "USE ROLE dp_sandbox_role;
USE database dp_container_service;
USE SCHEMA data_schema;
USE WAREHOUSE dp_sandbox_wh;
CREATE SERVICE dp_sandbox_service
  IN COMPUTE POOL dp_sandbox_pool
  FROM SPECIFICATION \$\$
$(envsubst < snowflake_container/spec.yaml)
      \$\$
   MIN_INSTANCES=1
   MAX_INSTANCES=1;"

snowsql -q "USE ROLE dp_sandbox_role;
USE database dp_container_service;
USE SCHEMA data_schema;
show endpoints in service dp_sandbox_service;"

snowsql -q "USE ROLE dp_sandbox_role;
USE database dp_container_service;
USE SCHEMA data_schema;
SHOW SERVICES;
SELECT SYSTEM\$GET_SERVICE_STATUS('dp_sandbox_service');
DESCRIBE SERVICE dp_sandbox_service;"

snowsql -q "USE ROLE dp_sandbox_role;
USE database dp_container_service;
USE SCHEMA data_schema;
SHOW SERVICES;
SELECT SYSTEM\$GET_SERVICE_LOGS('dp_sandbox_service', 0, 'dp-sandbox-service-container');"

snowsql -q "USE ROLE dp_sandbox_role;
USE database dp_container_service;
USE SCHEMA data_schema;
drop service dp_sandbox_service;"


```

