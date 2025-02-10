import pandas as pd
import numpy as np
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
from sklearn.preprocessing import LabelEncoder

from .pre_processing_utils import convert_to_serializable, infer_column_type

import json
import warnings
warnings.filterwarnings('ignore')

def generate_synthetic_data(df, output_dir = '.', synthetic_fraction=0.2):
    """
    Generate synthetic data using CTGAN with reporting capabilities.
    """
    num_synthetic = int(len(df) * synthetic_fraction)
    df_encoded = df.copy()
    encoders = {}

    categorical_columns = []
    numeric_columns = []
    for column in df.columns:
        _, column_type = infer_column_type(df[column])
        # print(f"Column: {column}, Type: {column_type}")
        if column_type in ['object', 'boolean']: categorical_columns.append(column)
        elif column_type in ['int', 'float']: numeric_columns.append(column)

    for column in categorical_columns:
        le = LabelEncoder()
        encoded_values = le.fit_transform(df[column])
        df_encoded[column] = encoded_values.astype(float)
        encoders[column] = le
    
    numeric_ranges = {
        column: {
            'min': df[column].min(),
            'max': df[column].max(),
            'dtype': df[column].dtype
        }
        for column in numeric_columns
    }
    
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df_encoded)
    
    for column in categorical_columns:
        metadata.update_column(
            column_name=column,
            sdtype='numerical'
        )
    
    model = CTGANSynthesizer(
        epochs=128,
        batch_size=500,
        verbose=True,
        metadata=metadata
    )
    
    print("Training CTGAN model...")
    model.fit(df_encoded)
    
    print(f"Generating {num_synthetic} synthetic samples...")
    synthetic_data = model.sample(num_rows=num_synthetic)
    
    for column in categorical_columns:
        n_categories = len(encoders[column].classes_)
        synthetic_data[column] = synthetic_data[column].astype(float)
        synthetic_data[column] = np.floor(synthetic_data[column]).astype(int) % n_categories
        synthetic_data[column] = encoders[column].inverse_transform(synthetic_data[column])
    
    for column in numeric_ranges.keys():
        synthetic_data[column] = synthetic_data[column].clip(
            numeric_ranges[column]['min'],
            numeric_ranges[column]['max']
        )
        synthetic_data[column] = synthetic_data[column].astype(numeric_ranges[column]['dtype'])
    
    for column in categorical_columns:
        df_encoded[column] = encoders[column].inverse_transform(df_encoded[column].astype(int))
    
    combined_data = pd.concat([df_encoded, synthetic_data], axis=0, ignore_index=True)
    
    # Initial report
    synthesis_report = {
        'original_shape': {
            'rows': int(df.shape[0]),
            'columns': int(df.shape[1])
        },
        'synthetic_fraction': float(synthetic_fraction),
        'categorical_columns': {},
        'numeric_columns': {}
    }
    
    for col in categorical_columns:
        synthesis_report['categorical_columns'][col] = {
            'before_synthesis': {
                'unique_count': int(df[col].nunique()),
                'sample_values': sorted(df[col].unique())[:5]
            }
        }
    
    for col in numeric_columns:
        synthesis_report['numeric_columns'][col] = {
            'before_synthesis': {
                'unique_count': int(df[col].nunique()),
                'range': {
                    'min': float(df[col].min()),
                    'max': float(df[col].max())
                }
            }
        }

    # Post Synthesis
    for col in categorical_columns:
        synthesis_report['categorical_columns'][col]['after_synthesis'] = {
            'unique_count': int(combined_data[col].nunique()),
            'sample_values': sorted(combined_data[col].unique())[:5]
        }
    
    for col in numeric_columns:
        synthesis_report['numeric_columns'][col]['after_synthesis'] = {
            'unique_count': int(combined_data[col].nunique()),
            'range': {
                'min': float(combined_data[col].min()),
                'max': float(combined_data[col].max())
            }
        }
    
    synthesis_report['final_shape'] = {
        'rows': int(combined_data.shape[0]),
        'columns': int(combined_data.shape[1])
    }

    jpath = rf"{output_dir}\profiling_report.json"
    with open(jpath, 'r') as f:
        report = json.load(f)
    
    report['synthetic_data'] = synthesis_report
    with open(jpath, 'w') as f:
        json.dump(report, f, indent=4, default=convert_to_serializable)

    combined_data.to_csv(r"output\synthetic.csv")
    
    return combined_data



   
    