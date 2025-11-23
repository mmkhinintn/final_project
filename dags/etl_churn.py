from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime
import os
import pandas as pd
import logging
from transformers import impute_missing, anonymize_pii
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def download_data():
    """
    Downloads the customer churn dataset from Kaggle using environment variables.
    """
    try:
        dataset = os.getenv('KAGGLE_DATASET')
        path = os.getenv('DATA_PATH')
        if not dataset or not path:
            logger.error("KAGGLE_DATASET and DATA_PATH must be set in environment.")
            raise ValueError("KAGGLE_DATASET and DATA_PATH must be set.")
        rc = os.system(f"kaggle datasets download -d {dataset} -p {path} --unzip")
        if rc != 0:
            logger.error("Kaggle download failed.")
            raise RuntimeError("Kaggle download failed.")
        logger.info("Kaggle data downloaded successfully.")
    except Exception as e:
        logger.error(f"Download step failed: {e}")
        raise

def transform():
    """
    Loads the raw CSV file, imputes missing values, anonymizes PII, and writes a processed CSV.
    """
    try:
        data_path = os.getenv('DATA_PATH')
        input_file = os.path.join(data_path, "customer_churn_data.csv")
        output_file = os.path.join(data_path, "processed_churn.csv")
        if not os.path.exists(input_file):
            logger.error(f"Raw data file not found: {input_file}")
            raise FileNotFoundError(f"Raw data file not found: {input_file}")
        df = pd.read_csv(input_file)
        df = impute_missing(df)
        df = anonymize_pii(df)
        df.to_csv(output_file, index=False)
        logger.info("Data transformed and PII anonymized successfully.")
    except Exception as e:
        logger.error(f"Transform step failed: {e}")
        raise

def load_to_postgres():
    """
    Loads the processed CSV into the 'customer_churn' table in Postgres.
    """
    try:
        conn_str = os.getenv("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN")
        data_path = os.getenv('DATA_PATH')
        csv_file = os.path.join(data_path, "processed_churn.csv")
        if not conn_str:
            logger.error("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN not set in environment.")
            raise ValueError("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN not set.")
        if not os.path.exists(csv_file):
            logger.error(f"Processed CSV not found: {csv_file}")
            raise FileNotFoundError(f"Processed CSV not found: {csv_file}")
        engine = create_engine(conn_str)
        df = pd.read_csv(csv_file)
        df.to_sql("customer_churn", engine, if_exists="replace", index=False, method='multi')
        logger.info("Data loaded into PostgreSQL table 'customer_churn' successfully.")
    except Exception as e:
        logger.error(f"Load step failed: {e}")
        raise

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": 300,  # 5 minutes (seconds)
}

with DAG(
    dag_id="etl_churn",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    description="Automated ELT pipeline for telecom customer churn data—download, transform, anonymize PII, and load to Postgres."
) as dag:

    t_download = PythonOperator(
        task_id="download_data",
        python_callable=download_data,
        do_xcom_push=False,
    )

    t_transform = PythonOperator(
        task_id="transform",
        python_callable=transform,
        do_xcom_push=False,
    )

    t_create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_default",
        sql="sql/create_customer_table.sql"
    )

    t_load = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres,
        do_xcom_push=False,
    )

    t_download >> t_transform >> t_create_table >> t_load
