from flask import Flask, request, render_template, send_file, jsonify
import os
import pandas as pd
from profile_report import profile_report
from column import cat_c
from ydata_profiling import ProfileReport
from model import train_predict_regression,visualize_results
import requests
import json


app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# df = pd.read_csv("app/uploads/user_data.csv")  
# numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

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

@app.route("/run_model", methods=["POST"])
def run_model():
    data = request.get_json()
    model_name = data.get("model_name")

    valid_models = ["linear_regression", "decision_tree", "random_forest", "svm", "knn", "logistic_regression", "gradient_boosting", "xgboost"]
    if model_name not in valid_models:
        return jsonify({"error": "Invalid model selection."}), 400
    
    data_csv = r"app\uploads\user_data.csv"

    results = train_predict_regression(data_csv, model_name)
    # path = visualize_results()
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
        file_path = r"app\uploads\submitted_data.json"
        
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
    button_text = data.get("buttonText")
    parent_div = data.get("parentDiv")

    print(f"Button Clicked: {button_text}, Inside Div: {parent_div}")

    return jsonify({"message": "Data received", "buttonText": button_text, "parentDiv": parent_div})

    
if __name__ == "__main__":
    app.run(debug=True)




  

