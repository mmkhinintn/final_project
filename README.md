# Telecom Churn ELT Pipeline

## Overview

This project implements an automated ELT (Extract, Load, Transform) pipeline for Telecom Customer Churn analysis. The pipeline:

- Downloads data from Kaggle
- Applies imputation and PII anonymization (hashing of CustomerID and any PII columns)
- Loads clean data directly into the `customer_churn` table for reporting and analytics


## Architecture

The solution is containerized with Docker and uses:

- **Extraction:** Python script using the Kaggle API
- **Orchestration:** Apache Airflow (DAG scheduled as configured)
- **Database:** PostgreSQL (`staging` and `analytics` schemas)
- **Transformation:** Pandas & SQLAlchemy
- **Reporting:** Metabase connected to the `analytics` schema

## Architecture Diagram

![Pipeline Architecture](images/architecture.PNG)


## Prerequisites

- Docker & Docker Compose
- A Kaggle account (API credentials)

## Setup & Usage

1) Clone the project

```
git clone https://github.com/yourusername/telecom-churn-pipeline.git
cd telecom-churn-pipeline
```

2) Configure credentials

Create a `.env` file in the project root and add your Kaggle credentials (do not commit this file):

```
cp .env.example .env

```

Then edit `.env` and add your personal Kaggle credentials and other secrets.

*Do not commit your real `.env` file or secret keys!*



3) Build & launch the stack

```
docker-compose up --build
```

4) Initialize Airflow (one-time)

In a new terminal:

```
docker-compose exec airflow-webserver airflow db init
docker-compose exec airflow-webserver airflow users create \
  --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin
```

5) Trigger the pipeline

- Open the Airflow UI at `http://localhost:8080`
- Login with `admin` / `admin`
- Trigger the `etl_churn` DAG or wait for the scheduler
- We obtain a result like this:

![etl_churn](images/etl_churn.PNG)




6) Metabase (reporting)

- Open Metabase at `http://localhost:3000` and configure your admin account on first run
- Connect Metabase to the churn_db database and select the customer_churn table to view dashboards
- You can visualize the data as shown below:

![churn_customers](images/churn_customers.PNG)

## 📊 Example Dashboards

### 1. Churn by Contract Type

![Churn by Contract Type](images/churn_by_contracttype.PNG)

---

### 2. Average Monthly Charges for Churners by Contract Type

![Average Monthly Charges for Churners by Contract Type](images/avg_monthlycharges_by_contracttype.PNG)

---

### 3. Churn by Customer Tenure – Number of Churners per Tenure Group

![Churn by Tenure](images/churn_by_tenure.PNG)

---
## Project Structure

```
final_project/ (project root)
├── dags/
│   ├── etl_churn.py       # Airflow DAG
│   └── transformers.py    # Transformation helpers     # Airflow DAG
│   └── tests/test_transformers.py     # test transformers.py
├── data/                  # Raw and processed CSVs
├── sql/                   # SQL scripts
├── images/                # Dashboard screenshots
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
```

## Data Privacy & PII Handling

All personally identifiable information (PII) columns (e.g. CustomerID, name, email, phone, address, etc.) are anonymized using SHA256 hashing before any reporting or analytics. This ensures GDPR compliance and protects customer privacy. No PII is ever exposed in the analytics schema.



## Testing & Code Quality

- Includes unit tests for all transformation logic (`transformers.py`)
- Logging and error handling implemented in all ETL steps for traceability
- Easily extendable to handle new PII columns or evolving schema


## Notes

- All services are up in Docker for easy, portable testing.
- Airflow manages and schedules all steps, with full restartability and monitoring.
- Data is anonymized and preprocessed for business reporting.
- Metabase dashboards are ready to use and can be edited/forked as needed.

---

**Ready to use for any Telecom churn analysis!**



