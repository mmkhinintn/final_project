from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime
import os
import pandas as pd
from transformers import impute_missing, anonymize_pii
from sqlalchemy import create_engine

def download_data():
    os.system(f"kaggle datasets download -d {os.getenv('KAGGLE_DATASET')} -p {os.getenv('DATA_PATH')} --unzip")

def transform():
    df = pd.read_csv(f"{os.getenv('DATA_PATH')}/customer_churn_data.csv")
    df = impute_missing(df)
    df = anonymize_pii(df)
    df.to_csv(f"{os.getenv('DATA_PATH')}/processed_churn.csv", index=False)

def load_to_postgres():
    engine = create_engine(os.getenv("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN"))
    df = pd.read_csv(f"{os.getenv('DATA_PATH')}/processed_churn.csv")
    df.to_sql("customer_churn", engine, if_exists="replace", index=False, method='multi')


with DAG(
    "etl_churn",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    t_download = PythonOperator(
        task_id="download_data",
        python_callable=download_data
    )

    t_transform = PythonOperator(
        task_id="transform",
        python_callable=transform
    )

    t_create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_default",
        sql="sql/create_customer_table.sql"
    )

    t_load = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres
    )

    t_download >> t_transform >> t_create_table >> t_load
