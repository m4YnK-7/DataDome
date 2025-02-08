import warnings
from pathlib import Path

from module.logging_config import logger
from module.dataset_loader import load_dataset
from module.datatype_converter import infer_and_convert_dtypes
from module.duplicate_removal import remove_duplicates
from module.correlation_analysis import  drop_weak_correlations
from module.missing_value import handle_missing_values
from module.outlier_removal import remove_outliers
from module.transformation import transform
from module.reduction import reduce_dimensionality

warnings.filterwarnings("ignore")

file_path = "app\\uploads\\user_data.csv"

try:
    df = load_dataset(file_path)

    df, column_dtypes = infer_and_convert_dtypes(df)
    df = remove_duplicates(df)
    # df = drop_weak_correlations(df, threshold=-1.0)
    df = handle_missing_values(df, column_dtypes)
    df = remove_outliers(df, column_dtypes)

    df = transform(df)
    

    output_path = "data\\output\\"+Path(file_path).stem + "_transformed.csv"
    df.to_csv(output_path, index=False)

    logger.info("Dataset processing completed successfully")

except Exception as e:
    logger.error(f"Error processing dataset: {str(e)}")
