import os
import streamlit as st

def snow_config():
    return {
      "account": os.getenv("SNOWSQL_ACCOUNT"),
      "database": os.getenv("SNOWSQL_DATABASE"),
      "schema": os.getenv("SNOWSQL_SCHEMA"),
      "warehouse": os.getenv("SNOWSQL_WAREHOUSE"),
      "user": os.getenv("SNOWSQL_USER"),
      "role": os.getenv("SNOW_SANDBOX_ROLE"), # os.getenv("SNOWSQL_ROLE"),
      "password": os.getenv("SNOWSQL_PWD"),
      "sandbox_role": os.getenv("SNOW_SANDBOX_ROLE"),
    }

config = snow_config()
conn = st.connection("snowflake", type="snowflake", **snow_config())


session = conn.session()
repositoreis_sql = f"show image repositories;"
reposotires_data = session.sql(repositoreis_sql).collect()


st.header("Snowflake Container Services")

st.subheader("Image Repositories")
st.table(reposotires_data)
