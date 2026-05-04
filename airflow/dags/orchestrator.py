from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


DBT_PROJECT_DIR = "/opt/airflow/ecommerce_dbt"
DBT_PROFILES_DIR = "/opt/airflow/.dbt"


with DAG(
    dag_id="ecommerce_dbt_orchestrator",
    start_date=datetime(2024, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["ecommerce", "dbt", "postgres"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_new_data",
        bash_command="""
        set -e
        python /opt/airflow/data_generation/data_generator.py
        """,
    )

    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=f"""
        set -e
        cd {DBT_PROJECT_DIR}
        dbt debug --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    run_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command=f"""
        set -e
        cd {DBT_PROJECT_DIR}
        dbt run --select staging.* --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    run_mart = BashOperator(
        task_id="dbt_run_mart",
        bash_command=f"""
        set -e
        cd {DBT_PROJECT_DIR}
        dbt run --select mart.* --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    generate_data >> dbt_debug >> run_staging >> run_mart