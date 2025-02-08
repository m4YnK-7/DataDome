import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.preprocessing import StandardScaler

def reduce_dimensionality(df, target_column=None, mode="unsupervised", n_components=0.95, k_best=10):
    """
    Reduces dimensionality using PCA (unsupervised) or Mutual Information (supervised).

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        target_column (str, optional): Target variable for supervised feature selection.
        mode (str): "unsupervised" (PCA) or "supervised" (Mutual Information).
        n_components (float, optional): PCA components (default=0.95 for explained variance).
        k_best (int, optional): Number of best features for Mutual Information.

    Returns:
        pd.DataFrame: DataFrame with reduced dimensions.
    """
    
    # Separate features and target
    X = df.drop(columns=[target_column]) if target_column else df
    y = df[target_column] if target_column else None


    if mode == "unsupervised":
        # PCA: Reduce dimensions while keeping variance
        pca = PCA(n_components=n_components)
        X_pca = pca.fit_transform(X)
        print(f"✅ PCA retained {pca.n_components_} components (explained variance: {sum(pca.explained_variance_ratio_):.2f})")
        return pd.DataFrame(X_pca)

    elif mode == "supervised":
        if y is None:
            raise ValueError("❌ 'target_column' is required for supervised mode (Mutual Information).")
        
        # Select best features using Mutual Information
        selector = SelectKBest(mutual_info_classif, k=k_best)
        X_selected = selector.fit_transform(X, y)
        print(f"✅ Mutual Information selected {X_selected.shape[1]} best features.")
        return pd.DataFrame(X_selected)

    else:
        raise ValueError("❌ Invalid mode. Choose 'unsupervised' (PCA) or 'supervised' (Mutual Information).")
