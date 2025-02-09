import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pre_processing.modules.utils import infer_column_type

def transform(df, target_column, task):
    """
    Process dataframe by separating target, applying transformations to X, scaling y,
    and returning a concatenated DataFrame.
    """

    scaler = StandardScaler()
    label_encoder = LabelEncoder()

    # Transform target variable (Y)
    if task.lower() == "regression":
        Y = df[target_column].copy().values.reshape(-1, 1)
        Y = scaler.fit_transform(Y)
        Y = pd.DataFrame(Y, columns=[target_column])
    elif task.lower() == "classification":
        Y = label_encoder.fit_transform(df[target_column])  
        Y = pd.DataFrame(Y, columns=[target_column])

    # Process features (X)
    X = df.drop(columns=[target_column]).copy()

    categorical_features = []
    numeric_features = []

    for column in X.columns:
        _, column_type = infer_column_type(X[column])
        if column_type in ['object', 'boolean'] and not any(keyword in column.lower() for keyword in ['date', 'time', 'dt', 'datetime', 'year', 'month', 'day', 'created', 'modified', 'timestamp', 'updated']): 
            categorical_features.append(column)
        elif column_type in ['int', 'float']: numeric_features.append(column)

    # Scale numerical features
    if numeric_features:
        X[numeric_features] = scaler.fit_transform(X[numeric_features])

    # Encode categorical features using Label Encoding
    if categorical_features:
        for col in categorical_features:
            X[col] = label_encoder.fit_transform(X[col])

    X = X.reset_index(drop = True)
    Y = Y.reset_index(drop = True)

    transformed_df = pd.concat([X, Y], axis=1)
    return transformed_df



