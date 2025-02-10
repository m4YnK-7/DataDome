import os
import pandas as pd
from ydata_profiling import ProfileReport

def profile_report(input_file_path):
    # Check if file exists and is not empty
    if not input_file_path or not os.path.exists(input_file_path) or os.path.getsize(input_file_path) == 0:
        raise ValueError("Uploaded file is empty or invalid.")

    df = pd.read_csv(input_file_path)

    if df.empty:
        raise ValueError("Uploaded CSV has no data.")

    profile = ProfileReport(df, title="Pandas Profiling Report", minimal=True)
    profile.to_file(r"output\profile_report.html")

