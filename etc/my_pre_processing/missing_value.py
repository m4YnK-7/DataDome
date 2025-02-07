import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor
import logging

logger = logging.getLogger(__name__)

def handle_missing_values(df: pd.DataFrame, column_dtypes: dict) -> pd.DataFrame:
    """
    Detect and impute missing values using type-appropriate methods.

    Args:
        df: Input DataFrame
        column_dtypes: Dictionary of column data types

    Returns:
        DataFrame with imputed values
    """
    logger.info("Handling missing values...")
    df_imputed = df.copy()

    for column in df.columns:
        if df[column].isna().any():
            if column_dtypes[column] == "datetime":
                df_imputed[column] = df_imputed[column].fillna(method="ffill").fillna(method="bfill")
            elif column_dtypes[column] == "categorical":
                df_imputed[column] = df_imputed[column].fillna(df[column].mode()[0])
            else:  
                numeric_cols = [col for col in df.columns if column_dtypes[col] == "numeric"]
                if len(numeric_cols) > 1:
                    imputer = IterativeImputer(
                        estimator=RandomForestRegressor(n_estimators=100),
                        max_iter=10,
                        random_state=42
                    )
                    df_imputed[numeric_cols] = imputer.fit_transform(df[numeric_cols])
                else:
                    df_imputed[column] = df_imputed[column].fillna(df[column].mean())

    return df_imputed
