import pandas as pd
import json

def rule_based_cleaning_processor(df: pd.DataFrame, rules: dict = {}):
    for column, rule in rules.items():
            if rule[0].isnumeric(): 
                df = df[df[column].isnull() | df[column].between(int(rule[0]), int(rule[1]))]
            else:
                df = df[~df[column].isin(rule)]
    return df

def rule_based_cleaning(df , file_path ):
    with open(file_path , 'r') as file:
        rules = json.load(file)
    return rule_based_cleaning_processor(df,rules)