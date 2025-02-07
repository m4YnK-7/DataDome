# # ------------------------------------------------

# import pandas as pd
# import numpy as np
# from datetime import datetime
# from typing import List

# def remove_outliers(
#     df: pd.DataFrame, 
#     numerical_columns: List[str] = None,
#     categorical_columns: List[str] = None,
#     datetime_columns: List[str] = None,
#     datetime_range: tuple = (datetime(2000, 1, 1), datetime(2050, 12, 31))
# ) -> pd.DataFrame:

#     # Create a copy of the original DataFrame
#     cleaned_df = df.copy()

#     # Handle datetime columns
#     if datetime_columns:
#         for col in datetime_columns:
#             # Convert column to datetime (force conversion, setting invalid values to NaT)
#             cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
            
#             # Remove rows where datetime is outside the specified range
#             cleaned_df = cleaned_df[
#                 (cleaned_df[col] >= datetime_range[0]) & 
#                 (cleaned_df[col] <= datetime_range[1])
#             ]

#     # # Handle numerical columns using Z-Score method
#     if numerical_columns:
#         for col in numerical_columns:
#             if cleaned_df[col].dtype.kind in 'biufc':  # Ensure it's a numeric column
#                 z_scores = np.abs((cleaned_df[col] - cleaned_df[col].mean()) / cleaned_df[col].std())
#                 cleaned_df = cleaned_df[z_scores <= 3]

#     # Handle categorical columns
#     if categorical_columns:
#         for col in categorical_columns:
#             value_counts = cleaned_df[col].value_counts()
#             threshold = len(cleaned_df) * 0.05  # 5% threshold
#             valid_categories = value_counts[value_counts >= threshold].index
#             cleaned_df = cleaned_df[cleaned_df[col].isin(valid_categories)]
    
#     print(f"Original dataset size: {len(df)}")
#     print(f"Cleaned dataset size: {len(cleaned_df)}")
#     print(f"Removed {len(df) - len(cleaned_df)} records")
    
#     return cleaned_df

# # Load CSV
# df = pd.read_csv("train.csv")

# # Categorize columns
# from categorize_colums import cat_c
# ans = cat_c(df)

# # Apply outlier removal
# df_cleaned = remove_outliers(df, ans["numeric"], ans["categorical"], ans["datetime"])



import pandas as pd
import numpy as np
from datetime import datetime
from typing import List

def remove_outliers(
    df: pd.DataFrame,
    numerical_columns: List[str] = None,
    categorical_columns: List[str] = None,
    datetime_columns: List[str] = None,
    datetime_range: tuple = (datetime(2000, 1, 1), datetime(2050, 12, 31))
) -> pd.DataFrame:
    """
    Remove outliers from a DataFrame with mixed data types.
    
    Debug-enhanced version with detailed logging and more robust filtering.
    """
    # Create a copy of the original DataFrame
    cleaned_df = df.copy()
    
    # Detailed logging dictionary
    removal_log = {
        'datetime_rows_removed': 0,
        'numerical_rows_removed': 0,
        'categorical_rows_removed': 0
    }
    
    # Handle datetime columns
    # if datetime_columns:
    #     for col in datetime_columns:
    #         # Convert column to datetime (force conversion, setting invalid values to NaT)
    #         cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
            
    #         # Log rows with NaT values
    #         nat_count = cleaned_df[col].isna().sum()
    #         print(f"Datetime column {col}: {nat_count} NaT values")
            
    #         # Remove rows where datetime is outside the specified range
    #         initial_size = len(cleaned_df)
    #         cleaned_df = cleaned_df[
    #             (cleaned_df[col] >= datetime_range[0]) &
    #             (cleaned_df[col] <= datetime_range[1])
    #         ]
    #         removal_log['datetime_rows_removed'] = initial_size - len(cleaned_df)
    
    # Handle numerical columns using Z-Score method
    if numerical_columns:
        for col in numerical_columns:
            # Additional check to ensure column is numeric
            if cleaned_df[col].dtype.kind in 'biufc':
                # Print column statistics before filtering
                print(f"\nNumerical column {col} statistics:")
                print(f"Mean: {cleaned_df[col].mean()}")
                print(f"Std Dev: {cleaned_df[col].std()}")
                print(f"Min: {cleaned_df[col].min()}")
                print(f"Max: {cleaned_df[col].max()}")
                
                # Robust Z-Score calculation with error handling
                try:
                    initial_size = len(cleaned_df)
                    z_scores = np.abs((cleaned_df[col] - cleaned_df[col].mean()) / cleaned_df[col].std())
                    
                    # More flexible Z-Score filtering
                    cleaned_df = cleaned_df[z_scores <= 3]
                    
                    removal_log['numerical_rows_removed'] = initial_size - len(cleaned_df)
                    print("TSET")
                except Exception as e:
                    print(f"Error processing numerical column {col}: {e}")
    
    # Handle categorical columns
    # if categorical_columns:
    #     for col in categorical_columns:
    #         # Print initial value counts
    #         print(f"\nCategorical column {col} initial value counts:")
    #         print(cleaned_df[col].value_counts())
            
    #         # Compute threshold with more robust calculation
    #         threshold = max(5, len(cleaned_df) * 0.05)  # Ensure at least 5 records
            
    #         initial_size = len(cleaned_df)
    #         value_counts = cleaned_df[col].value_counts()
    #         valid_categories = value_counts[value_counts >= threshold].index
            
    #         # Print valid categories
    #         print(f"Valid categories for {col}: {list(valid_categories)}")
            
    #         cleaned_df = cleaned_df[cleaned_df[col].isin(valid_categories)]
    #         removal_log['categorical_rows_removed'] = initial_size - len(cleaned_df)
    
    # Comprehensive removal summary
    print("\n--- Outlier Removal Summary ---")
    print(f"Original dataset size: {len(df)}")
    print(f"Cleaned dataset size: {len(cleaned_df)}")
    print("Rows removed:")
    for key, value in removal_log.items():
        print(f"  {key}: {value}")
    
    return cleaned_df

# Diagnostic print to understand column types
def print_column_types(df):
    print("\nColumn Types:")
    for col in df.columns:
        print(f"{col}: {df[col].dtype}")

# Load CSV
df = pd.read_csv("train.csv")

# Categorize columns
from categorize_colums import cat_c
ans = cat_c(df)

# Apply outlier removal
df_cleaned = remove_outliers(df, ans["numeric"], ans["categorical"], ans["datetime"])
