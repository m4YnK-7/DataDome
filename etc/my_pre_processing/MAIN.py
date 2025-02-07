import json
import warnings
from pathlib import Path
import logging

from logging_config import logger
from dataset_loader import load_dataset
from data_type_converter import infer_and_convert_dtypes
from duplicate_removal import remove_duplicates
from corr_anlys import calculate_correlations, drop_weak_correlations
from missing_value import handle_missing_values
from outlier import remove_outliers

warnings.filterwarnings("ignore")

file_path = "train.csv"

try:
    df = load_dataset(file_path)

    df, column_dtypes = infer_and_convert_dtypes(df)
    df = remove_duplicates(df)

    # correlation_scores = calculate_correlations(df)
    # df = drop_weak_correlations(df, correlation_scores, threshold=-1.0)

    # df = handle_missing_values(df, column_dtypes)
    # df = remove_outliers(df, column_dtypes, threshold=3.0)

    output_path = Path(file_path).stem + "_cleaned.csv"
    df.to_csv(output_path, index=False)

    logger.info("Dataset processing completed successfully")

except Exception as e:
    logger.error(f"Error processing dataset: {str(e)}")
