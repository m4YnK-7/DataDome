import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from scipy import stats
import hashlib
import warnings
import json
from datetime import datetime
import logging
from pathlib import Path
from typing import Tuple, Dict, List, Any, Optional, Union

# Configure logging with detailed formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('preprocessing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    """
    A comprehensive data preprocessing pipeline that handles cleaning, validation,
    and profiling of datasets with support for multiple data types and optimized
    performance for large datasets.
    """
    
    def _init_(self, 
                 chunk_size: int = 10000,
                 correlation_threshold: float = -1.0,
                 outlier_threshold: float = 3.0):
        """
        Initialize the preprocessor with configurable parameters.
        
        Args:
            chunk_size: Size of chunks for processing large datasets
            correlation_threshold: Z-score threshold for correlation filtering
            outlier_threshold: Z-score threshold for outlier detection
        """
        self.chunk_size = chunk_size
        self.correlation_threshold = correlation_threshold
        self.outlier_threshold = outlier_threshold
        
        # Initialize storage dictionaries
        self.index_store = {
            'row_indices': None,
            'column_indices': None,
            'duplicate_indices': None,
            'missing_value_indices': None,
            'invalid_dtype_indices': None,
            'outlier_indices': None
        }
        self.correlation_scores = None
        self.profile_report = {}
        self.column_dtypes = {}
        
    def load_dataset(self, file_path: str) -> pd.DataFrame:
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
            if file_path.suffix.lower() == '.csv':
                return pd.read_csv(file_path)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise
            
    def identify_indices(self, df: pd.DataFrame) -> None:
        """
        Store index positions of rows and columns for tracking.
        
        Args:
            df: Input DataFrame
        """
        self.index_store['row_indices'] = df.index.tolist()
        self.index_store['column_indices'] = df.columns.tolist()
        
    def infer_and_convert_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Infer and convert column data types, handling dates, numerics, and categories.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with properly converted data types
        """
        logger.info("Inferring and converting data types...")
        df_converted = df.copy()
        
        for column in df.columns:
            # Try datetime conversion first
            try:
                df_converted[column] = pd.to_datetime(df[column])
                self.column_dtypes[column] = 'datetime'
                logger.debug(f"Column '{column}' converted to datetime")
                continue
            except (ValueError, TypeError):
                pass
            
            # Try numeric conversion
            try:
                df_converted[column] = pd.to_numeric(df[column])
                self.column_dtypes[column] = 'numeric'
                logger.debug(f"Column '{column}' converted to numeric")
                continue
            except (ValueError, TypeError):
                pass
            
            # Fall back to categorical
            df_converted[column] = df[column].astype('category')
            self.column_dtypes[column] = 'categorical'
            logger.debug(f"Column '{column}' converted to categorical")
            
        return df_converted
        
    def generate_chunk_hash(self, chunk: pd.DataFrame) -> str:
        """
        Generate a hash for a chunk of data for duplicate detection.
        
        Args:
            chunk: DataFrame chunk
            
        Returns:
            Hash string of the chunk
        """
        return hashlib.md5(pd.util.hash_pandas_object(chunk).values).hexdigest()
        
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate rows using memory-efficient chunk processing.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with duplicates removed
        """
        logger.info("Removing duplicate rows...")
        
        # Store duplicate indices before removal
        self.index_store['duplicate_indices'] = df[df.duplicated()].index.tolist()
        
        # Remove duplicates efficiently
        return df.drop_duplicates(keep='first')
        
    def prepare_numeric_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert all features to numeric format for correlation analysis.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with all features in numeric format
        """
        df_numeric = df.copy()
        
        for column in df.columns:
            if self.column_dtypes[column] == 'datetime':
                # Convert datetime to Unix timestamp
                df_numeric[column] = df_numeric[column].astype(np.int64) // 10**9
            elif self.column_dtypes[column] == 'categorical':
                # Convert categorical to numeric using label encoding
                df_numeric[column] = df_numeric[column].cat.codes
                
        return df_numeric
        
    def calculate_correlations(self, df: pd.DataFrame) -> None:
        """
        Calculate correlations with the target variable.
        
        Args:
            df: Input DataFrame
        """
        logger.info("Calculating correlations...")
        
        # Convert features to numeric format
        df_numeric = self.prepare_numeric_features(df)
        
        # Calculate correlations with target
        target_col = df.columns[-1]
        self.correlation_scores = df_numeric.corrwith(df_numeric[target_col]).abs()
        
    def drop_weak_correlations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove columns with weak correlations based on Z-score threshold.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with weak correlations removed
        """
        if self.correlation_scores is None:
            self.calculate_correlations(df)
            
        # Calculate Z-scores of correlations
        correlation_zscores = stats.zscore(self.correlation_scores)
        
        # Identify columns to keep
        columns_to_keep = self.correlation_scores[
            correlation_zscores > self.correlation_threshold
        ].index.tolist()
        
        # Always keep the target column
        if df.columns[-1] not in columns_to_keep:
            columns_to_keep.append(df.columns[-1])
            
        return df[columns_to_keep]
        
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect and impute missing values using type-appropriate methods.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with imputed values
        """
        logger.info("Handling missing values...")
        
        # Store missing value indices
        self.index_store['missing_value_indices'] = {
            col: df[df[col].isna()].index.tolist()
            for col in df.columns
        }
        
        df_imputed = df.copy()
        
        # Handle each column based on its type
        for column in df.columns:
            if df[column].isna().any():
                if self.column_dtypes[column] == 'datetime':
                    # Forward/backward fill for datetime
                    df_imputed[column] = df_imputed[column].fillna(method='ffill').fillna(method='bfill')
                elif self.column_dtypes[column] == 'categorical':
                    # Mode imputation for categorical
                    df_imputed[column] = df_imputed[column].fillna(df_imputed[column].mode()[0])
                else:  # numeric
                    numeric_cols = [col for col in df.columns if self.column_dtypes[col] == 'numeric']
                    if len(numeric_cols) > 1:
                        # Random Forest imputation for multiple numeric columns
                        imputer = IterativeImputer(
                            estimator=RandomForestRegressor(n_estimators=100),
                            max_iter=10,
                            random_state=42
                        )
                        df_imputed[numeric_cols] = imputer.fit_transform(df[numeric_cols])
                    else:
                        # Mean imputation for single numeric column
                        df_imputed[column] = df_imputed[column].fillna(df_imputed[column].mean())
                        
        return df_imputed
        
    def remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify and remove statistical outliers from numeric columns.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with outliers removed
        """
        logger.info("Removing outliers...")
        
        self.index_store['outlier_indices'] = {}
        numeric_cols = [col for col in df.columns if self.column_dtypes[col] == 'numeric']
        
        for col in numeric_cols:
            z_scores = np.abs(stats.zscore(df[col]))
            outlier_mask = z_scores > self.outlier_threshold
            self.index_store['outlier_indices'][col] = df[outlier_mask].index.tolist()
            
        # Remove all identified outliers
        all_outlier_indices = set().union(*[set(indices) for indices in self.index_store['outlier_indices'].values()])
        return df.drop(index=all_outlier_indices)
        
    def generate_profile_report(self, df: pd.DataFrame) -> Dict:
        """
        Generate a comprehensive data profile report.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary containing the profile report
        """
        logger.info("Generating profile report...")
        
        self.profile_report = {
            'dataset_info': {
                'rows': len(df),
                'columns': len(df.columns),
                'memory_usage': df.memory_usage(deep=True).sum(),
                'duplicate_rows': len(self.index_store['duplicate_indices']) if self.index_store['duplicate_indices'] else 0
            },
            'column_profiles': {},
            'correlation_analysis': self.correlation_scores.to_dict() if self.correlation_scores is not None else {},
            'missing_values': {
                col: len(indices) for col, indices in self.index_store['missing_value_indices'].items()
            },
            'outliers': {
                col: len(indices) for col, indices in self.index_store['outlier_indices'].items()
            },
            'processing_timestamp': datetime.now().isoformat()
        }
        
        # Generate column-specific profiles
        for column in df.columns:
            profile = {
                'dtype': self.column_dtypes[column],
                'unique_values': df[column].nunique(),
                'missing_values': df[column].isna().sum(),
                'memory_usage': df[column].memory_usage(deep=True)
            }
            
            if self.column_dtypes[column] == 'numeric':
                profile.update({
                    'mean': df[column].mean(),
                    'std': df[column].std(),
                    'min': df[column].min(),
                    'max': df[column].max(),
                    'quartiles': df[column].quantile([0.25, 0.5, 0.75]).to_dict()
                })
            elif self.column_dtypes[column] == 'datetime':
                profile.update({
                    'min_date': df[column].min().isoformat(),
                    'max_date': df[column].max().isoformat(),
                    'date_range_days': (df[column].max() - df[column].min()).days
                })
            elif self.column_dtypes[column] == 'categorical':
                profile.update({
                    'categories': df[column].value_counts().to_dict()
                })
                
            self.profile_report['column_profiles'][column] = profile
            
        return self.profile_report
        
    def process_dataset(self, file_path: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Process the dataset through the entire preprocessing pipeline.
        
        Args:
            file_path: Path to the input file
            
        Returns:
            Tuple of (cleaned DataFrame, profile report)
            
        Raises:
            Various exceptions with appropriate error messages
        """
        logger.info(f"Starting dataset processing: {file_path}")
        
        try:
            # Load dataset
            df = self.load_dataset(file_path)
            
            # Store initial indices
            self.identify_indices(df)
            
            # Infer and convert data types
            df = self.infer_and_convert_dtypes(df)
            
            # Remove duplicates
            df = self.remove_duplicates(df)
            
            # Calculate correlations and drop weak correlations
            self.calculate_correlations(df)
            df = self.drop_weak_correlations(df)
            
            # Handle missing values
            df = self.handle_missing_values(df)
            
            # Remove outliers
            df = self.remove_outliers(df)
            
            # Generate profile report
            profile_report = self.generate_profile_report(df)
            
            logger.info("Dataset processing completed successfully")
            return df, profile_report
            
        except Exception as e:
            logger.error(f"Error processing dataset: {str(e)}")
            raise


warnings.filterwarnings('ignore')

preprocessor = DataPreprocessor(
    chunk_size=10000,
    correlation_threshold=-1.0,
    outlier_threshold=3.0
)

try:
    file_path = "data.csv" 
    cleaned_df, report = preprocessor.process_dataset(file_path)
    
    output_path = Path(file_path).stem + "_cleaned.csv"
    report_path = Path(file_path).stem + "_report.json"
    
    cleaned_df.to_csv(output_path, index=False)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)
        
    logger.info("Results saved successfully")
    
except Exception as e:
    logger.error(f"Error processing dataset: {str(e)}")