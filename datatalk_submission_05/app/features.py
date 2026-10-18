"""Feature definitions and preprocessing shared by training and prediction.

Both train.py and predict.py go through `to_records`, so a lead is always
prepared the same way whether it comes from the CSV or from a live request.
"""
import pandas as pd

TARGET = "converted"

CATEGORICAL = ["lead_source", "industry", "employment_status", "location"]
NUMERICAL = ["number_of_courses_viewed", "annual_income", "interaction_count", "lead_score"]
FEATURES = CATEGORICAL + NUMERICAL

MISSING_CATEGORY = "NA"
MISSING_NUMBER = 0


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only the model's input columns and fill missing values.

    Columns absent from `df` are added as missing; extra columns are dropped.
    Non-numeric values in numerical columns are treated as missing.
    """
    X = df.reindex(columns=FEATURES)
    for col in CATEGORICAL:
        X[col] = X[col].astype("object").fillna(MISSING_CATEGORY)
    for col in NUMERICAL:
        X[col] = pd.to_numeric(X[col], errors="coerce").fillna(MISSING_NUMBER)
    return X


def to_records(df: pd.DataFrame) -> list[dict]:
    """Prepare features and convert to the list-of-dicts format DictVectorizer expects."""
    return prepare_features(df).to_dict(orient="records")
