
from fuzzy_system.core import evaluate_system

def create_variable(min_val, max_val):
    return {
        'min': min_val,
        'max': max_val,
        'sets': {}
    }

def add_set(variable, name, mf_type, params):
    variable['sets'][name] = {
        'type': mf_type,
        'params': params
    }

def get_credit_system_config():
    variables = {}

    # --- GİRİŞLER ---
    
    # 1. Piyasa Değeri (0 - 1,000,000 USD)
    variables['Market_value'] = create_variable(0, 1000000)
    add_set(variables['Market_value'], "Low", "trapezoidal", [0, 0, 100000, 300000])
    add_set(variables['Market_value'], "Medium", "triangular", [200000, 400000, 600000])
    add_set(variables['Market_value'], "High", "triangular", [500000, 700000, 900000])
    add_set(variables['Market_value'], "Very_High", "trapezoidal", [800000, 900000, 1000000, 1000000])

    # 2. Konum (0 - 10)
    variables['Location'] = create_variable(0, 10)
    add_set(variables['Location'], "Bad", "trapezoidal", [0, 0, 2, 4])
    add_set(variables['Location'], "Fair", "triangular", [3, 5, 7])
    add_set(variables['Location'], "Excellent", "trapezoidal", [6, 8, 10, 10])

    # 3. Varlık (0 - 1,000,000 USD)
    variables['Asset'] = create_variable(0, 1000000)
    add_set(variables['Asset'], "Low", "trapezoidal", [0, 0, 100000, 300000])
    add_set(variables['Asset'], "Medium", "triangular", [200000, 400000, 600000])
    add_set(variables['Asset'], "High", "trapezoidal", [500000, 700000, 1000000, 1000000])

    # 4. Gelir (0 - 200,000 USD/Yıl)
    variables['Income'] = create_variable(0, 200000)
    add_set(variables['Income'], "Low", "trapezoidal", [0, 0, 30000, 60000])
    add_set(variables['Income'], "Medium", "triangular", [40000, 80000, 120000])
    add_set(variables['Income'], "High", "triangular", [100000, 140000, 180000])
    add_set(variables['Income'], "Very_High", "trapezoidal", [160000, 180000, 200000, 200000])

    # 5. Faiz (0 - 20 %)
    variables['Interest'] = create_variable(0, 20)
    add_set(variables['Interest'], "Low", "trapezoidal", [0, 0, 5, 8])
    add_set(variables['Interest'], "Medium", "triangular", [6, 10, 14])
    add_set(variables['Interest'], "High", "trapezoidal", [12, 15, 20, 20])

    # --- ARA ÇIKIŞLAR ---

    # Ev (0 - 10)
    variables['House'] = create_variable(0, 10)
    add_set(variables['House'], "Very_Low", "trapezoidal", [0, 0, 1, 3])
    add_set(variables['House'], "Low", "triangular", [2, 4, 6])
    add_set(variables['House'], "Medium", "triangular", [4, 6, 8])
    add_set(variables['House'], "High", "triangular", [6, 8, 9])
    add_set(variables['House'], "Very_High", "trapezoidal", [8, 9, 10, 10])

    # Başvuru Sahibi (0 - 10)
    variables['Applicant'] = create_variable(0, 10)
    add_set(variables['Applicant'], "Low", "trapezoidal", [0, 0, 3, 5])
    add_set(variables['Applicant'], "Medium", "triangular", [3, 5, 7])
    add_set(variables['Applicant'], "High", "trapezoidal", [6, 8, 10, 10])

    # --- NİHAİ ÇIKIŞ ---

    # Kredi (0 - 500,000 USD)
    variables['Credit'] = create_variable(0, 500000)
    add_set(variables['Credit'], "Very_Low", "trapezoidal", [0, 0, 50000, 100000])
    add_set(variables['Credit'], "Low", "triangular", [50000, 100000, 250000])
    add_set(variables['Credit'], "Medium", "triangular", [200000, 300000, 400000])
    add_set(variables['Credit'], "High", "triangular", [300000, 400000, 450000])
    add_set(variables['Credit'], "Very_High", "trapezoidal", [400000, 450000, 500000, 500000])

    # --- RULES ---
    
    # Stage 1 Rules
    stage1_rules = [
        {'antecedents': [("Location", "Bad"), ("Market_value", "Low")], 'consequent': ("House", "Very_Low")},
        {'antecedents': [("Location", "Bad"), ("Market_value", "Medium")], 'consequent': ("House", "Low")},
        {'antecedents': [("Location", "Bad"), ("Market_value", "High")], 'consequent': ("House", "Medium")},
        {'antecedents': [("Location", "Bad"), ("Market_value", "Very_High")], 'consequent': ("House", "Medium")},
        
        {'antecedents': [("Location", "Fair"), ("Market_value", "Low")], 'consequent': ("House", "Low")},
        {'antecedents': [("Location", "Fair"), ("Market_value", "Medium")], 'consequent': ("House", "Medium")},
        {'antecedents': [("Location", "Fair"), ("Market_value", "High")], 'consequent': ("House", "High")},
        {'antecedents': [("Location", "Fair"), ("Market_value", "Very_High")], 'consequent': ("House", "High")},
        
        {'antecedents': [("Location", "Excellent"), ("Market_value", "Low")], 'consequent': ("House", "Medium")},
        {'antecedents': [("Location", "Excellent"), ("Market_value", "Medium")], 'consequent': ("House", "High")},
        {'antecedents': [("Location", "Excellent"), ("Market_value", "High")], 'consequent': ("House", "Very_High")},
        {'antecedents': [("Location", "Excellent"), ("Market_value", "Very_High")], 'consequent': ("House", "Very_High")},
        
        {'antecedents': [("Location", "Bad"), ("Market_value", "Very_High")], 'consequent': ("House", "Medium")},
        {'antecedents': [("Location", "Excellent"), ("Market_value", "Low")], 'consequent': ("House", "Medium")}
    ]

    # Stage 2 Rules
    stage2_rules = [
        {'antecedents': [("Income", "Low"), ("Asset", "Low")], 'consequent': ("Applicant", "Low")},
        {'antecedents': [("Income", "Low"), ("Asset", "Medium")], 'consequent': ("Applicant", "Low")},
        {'antecedents': [("Income", "Low"), ("Asset", "High")], 'consequent': ("Applicant", "Medium")},
        
        {'antecedents': [("Income", "Medium"), ("Asset", "Low")], 'consequent': ("Applicant", "Low")},
        {'antecedents': [("Income", "Medium"), ("Asset", "Medium")], 'consequent': ("Applicant", "Medium")},
        {'antecedents': [("Income", "Medium"), ("Asset", "High")], 'consequent': ("Applicant", "High")},
        
        {'antecedents': [("Income", "High"), ("Asset", "Low")], 'consequent': ("Applicant", "Medium")},
        {'antecedents': [("Income", "High"), ("Asset", "Medium")], 'consequent': ("Applicant", "High")},
        {'antecedents': [("Income", "High"), ("Asset", "High")], 'consequent': ("Applicant", "High")},
        
        {'antecedents': [("Income", "Very_High"), ("Asset", "Low")], 'consequent': ("Applicant", "Medium")},
        {'antecedents': [("Income", "Very_High"), ("Asset", "Medium")], 'consequent': ("Applicant", "High")},
        {'antecedents': [("Income", "Very_High"), ("Asset", "High")], 'consequent': ("Applicant", "High")}
    ]

    # Stage 3 Rules
    stage3_rules = [
        {'antecedents': [("Applicant", "Low"), ("House", "Very_Low")], 'consequent': ("Credit", "Very_Low")},
        {'antecedents': [("Applicant", "Low"), ("House", "Low")], 'consequent': ("Credit", "Very_Low")},
        
        {'antecedents': [("Applicant", "Low"), ("Income", "High")], 'consequent': ("Credit", "Low")},
        {'antecedents': [("Applicant", "Low"), ("House", "High")], 'consequent': ("Credit", "Low")},
        
        {'antecedents': [("Applicant", "Medium"), ("House", "Low")], 'consequent': ("Credit", "Low")},
        {'antecedents': [("Applicant", "Medium"), ("House", "Medium"), ("Interest", "Medium")], 'consequent': ("Credit", "Medium")},
        {'antecedents': [("Applicant", "Medium"), ("House", "High")], 'consequent': ("Credit", "Medium")},
        
        {'antecedents': [("Applicant", "High"), ("House", "Low")], 'consequent': ("Credit", "Medium")},
        {'antecedents': [("Applicant", "High"), ("House", "Medium")], 'consequent': ("Credit", "High")},
        {'antecedents': [("Applicant", "High"), ("House", "High"), ("Interest", "Low")], 'consequent': ("Credit", "Very_High")},
        
        {'antecedents': [("Interest", "High"), ("Applicant", "Medium")], 'consequent': ("Credit", "Low")},
        {'antecedents': [("Interest", "High"), ("Applicant", "High")], 'consequent': ("Credit", "Medium")},
        
        {'antecedents': [("Income", "Very_High"), ("House", "Very_High")], 'consequent': ("Credit", "Very_High")},
        {'antecedents': [("Income", "Low"), ("House", "High")], 'consequent': ("Credit", "Low")},
        
        {'antecedents': [("Applicant", "High"), ("House", "Very_High"), ("Interest", "Low")], 'consequent': ("Credit", "Very_High")}
    ]

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
