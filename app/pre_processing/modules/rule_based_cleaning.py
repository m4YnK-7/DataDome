import pandas as pd
import json

def rule_based_cleaning_processor(df: pd.DataFrame, rules: dict = {}):
    for column, rule in rules.items():
        try:
            if isinstance(rule[0], str) and rule[0].isnumeric(): 
                df = df[df[column].isnull() | df[column].between(rule[0], rule[1])]
            else:
                raise
        except:
            df = df[~df[column].isin(rule)]
            
    return df

def rule_based_cleaning(df , file_path = "submitted_data.json"):
    with open(file_path , 'r') as file:
        rules = json.load(file)
    return rule_based_cleaning_processor(df,rules)

