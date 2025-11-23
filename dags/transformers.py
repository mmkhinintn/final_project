import pandas as pd

def impute_missing(df):
    # Ex: remplacement des valeurs manquantes par la médiane pour chaque colonne
    for col in df.columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median() if df[col].dtype != 'O' else df[col].mode()[0])
    return df

def anonymize_pii(df):
    # Ex: suppression de colonnes sensibles
    cols_to_drop = [col for col in df.columns if 'name' in col or 'email' in col or 'phone' in col]
    df = df.drop(columns=cols_to_drop, errors='ignore')
    return df
