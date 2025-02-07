import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import logging
from scipy.stats import skew

logger = logging.getLogger(__name__)

def handle_missing_values(df: pd.DataFrame, column_dtypes: dict) -> pd.DataFrame:
    """
    Detect and impute missing values using type-appropriate methods with optimized handling.

    Args:
        df: Input DataFrame
        column_dtypes: Dictionary of column data types

    Returns:
        DataFrame with imputed values
    """
    logger.info("Handling missing values with optimized approach...")
    df_imputed = df.copy()

    numeric_cols = [col for col in df.columns if column_dtypes[col] == "numeric"]
    missing_percentages = df.isna().sum() / len(df) * 100

    high_missing_numeric_cols = [col for col in numeric_cols if missing_percentages[col] >= 5]
    if high_missing_numeric_cols:
        if not df[high_missing_numeric_cols].isnull().all().all():
            imputer = KNNImputer(n_neighbors=5)
            null_mask = df[high_missing_numeric_cols].isnull()
            imputed_values = imputer.fit_transform(df[high_missing_numeric_cols])
            df_imputed.loc[:, high_missing_numeric_cols] = df[high_missing_numeric_cols].where(~null_mask, imputed_values)
        else:
            logger.warning("All values in high-missing numeric columns are null. Skipping KNN imputation.")

    for column in df.columns:
        if df[column].isna().any():
            try:
                if column_dtypes[column] == "datetime":
                    df_imputed[column] = df_imputed[column].fillna(method="ffill").fillna(method="bfill")
                elif column_dtypes[column] == "categorical":
                    mode_value = df[column].mode()
                    if mode_value.empty:
                        logger.warning(f"Column '{column}' has no mode to impute. Leaving as NaN.")
                    else:
                        df_imputed[column] = df_imputed[column].fillna(mode_value.iloc[0])
                elif column_dtypes[column] == "numeric":
                    if missing_percentages[column] < 5:
                        # Check skewness
                        skewness = skew(df[column].dropna())
                        if abs(skewness) > 0.5:
                            # Use median for skewed data
                            logger.info(f"Column '{column}' is skewed (skewness: {skewness:.2f}). Using median for imputation.")
                            df_imputed[column] = df_imputed[column].fillna(df[column].median())
                        else:
                            # Use mean for symmetric data
                            logger.info(f"Column '{column}' is relatively symmetric (skewness: {skewness:.2f}). Using mean for imputation.")
                            df_imputed[column] = df_imputed[column].fillna(df[column].mean())
                    # KNN imputation for high-missing columns is already handled
            except Exception as e:
                logger.error(f"Error handling column '{column}': {e}")

    return df_imputed
