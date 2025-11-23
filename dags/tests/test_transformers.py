import pandas as pd
import sys
sys.path.append("..")
from transformers import impute_missing, anonymize_pii

def test_impute_missing_numeric():
    df = pd.DataFrame({"A": [1, None, 3]})
    result = impute_missing(df)
    assert result["A"].isnull().sum() == 0
    # Should fill with median (2.0)
    assert result["A"][1] == 2.0

def test_impute_missing_text():
    df = pd.DataFrame({"A": ["x", None, "y", "x"]})
    result = impute_missing(df)
    assert result["A"].isnull().sum() == 0
    # Should fill with mode ("x")
    assert result["A"][1] == "x"

def test_anonymize_pii_removes_columns_and_hashes_id():
    df = pd.DataFrame({
        "name": ["John"],
        "email": ["a@b.com"],
        "CustomerID": ["12345"],
        "Other": ["data"]
    })
    result = anonymize_pii(df)
    assert "name" not in result
    assert "email" not in result
    assert "CustomerID" in result
    # Verify that CustomerID is hashed (length 12)
    assert isinstance(result["CustomerID"][0], str)
    assert len(result["CustomerID"][0]) == 12
