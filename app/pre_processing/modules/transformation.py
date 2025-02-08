import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures

def transform(df):
    """
    Reads a CSV file, normalizes numerical data, encodes categorical features,
    applies feature engineering (log transformation, polynomial features), and
    saves the processed data.

    Parameters:
        file_path (str): Path to the input CSV file.
        output_path (str): Path to save the processed CSV file.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    # Load CSV file
    # df = pd.read_csv(file_path)

    # Identify numeric & categorical columns
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df.select_dtypes(include=['object']).columns.tolist()

    # Scaling numerical features
    scaler = StandardScaler()
    df[numeric_features] = scaler.fit_transform(df[numeric_features])

    # Encoding categorical features (One-Hot Encoding)
    if categorical_features:
        encoder = OneHotEncoder(drop='first', sparse_output=False)
        encoded_cats = pd.DataFrame(encoder.fit_transform(df[categorical_features]), 
                                    columns=encoder.get_feature_names_out(categorical_features))
        df = df.drop(columns=categorical_features).reset_index(drop=True)
        df = pd.concat([df, encoded_cats], axis=1)

    # Log Transformation (Feature Engineering)
    # for col in numeric_features:
    #     if df[col].min() > 0:  # Log transformation requires positive values
    #         df[f"log_{col}"] = np.log1p(df[col])

    # Polynomial Features
    # poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
    # poly_features = poly.fit_transform(df[numeric_features])
    # poly_feature_names = poly.get_feature_names_out(numeric_features)
    # df_poly = pd.DataFrame(poly_features, columns=poly_feature_names)

    # # Merge Polynomial Features into DataFrame
    # df = pd.concat([df, df_poly], axis=1)

    # # Save preprocessed CSV
    # output_path = os.path.join('./output', f'clean_{os.path.basename('transformation.csv')}')
    # df.to_csv("/output/", index=False)

    return df


