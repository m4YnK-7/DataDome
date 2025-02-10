from sklearn.impute import KNNImputer
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd

class DataImputer:
    def __init__(self, n_neighbors=7):
        self.n_neighbors = n_neighbors
        self.scaler = StandardScaler()
        self.imputer = KNNImputer(n_neighbors=n_neighbors)

        self.outlier_report = {}
    
    def knn(self, df):
        """
        Fast and accurate missing value imputation using KNN. Better than IRMI
        """
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        
        df_imputed = df.copy()
        
        if len(numeric_columns) > 0:
            numeric_data = df[numeric_columns]
            scaled_data = self.scaler.fit_transform(numeric_data)
            imputed_scaled_data = self.imputer.fit_transform(scaled_data)
            df_imputed[numeric_columns] = self.scaler.inverse_transform(imputed_scaled_data)
        
        for col in categorical_columns:
            df_imputed[col] = df_imputed[col].fillna(df_imputed[col].mode()[0])
        
        return df_imputed
    
    def impute_missing_values(self,df: pd.DataFrame, column_dtypes: dict, eps: float = 0.5, min_samples: int = 5, n_components: int = 2) -> pd.DataFrame:
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
        # df = self.knn(df)
        numeric = ['int','float']
        numeric_cols = [col for col in df.columns if column_dtypes[col] in numeric ]

        if not numeric_cols:

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
        outlier_indices = df[labels == -1].index.tolist()

        outliers_removed = len(df) - len(df_clean)
        # print(outliers_removed)
        self.outlier_report = {
            'outliers_removed': outliers_removed,
            'outlier_percentage': outliers_removed / len(df) * 100,
            'outlier_indices': outlier_indices
        }
        
        return df_clean

