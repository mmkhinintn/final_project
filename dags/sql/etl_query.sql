--a csv file is used to load data into the customer_churn table
COPY customer_churn (tenure, churn, monthly_charges, total_charges, gender, senior_citizen, partner, dependents)
FROM '/data/processed_churn.csv' DELIMITER ',' CSV HEADER;
