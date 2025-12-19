from fuzzy_system.core import evaluate_system
from variables import (
    market_value, location, asset, income, interest,
    house, applicant, credit,
    stage1_rules, stage2_rules, stage3_rules
)

def get_credit_system_config():
    variables = {
        'Market_value': market_value,
        'Location': location,
        'Asset': asset,
        'Income': income,
        'Interest': interest,
        'House': house,
        'Applicant': applicant,
        'Credit': credit
    }

    return {
        'variables': variables,
        'stage1_rules': stage1_rules,
        'stage2_rules': stage2_rules,
        'stage3_rules': stage3_rules
    }

def calculate_credit(inputs):
    config = get_credit_system_config()
    variables = config['variables']

    # Stage 1
    stage1_system = {
        'variables': variables,
        'rules': config['stage1_rules'],
        'output_variables': ['House']
    }
    stage1_results = evaluate_system(stage1_system, inputs)
    inputs['House'] = stage1_results['House'] # Feed forward

    # Stage 2
    stage2_system = {
        'variables': variables,
        'rules': config['stage2_rules'],
        'output_variables': ['Applicant']
    }
    stage2_results = evaluate_system(stage2_system, inputs)
    inputs['Applicant'] = stage2_results['Applicant'] # Feed forward

    # Stage 3
    stage3_system = {
        'variables': variables,
        'rules': config['stage3_rules'],
        'output_variables': ['Credit']
    }
    stage3_results = evaluate_system(stage3_system, inputs)
    
    return {
        'House_Score': stage1_results['House'],
        'Applicant_Score': stage2_results['Applicant'],
        'Credit_Amount': stage3_results['Credit']
    }
