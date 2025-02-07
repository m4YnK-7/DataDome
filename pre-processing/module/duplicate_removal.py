import pandas as pd
import hashlib
import logging

logger = logging.getLogger(__name__)

def remove_duplicates(df: pd.DataFrame) ->pd.DataFrame:
    """
    Remove duplicate rows using row hashing.

    Args:
        df: Input DataFrame

    Returns:
        Tuple containing:
        - DataFrame with duplicates removed
        - List of indices of duplicate rows
    """
    logger.info("Removing duplicate rows using row hashing...")

    def hash_row(row):
        row_str = ''.join(str(x) for x in row)
        return hashlib.md5(row_str.encode()).hexdigest()
    
    df['_row_hash'] = df.apply(hash_row, axis=1)
    
    duplicate_mask = df.duplicated(subset=['_row_hash'], keep=False)
    # duplicate_indices = df[duplicate_mask].index.tolist()
    
    df_unique = df.drop_duplicates(subset=['_row_hash']).drop(columns=['_row_hash'])
    
    logger.info(f"Duplicate removal completed. Rows reduced from {len(df)} to {len(df_unique)}")
    # logger.info(f"Number of duplicate rows found: {len(duplicate_indices)}")

    return df_unique
