FROM apache/airflow:2.10.3-python3.10

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY dags/ /opt/airflow/dags/
