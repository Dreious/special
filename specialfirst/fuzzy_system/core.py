


def linspace(start, stop, num=50):
    if num == 1:
        return [start]
    step = (stop - start) / (num - 1)
    return [start + step * i for i in range(num)]

def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0

def trapezoidal(x, a, b, c, d):
    if x <= a or x >= d:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return 1.0
    elif c < x < d:
        return (d - x) / (d - c)
    return 0.0

def calculate_membership(x, mf_type, params):
    if mf_type == 'triangular':
        return triangular(x, *params)
    elif mf_type == 'trapezoidal':
        return trapezoidal(x, *params)
    return 0.0

def evaluate_rule_strength(rule, inputs, variables):
    """
    rule: {'antecedents': [('VarName', 'SetName'), ...], 'consequent': ('VarName', 'SetName')}
    inputs: {'VarName': value}
    variables: dict of variable definitions
    """
    strengths = []
    for var_name, set_name in rule['antecedents']:
        if var_name in inputs:
            val = inputs[var_name]
            var_def = variables.get(var_name)
            if var_def and set_name in var_def['sets']:
                set_def = var_def['sets'][set_name]
                strengths.append(calculate_membership(val, set_def['type'], set_def['params']))
            else:
                strengths.append(0.0)
        else:
            strengths.append(0.0)
    
    if not strengths:
        return 0.0
    return min(strengths)

def evaluate_system(system_config, inputs, resolution=100):
    """
    system_config: {
        'variables': {...},
        'rules': [...],
        'output_variables': ['VarName', ...]
    }
    """
    variables = system_config['variables']
    rules = system_config['rules']
    output_var_names = system_config['output_variables']

    # 1. Fuzzification and Inference
    aggregated_fuzzy_output = {} 

    for rule in rules:
        strength = evaluate_rule_strength(rule, inputs, variables)
        
        consequent_var_name, consequent_set_name = rule['consequent']

        if consequent_var_name not in aggregated_fuzzy_output:
            aggregated_fuzzy_output[consequent_var_name] = {}
        
        current_max = aggregated_fuzzy_output[consequent_var_name].get(consequent_set_name, 0.0)
        aggregated_fuzzy_output[consequent_var_name][consequent_set_name] = max(current_max, strength)

    # 2. Defuzzification (Centroid)
    results = {}
    for var_name in output_var_names:
        if var_name not in aggregated_fuzzy_output:
            results[var_name] = 0.0
            continue

        variable = variables[var_name]
        active_sets = aggregated_fuzzy_output[var_name]
        
        x_values = linspace(variable['min'], variable['max'], resolution)
        numerator = 0.0
        denominator = 0.0

        for x in x_values:
            max_membership_at_x = 0.0
            for set_name, rule_strength in active_sets.items():
                set_def = variable['sets'][set_name]
                set_mf_val = calculate_membership(x, set_def['type'], set_def['params'])
                clipped_val = min(rule_strength, set_mf_val)
                max_membership_at_x = max(max_membership_at_x, clipped_val)

            numerator += x * max_membership_at_x
            denominator += max_membership_at_x

        if denominator == 0:
            results[var_name] = 0.0
        else:
            results[var_name] = numerator / denominator

    return results
