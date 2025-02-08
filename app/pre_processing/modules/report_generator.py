class ReportGenerator:
    def generate_profiling_report(self, original_df, processed_df, data_cleaner, data_imputer):
        """
        Generate comprehensive profiling report.
        """
        report = {
            'original_dataset': {
                'total_rows': int(original_df.shape[0]),
                'total_columns': int(original_df.shape[1]),
                'column_names': list(original_df.columns)
            },
            'processed_dataset': {
                'total_rows': int(processed_df.shape[0]),
                'total_columns': int(processed_df.shape[1])
            },
            'duplicates': {
                'duplicate_count': len(data_cleaner.duplicate_indices),
                'duplicate_indices': data_cleaner.duplicate_indices
            },
            'missing_values': data_cleaner.missing_info,
            'column_details': {
                col: {
                    'dtype': str(processed_df[col].dtype),
                    'non_null_count': int(processed_df[col].count()),
                    'unique_values': int(processed_df[col].nunique())
                } for col in processed_df.columns
            }
        }
        
        report['type_validation'] = data_cleaner.type_validation_report
        report['outlier_detection'] = data_imputer.outlier_report
        return report