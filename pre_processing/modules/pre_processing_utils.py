import numpy as np
import pandas as pd
import re

def convert_to_serializable(obj):
    """
    Convert non-serializable objects to JSON-compatible types.
    """
    if isinstance(obj, (np.integer, np.floating)):
        return int(obj) if isinstance(obj, np.integer) else float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.core.indexes.base.Index):
        return obj.tolist()
    return obj

def infer_column_type(series):
    def extract_numeric(value):
        if pd.isna(value):
            return np.nan
        if isinstance(value, (int, float)):
            return value
        
        match = re.search(r'[-+]?(?:\d*\.\d+|\d+)', str(value))
        return float(match.group()) if match else np.nan

    series = series.astype(str).str.strip()
    
    bool_map = {'true': True, 'false': False, '1': True, '0': False}
    boolean_values = series.str.lower().map(bool_map)
    if boolean_values.notna().all():
        return boolean_values, 'boolean'
    
    numeric_values = series.apply(extract_numeric)
    if numeric_values.notna().any():
        if numeric_values.nunique() / len(series) > 0.2:
            if numeric_values.apply(float.is_integer).all():
                return numeric_values.astype(int), 'int'
            else:
                return numeric_values, 'float'
        else:
            return numeric_values, 'object'
    
    return series, 'object'