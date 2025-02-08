from flask import Flask, request, render_template, send_file, jsonify
import os
import pandas as pd
from profile_report import profile_report
from column import cat_c
from ydata_profiling import ProfileReport
from model import train_and_predict
import requests
import json


app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

global train_path, test_path
train_path = ""
test_path = ""
df = pd.read_csv("app/uploads/user_data.csv")  # Replace with your actual CSV file
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], "user_data.csv")
    file.save(file_path)

    return render_template("tempindex.html")

@app.route("/generate", methods=["POST"])
def generateFile():
    profile_report("app/uploads/user_data.csv")
    return send_file("..//profile_report.html", as_attachment=False)

@app.route("/columns")
def columns():
    df = pd.read_csv("app/uploads/user_data.csv")

    categorized = cat_c(df)
    categorical_data = {}
    for col in categorized["categorical"]:
        categorical_data[col] = df[col].dropna().unique().tolist()
    return render_template("column.html", 
                           columns = categorical_data,
                           numeric=categorized["numeric"], 
                           categorical=categorized["categorical"], 
                           datetime=categorized["datetime"], 
                           categorical_data=categorical_data)

@app.route("/next")
def next():
    return render_template("next.html")

@app.route("/modeluploadclea", methods=["POST"])
def model_upload_file():
    global train_path, test_path

    if "train_file" not in request.files or "test_file" not in request.files:
        return jsonify({"error": "Please upload both train and test CSV files."}), 400

    train_file = request.files["train_file"]
    test_file = request.files["test_file"]

    if train_file.filename == "" or test_file.filename == "":
        return jsonify({"error": "No selected file."}), 400

    train_path = os.path.join(UPLOAD_FOLDER, train_file.filename)
    test_path = os.path.join(UPLOAD_FOLDER, test_file.filename)
    train_file.save(train_path)
    test_file.save(test_path)

    return jsonify({"message": "Files uploaded successfully."})

@app.route("/run_model", methods=["POST"])
def run_model():
    global train_path, test_path

    if not train_path or not test_path:
        return jsonify({"error": "Files not uploaded yet."}), 400

    data = request.get_json()
    model_name = data.get("model_name")

    valid_models = ["linear_regression", "decision_tree", "random_forest", "svm", "knn", "logistic_regression", "gradient_boosting", "xgboost"]
    if model_name not in valid_models:
        return jsonify({"error": "Invalid model selection."}), 400

    results = train_and_predict(train_path, test_path, model_name)
    return jsonify(results)
 
@app.route("/fetch-dataset", methods=["POST"])
def fetch_dataset():
    data = request.json
    print("Received data:", data)  # Debugging: Print received data

    dataset_url = data.get("url")
    if not dataset_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400

    try:
        response = requests.get(dataset_url, stream=True)
        response.raise_for_status()  # Raises error for HTTP failures

        filename = "user_data.csv"
        filepath = os.path.join(os.getcwd(),"app","uploads", filename)

        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return jsonify({"success": True, "filename": filename})

    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e))  # Debugging: Print error
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/save-file', methods=['POST'])
def save_file():
    try:
        # Get the JSON data from the request
        json_data = request.get_json()
        
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create the file path in the current directory
        file_path = os.path.join(current_dir, 'submitted_data.json')
        
        # Write the JSON data to a file
        with open(file_path, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        return jsonify({
            'message': 'File saved successfully',
            'path': file_path
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
    


    
if __name__ == "__main__":
    app.run(debug=True)




  

