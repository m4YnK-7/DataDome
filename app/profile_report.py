import pandas as pd
from ydata_profiling import ProfileReport

def profile_report(input_file):
    df = pd.read_csv(input_file, encoding="ISO-8859-1")
    profile = ProfileReport(df, title="Pandas Profiling Report", minimal=True)
    html = profile.to_file("profile_report.html")

    return html
