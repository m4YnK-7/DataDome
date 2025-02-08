import numpy as np
import pandas as pd
import json

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
