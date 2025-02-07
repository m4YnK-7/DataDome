import pandas as pd
from scipy import stats
import logging

logger = logging.getLogger(__name__)

def calculate_correlations(df: pd.DataFrame) -> pd.Series:
    """
    Calculate correlations with the target variable.

    Args:
        df: Input DataFrame

    Returns:
        Series with correlation scores
    """
    logger.info("Calculating correlations...")
    target_col = df.columns[-1]
    correlation_scores = df.corrwith(df[target_col])
    return correlation_scores

def drop_weak_correlations(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Remove columns with weak correlations based on Z-score threshold.

    Args:
        df: Input DataFrame
        correlation_scores: Precomputed correlation scores
        threshold: Minimum Z-score to retain columns

    Returns:
        DataFrame with weak correlations removed
    """
    correlation_scores = calculate_correlations(df)
    correlation_zscores = stats.zscore(correlation_scores)
    columns_to_keep = correlation_scores[correlation_zscores > threshold].index.tolist()

    if df.columns[-1] not in columns_to_keep:
        columns_to_keep.append(df.columns[-1])

    return df[columns_to_keep]
