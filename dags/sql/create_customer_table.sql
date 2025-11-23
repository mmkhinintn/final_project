CREATE TABLE IF NOT EXISTS customer_churn (
    id SERIAL PRIMARY KEY,
    -- Example of columns, adjust according to actual data
    tenure INTEGER,
    churn BOOLEAN,
    monthly_charges FLOAT,
    total_charges FLOAT,
    gender TEXT,
    senior_citizen INTEGER,
    partner BOOLEAN,
    dependents BOOLEAN
    
);
