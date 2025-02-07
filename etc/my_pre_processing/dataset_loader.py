import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load dataset from various file formats with automatic format detection.
    
    Args:
        file_path: Path to the input file
        
    Returns:
        Loaded DataFrame

    Raises:
        ValueError: If file format is unsupported
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        if file_path.suffix.lower() == ".csv":
            return pd.read_csv(file_path)
        elif file_path.suffix.lower() in [".xlsx", ".xls"]:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    except Exception as e:
        logger.error(f"Error loading dataset: {str(e)}")
        raise
