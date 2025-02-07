import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
# from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder

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

def train_and_predict(train_csv, test_csv, model_name):
    train_data = preprocess_data(train_csv)
    test_data = preprocess_data(test_csv)

    X_train = train_data.iloc[:, :-1]
    y_train = train_data.iloc[:, -1]

    model = models.get(model_name)
    model.fit(X_train, y_train)

    predictions = model.predict(test_data)

    return {
        "model": model_name,
        "predictions": predictions.tolist()
    }
