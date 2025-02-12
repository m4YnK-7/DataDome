import requests
from flask_cors import CORS
from flask import Flask, request, render_template, send_file, jsonify, session

import os
import json
import pandas as pd

from utils.profile_report import profile_report
from utils.categorize_columns import cat_c
import utils.global_store as global_store
from utils.secret_key import generate_secret_key

from pre_processing.models import classification_standard, regression_standard, train_predict_regression,visualize_results,train_predict_classification

app = Flask(__name__)
CORS(app)  

UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SESSION_PERMANENT'] = False

app.secret_key = generate_secret_key()

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

    return render_template("profile.html")

@app.route("/generate", methods=["POST"])
def generateFile():
    profile_report("app/uploads/user_data.csv")
    return send_file(r"..\output\profile_report.html", as_attachment=False)

@app.route("/attribute_cleaning")
def attribute_cleaning():
    df = pd.read_csv("app/uploads/user_data.csv")

    categorized = cat_c(df)
    categorical_data = {}
    for col in categorized["categorical"]:
        categorical_data[col] = df[col].dropna().unique().tolist()
    return render_template("attribute_cleaning.html", 
                           columns = categorical_data,
                           numeric=categorized["numeric"], 
                           categorical=categorized["categorical"], 
                           datetime=categorized["datetime"], 
                           categorical_data=categorical_data)

@app.route("/models")
def models():
    return render_template("models.html")

#___________________________________________________________________________________________________________________________________
@app.route("/run_model", methods=["POST"])
def run_model():
    data = request.get_json()
    model_name = data.get("model_name")

    valid_models = ["linear_regression", "decision_tree", "random_forest", "svm", "knn", "logistic_regression", "gradient_boosting", "xgboost"]
    if model_name not in valid_models:
        return jsonify({"error": "Invalid model selection."}), 400
    
    # Retrieve result_array from session
    result_array = session.get("result_array")
    print(result_array[2])

    data_csv = r"app\uploads\user_data.csv"

    results = {}

    if(result_array[1] == "prediction"):
        results, y_test, y_test_pred = train_predict_regression(data_csv, model_name,target = result_array[2])
        un_results, un_y_test, un_y_test_pred = regression_standard(data_csv, model_name,target = result_array[2])
    elif(result_array[1] == "classification"):
        results, y_test, y_test_pred = train_predict_classification(data_csv, model_name,target = result_array[2])
        un_results, un_y_test, un_y_test_pred = classification_standard(data_csv, model_name,target = result_array[2])
    else:
        pass
    
    print(results)
    
    visualize_results(
        un_results=un_results,
        un_y_test=un_y_test,    
        un_y_pred=un_y_test_pred,
        pros_results= results,
        pros_test=y_test,
        pros_pred=y_test_pred,
        save_path= r"app\static\metrics.jpeg"
    )

    return jsonify(results)

#_______________________________________________________________________________________________________________________________________--
 
@app.route("/fetch-dataset", methods=["POST"])
def fetch_dataset():
    data = request.json
    print("Received data:", data)  

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
        json_data = request.get_json()
        file_path = r"output/submitted_data.json"
        
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
    
@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    button_text = data.get("buttonText", "Unknown Button")
    parent_div = data.get("parentDiv", "Unknown Div")
    input_value = data.get("inputVal", "No Input")

    result_array = [button_text, parent_div, input_value]

    session["result_array"] = result_array  
    session.modified = True

    print(f"Received Data: {result_array}")

    return jsonify(result_array)

@app.route('/checkbox-data', methods=['POST'])
def checkbox_data():
    data = request.get_json()
    generate_value = data.get("generate", 0) 

    global_store.global_data["checkbox"] = generate_value  
    print(f"Checkbox Value Received: {generate_value}")
    
    return jsonify({"message": "Checkbox value received", "value": generate_value})
    

def app_run():
    app.run(debug=False)

if __name__ == "__main__":
    app.run(debug=False)




  

