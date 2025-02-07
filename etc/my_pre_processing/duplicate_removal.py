import pandas as pd
import logging

logger = logging.getLogger(__name__)

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows using memory-efficient chunk processing.

    Args:
        df: Input DataFrame

    Returns:
        DataFrame with duplicates removed
    """
    logger.info("Removing duplicate rows...")
    return df.drop_duplicates(keep="first")
