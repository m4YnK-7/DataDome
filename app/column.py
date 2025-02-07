import pandas as pd

def cat_c(df):
    # Identify numeric, categorical, and datetime columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Attempt to infer datetime columns
    for col in df.columns:
        if col not in numeric_cols and col not in categorical_cols:
            try:
                df[col] = pd.to_datetime(df[col])
                datetime_cols.append(col)
            except (ValueError, TypeError):
                categorical_cols.append(col)  # If conversion fails, consider it categorical
    
    return {
        "numeric": numeric_cols,  
        "categorical": categorical_cols,  
        "datetime": datetime_cols  
    }  