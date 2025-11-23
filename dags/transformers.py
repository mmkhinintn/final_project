import pandas as pd
import hashlib
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def impute_missing(df):
    """
    Fill missing values:
      - Numeric columns: median
      - Categorical/object columns: most frequent value (mode)
    """
    logger.info("Imputing missing values in dataframe")
    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype == "O":
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode[0])
                    logger.debug(f"Filled missing values in column '{col}' with mode '{mode[0]}'")
            else:
                median = df[col].median()
                df[col] = df[col].fillna(median)
                logger.debug(f"Filled missing values in column '{col}' with median '{median}'")
    return df

def hash_column(series):
    """
    Hash each value in a pandas Series using SHA256, truncate to first 12 characters.
    """
    return series.apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:12])

def anonymize_pii(df):
    """
    Anonymize Personal Identifiable Information (PII):
      - Hash any column containing 'customerid', 'name', 'email', 'phone', 'address'
      - No column is deleted; all detected PII are anonymized.
    """
    logger.info("Anonymizing PII columns")
    pii_keys = ['customerid', 'name', 'email', 'phone', 'address']
    pii_cols = [col for col in df.columns if any(key in col.lower() for key in pii_keys)]
    for col in pii_cols:
        df[col] = hash_column(df[col])
        logger.debug(f"Hashed column '{col}' for PII protection.")
    return df
