import os
from snowflake.snowpark.context import get_active_session
import streamlit as st


def snow_config():
    return {
        "account": os.getenv("SNOWSQL_ACCOUNT"),
        "database": os.getenv("SNOWSQL_DATABASE"),
        "schema": os.getenv("SNOWSQL_SCHEMA"),
        "warehouse": os.getenv("SNOWSQL_WAREHOUSE"),
        "user": os.getenv("SNOWSQL_USER"),
        "role": os.getenv("SNOW_SANDBOX_ROLE"),  # os.getenv("SNOWSQL_ROLE"),
        "password": os.getenv("SNOWSQL_PWD"),
        "sandbox_role": os.getenv("SNOW_SANDBOX_ROLE"),
    }


def get_session():
    # active_session = get_active_session()
    # if active_session:
    #     return active_session

    config = snow_config()
    return st.connection("snowflake", type="snowflake", **snow_config()).session()


def get_repositories():
    session = get_session()
    repositoreis_sql = f"show image repositories;"
    reposotires_data = session.sql(repositoreis_sql).collect()
    return reposotires_data


def get_images_in_repository(database_name, schema_name, repository_name):
    # TODO fix "401 Unauthorized" error
    session = get_session()
    session.sql(f"use role {config['sandbox_role']};").collect()
    session.sql(f"use database {database_name};").collect()
    session.sql(f"use schema {schema_name};").collect()
    st.write(f"show images in image repository {repository_name};")
    images_data = session.sql(
        f"show images in image repository {repository_name};"
    ).collect()
    return images_data


reposotires_data = get_repositories()

st.header("Snowflake Container Services")

st.subheader("Image Repositories")

repos_df = st.dataframe(
    reposotires_data,
    selection_mode="single-row",
    column_order=["name", "database_name", "schema_name"],
    on_select="rerun",
    column_config={
        "name": "Name",
        "database_name": "Database",
        "schema_name": "Schema",
    },
)

if repos_df.selection["rows"]:
    selected_repo = reposotires_data[repos_df.selection["rows"][0]]
    host = selected_repo["repository_url"].split("/")[0]

    # images = get_images_in_repository(
    #     selected_repo["database_name"],
    #     selected_repo["schema_name"],
    #     selected_repo["name"],
    # )
    # st.write(images)

    st.subheader(f"{selected_repo['name']}")

    st.text(f"Created On: {selected_repo['created_on']}")
    st.text(f"Database Name: {selected_repo['database_name']}")
    st.text(f"Schema: {selected_repo['schema_name']}")
    st.text(f"Docker Repsotiory Address: {selected_repo['repository_url']}")
    st.text(f"Owner: {selected_repo['owner']}")
    st.text(f"Owner Role Type: {selected_repo['owner_role_type']}")
    st.text(f"Comment: {selected_repo['comment']}")
    st.text(f"Docker login command: {selected_repo['comment']}")
    st.code(f"docker login {host} -u $SNOWSQL_USER")
