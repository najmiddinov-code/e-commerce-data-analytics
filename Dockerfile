FROM apache/airflow:3.0.0-python3.12

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir \
    psycopg2-binary \
    faker \
    dbt-postgres==1.9.0