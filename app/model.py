import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
# from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
from pre_processing.main import main

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


models = {
    "linear_regression": LinearRegression(),
    "decision_tree": DecisionTreeRegressor(),
    "random_forest": RandomForestRegressor(),
    "svm": SVR(),
    "knn": KNeighborsRegressor(),
    "logistic_regression": LogisticRegression(),
    "gradient_boosting": GradientBoostingRegressor(),
    # "xgboost": XGBRegressor()
}

def preprocess_data(csv_path):
    data = pd.read_csv(csv_path)
    
    for col in data.columns:
        if data[col].dtype == 'object':
            encoder = LabelEncoder()
            data[col] = encoder.fit_transform(data[col].astype(str))

    data.fillna(data.mean(), inplace=True)
    return data

def train_and_predict(data_csv, model_name):
    data,_ = main(data_csv) 

    X = data.iloc[:, :-1]
    print("TEST")
    y = data.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = models.get(model_name)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    
    # Use a separate MinMaxScaler for y
    y_scaler = MinMaxScaler()
    y_train_reshaped = y_train.values.reshape(-1, 1)  # Reshape to 2D
    y_scaler.fit(y_train_reshaped)  # Fit on target variable only

    # Reshape predictions before inverse transform
    y_pred_reshaped = predictions.reshape(-1, 1)
    y_pred_original = y_scaler.inverse_transform(y_pred_reshaped)

    return {
        "model": model_name,
        "predictions": y_pred_original.tolist()
    }
