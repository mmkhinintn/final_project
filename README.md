# Telecom Churn ELT Pipeline

## Overview

This project creates an automated ELT (Extract, Load, Transform) pipeline to analyze Telecom Customer Churn.  
It ingests data from Kaggle, stores raw data in a staging area, anonymizes Personal Identifiable Information (PII), and creates a clean dataset ready for reporting.

---

## Architecture

The solution is fully containerized using Docker.

- **Extraction :** Python script using Kaggle API.
# Telecom Churn ELT Pipeline

## Overview

This project implements an automated ELT (Extract, Load, Transform) pipeline for Telecom Customer Churn analysis. The pipeline:

- Downloads raw data (Kaggle)
- Loads raw data into a staging area
- Anonymizes PII and transforms the data
- Stores cleaned data in an `analytics` schema for reporting

## Architecture

The solution is containerized with Docker and uses:

- **Extraction:** Python script using the Kaggle API
- **Orchestration:** Apache Airflow (DAG scheduled as configured)
- **Database:** PostgreSQL ( `staging` and `analytics` schemas )
- **Transformation:** Pandas & SQLAlchemy
- **Reporting:** Metabase connected to the `analytics` schema

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
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_secret_key
```

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

6) Verify results

- Raw data should be available in `staging.customer_churn`
- Processed data should be available in `analytics.customer_churn`

7) Metabase (reporting)

- Open Metabase at `http://localhost:3000` and configure your admin account on first run
- Connect Metabase to the `analytics` schema to view dashboards

## Example Dashboards

- Churn by Contract Type (`images/churn_by_contracttype.PNG`)
- Average Monthly Charges for Churners by Contract Type (`images/avg_monthlycharges_by_contracttype.PNG`)
- Churn by Customer Tenure (`images/churn_by_tenure.PNG`)

## Project Structure

```
final_project/ (project root)
├── dags/
│   ├── etl_churn.py       # Airflow DAG
│   └── transformers.py    # Transformation helpers
├── data/                  # Raw and processed CSVs
├── sql/                   # SQL scripts
├── images/                # Dashboard screenshots
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
```

## Notes

- The stack runs in Docker for portability and easy testing.
- Airflow manages and schedules pipeline tasks with restartability and monitoring.
- Data is anonymized before being stored in the `analytics` schema.

If you add images for the README, place them in the `images/` folder or update the paths accordingly.

---

Ready to use for Telecom churn analysis!
---



## Project Structure


