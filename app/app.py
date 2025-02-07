import os
from flask import Flask, request, render_template, jsonify
from model import train_and_predict

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables to store file paths
train_path = None
test_path = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    global train_path, test_path

    if "train_file" not in request.files or "test_file" not in request.files:
        return jsonify({"error": "Please upload both train and test CSV files."})

    train_file = request.files["train_file"]
    test_file = request.files["test_file"]

    if train_file.filename == "" or test_file.filename == "":
        return jsonify({"error": "No selected file."})

    train_path = os.path.join(UPLOAD_FOLDER, train_file.filename)
    test_path = os.path.join(UPLOAD_FOLDER, test_file.filename)
    train_file.save(train_path)
    test_file.save(test_path)

    return jsonify({"message": "Files uploaded successfully."})

@app.route("/run_model", methods=["POST"])
def run_model():
    global train_path, test_path

    if not train_path or not test_path:
        return jsonify({"error": "Files not uploaded yet."})

    data = request.get_json()
    model_name = data.get("model_name")

    if model_name not in ["linear_regression", "decision_tree", "random_forest", "svm", "knn", "logistic_regression", "gradient_boosting", "xgboost"]:
        return jsonify({"error": "Invalid model selection."})

    results = train_and_predict(train_path, test_path, model_name)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
