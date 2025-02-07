# # import pandas as pd
# # import numpy as np
# # from scipy import stats
# # import logging

# # logger = logging.getLogger(__name__)

# # def remove_outliers(df: pd.DataFrame, column_dtypes: dict, threshold: float) -> pd.DataFrame:
# #     """
# #     Identify and remove statistical outliers from numeric columns.

# #     Args:
# #         df: Input DataFrame
# #         column_dtypes: Dictionary of column data types
# #         threshold: Z-score threshold for outlier detection

# #     Returns:
# #         DataFrame with outliers removed
# #     """
# #     logger.info("Removing outliers...")
# #     numeric_cols = [col for col in df.columns if column_dtypes[col] == "numeric"]

# #     for col in numeric_cols:
# #         z_scores = np.abs(stats.zscore(df[col]))
# #         df = df[z_scores <= threshold]

# #     return df

# import pandas as pd
# from sklearn.cluster import DBSCAN
# from sklearn.preprocessing import StandardScaler
# import logging

# logger = logging.getLogger(__name__)

# def remove_outliers(df: pd.DataFrame, column_dtypes: dict, eps: float = 0.5, min_samples: int = 5) -> pd.DataFrame:
#     """
#     Identify and remove outliers from numeric columns using DBSCAN.

#     Args:
#         df: Input DataFrame
#         column_dtypes: Dictionary of column data types
#         eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other
#         min_samples: The number of samples in a neighborhood for a point to be considered as a core point

#     Returns:
#         DataFrame with outliers removed
#     """
#     logger.info("Removing outliers using DBSCAN...")
#     numeric_cols = [col for col in df.columns if column_dtypes[col] == "numeric"]
    
#     if not numeric_cols:
#         logger.warning("No numeric columns found for outlier detection.")
#         return df

#     # Standardize the numeric columns
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(df[numeric_cols])

#     # Apply DBSCAN
#     dbscan = DBSCAN(eps=eps, min_samples=min_samples)
#     labels = dbscan.fit_predict(X_scaled)

#     # Remove outliers (points labeled as -1 by DBSCAN)
#     df_clean = df[labels != -1]

#     outliers_removed = len(df) - len(df_clean)
#     logger.info(f"Removed {outliers_removed} outliers. Rows reduced from {len(df)} to {len(df_clean)}")

#     return df_clean


import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)

def remove_outliers(df: pd.DataFrame, column_dtypes: dict, eps: float = 0.5, min_samples: int = 5, n_components: int = 2) -> pd.DataFrame:
    """
    Identify and remove outliers from numeric columns using PCA and DBSCAN.

    Args:
        df: Input DataFrame
        column_dtypes: Dictionary of column data types
        eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other
        min_samples: The number of samples in a neighborhood for a point to be considered as a core point
        n_components: Number of principal components to retain

    Returns:
        DataFrame with outliers removed
    """
    logger.info("Removing outliers using PCA and DBSCAN...")
    numeric_cols = [col for col in df.columns if column_dtypes[col] == "numeric"]

    if not numeric_cols:
        logger.warning("No numeric columns found for outlier detection.")
        return df

    # Standardize the numeric columns
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[numeric_cols])

    # Apply PCA to reduce dimensions
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)

    # Apply DBSCAN on reduced data
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X_pca)

    # Remove outliers (points labeled as -1 by DBSCAN)
    df_clean = df[labels != -1]

    outliers_removed = len(df) - len(df_clean)
    logger.info(f"Removed {outliers_removed} outliers. Rows reduced from {len(df)} to {len(df_clean)}")

    return df_clean
