from flask import Flask, request, render_template, send_file, jsonify
import os
import pandas as pd
from profile_report import profile_report
from column import cat_c
from ydata_profiling import ProfileReport

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
  
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    filename = "hello.csv"
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    
    
    # Generate report
    profile_report(file)

    return send_file("profile_report.html", as_attachment=False)  

@app.route("/columns")
def columns():
    # Load a sample dataframe (replace this with your actual data)
    df = pd.read_csv("train.csv")  # Replace with actual file

    # Call your function to categorize columns
    categorized = cat_c(df)
    print(categorized)

    # Pass these lists to the template
    return render_template("column.html", 
                           numeric=categorized["numeric"], 
                           categorical=categorized["categorical"], 
                           datetime=categorized["datetime"])

@app.route("/next")
def next():
    return render_template("next.html")

if __name__ == "__main__":
    app.run(debug=True)




  

