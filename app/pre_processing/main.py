import os
import json
from pre_processing.modules.data_loader import load_and_preprocess_dataset
from pre_processing.modules.data_cleaner import DataCleaner
from pre_processing.modules.data_imputer import DataImputer
from pre_processing.modules.report_generator import ReportGenerator
from pre_processing.modules.utils import convert_to_serializable
from pre_processing.modules.transformation import transform
from pre_processing.modules.synthetic import generate_synthetic_data
from pre_processing.modules.rule_based_cleaning import rule_based_cleaning

import warnings 
warnings.filterwarnings('ignore') 

def main(file_path, output_dir='app\output', gen_syn_data=False, target=None, task=None):

    data_cleaner = DataCleaner()
    data_imputer = DataImputer()
    report_generator = ReportGenerator()
    
    # Load and process data
    original_df, initial_report = load_and_preprocess_dataset(file_path)

    # original_df = rule_based_cleaning(original_df,r"app\uploads\submitted_data.json")
    
    # Clean data
    processed_df,column_dtype = data_cleaner.infer_and_validate_column_types(original_df)
    processed_df = data_cleaner.identify_duplicate_rows(processed_df)
    data_cleaner.detect_missing_values(processed_df)
        
    # Impute missing values
    processed_df = data_imputer.impute_missing_values(processed_df,column_dtype)
    
    # Generate report
    profiling_report = report_generator.generate_profiling_report(
        original_df, processed_df, data_cleaner, data_imputer
    )
    profiling_report_path = os.path.join(output_dir, 'profiling_report.json')
    with open(profiling_report_path, 'w') as f:
        json.dump({
            'initial_report': initial_report,
            'profiling_report': profiling_report
        }, f, indent=4, default=convert_to_serializable)

    # Generate synthetic data
    if gen_syn_data: processed_df = generate_synthetic_data(processed_df, output_dir)
    
    # transformation
    # processed_df = transform(processed_df, target_column=target, task=task)
    
    processed_dataset_path = os.path.join(output_dir, f'clean_{os.path.basename(file_path)}')
    processed_df.to_csv(processed_dataset_path, index=False)
    
    return processed_df, profiling_report


if __name__ == "__main__":
    file_path = r"app\uploads\user_data.csv"
    processed_data, report = main(file_path)