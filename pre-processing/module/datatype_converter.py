import pandas as pd
import logging

logger = logging.getLogger(__name__)

def infer_and_convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Infer and convert column data types, handling dates, numerics, and categories.

    Args:
        df: Input DataFrame

    Returns:
        DataFrame with properly converted data types
    """
    logger.info("Inferring and converting data types...")
    df_converted = df.copy()
    column_dtypes = {}

    for column in df.columns:
        # Try numeric conversion
        try:
            df_converted[column] = pd.to_numeric(df[column])
            column_dtypes[column] = "numeric"
            continue
        except (ValueError, TypeError):
            pass
    
        # Try datetime conversion first
        try:
            df_converted[column] = pd.to_datetime(df[column])
            column_dtypes[column] = "datetime"
            continue
        except (ValueError, TypeError):
            pass

        

        # Fall back to categorical
        df_converted[column] = df[column].astype("category")
        column_dtypes[column] = "categorical"

    return df_converted, column_dtypes
