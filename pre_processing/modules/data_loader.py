import pandas as pd

def load_and_preprocess_dataset(file_path):
    """
    Load dataset from CSV or Excel, with error handling and basic preprocessing.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")
    except Exception as e:
        raise IOError(f"Error loading file: {e}")
    
    report = {
        'original_shape': list(df.shape),
        'column_indices': {col: idx for idx, col in enumerate(df.columns)},
    }
    
    return df, report