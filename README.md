# Telecom Churn ELT Pipeline

## Overview
This project creates an automated ELT (Extract, Load, Transform) pipeline to analyze Telecom Customer Churn.
It ingests data from Kaggle, stores raw data in a staging area, anonymizes Personal Identifiable Information (PII), and creates a clean dataset ready for reporting.

## Architecture
The solution is fully containerized using Docker.

* **Extraction:** Python script using Kaggle API.
* **Orchestration:** Apache Airflow (Scheduled to run hourly).
* **Database:** PostgreSQL (Split into `staging` and `analytics` schemas).
* **Transformation:** Pandas & SQLAlchemy (Clean & Anonymize).
* **Reporting:** Metabase (Connected to the `analytics` schema).

## Prerequisites
* Docker & Docker Compose installed.
* A Kaggle Account (for API credentials).

## Setup & Usage

### 1. Configure Credentials
For security reasons, API keys are not stored in the repository.
1. Create a `.env` file in the root directory.
2. Add your Kaggle credentials (from your `kaggle.json`):

```bash
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_secret_key


---

### 3. Vérification de la structure finale

Avant de pousser sur GitHub, vérifie que ton dossier ressemble **exactement** à ça. Si un fichier manque, dis-le-moi.

```text
telecom-churn-pipeline/
│
├── dags/
│   └── churn_pipeline.py    # (Le code Python que je t'ai donné avant)
│
├── data/                    # (Dossier vide, le script va le remplir)
│
├── .env                     # (Tes clés Kaggle - NE PAS COMMITTER SUR GITHUB)
├── .gitignore               # (Voir ci-dessous)
├── docker-compose.yaml      # (L'infra complète)
├── Dockerfile               # (La construction de l'image Airflow custom)
├── README.md                # (La doc ci-dessus)
└── requirements.txt         # (La liste des packages)