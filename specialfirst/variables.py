# --- GİRİŞLER ---

# 1. Piyasa Değeri (0 - 1,000,000 USD)
market_value = {
    'min': 0,
    'max': 1_000_000,
    'sets': {
        'Low': {
            'type': 'trapezoidal',
            'params': [0, 0, 80_000, 100_000]
        },
        'Medium': {
            'type': 'trapezoidal',
            'params': [50_000, 100_000, 200_000, 250_000]
        },
        'High': {
            'type': 'trapezoidal',
            'params': [200_000, 300_000, 650_000, 850_000]
        },
        'Very_High': {
            'type': 'trapezoidal',
            'params': [650_000, 850_000, 1_000_000, 1_000_000]
        }
    }
}

# 2. Konum (0 - 10)
location = {
    'min': 0,
    'max': 10,
    'sets': {
        'Bad': {
            'type': 'trapezoidal',
            'params': [0, 0, 2, 4]
        },
        'Fair': {
            'type': 'trapezoidal',
            'params': [2.5, 5, 6, 8.5]
        },
        'Excellent': {
            'type': 'trapezoidal',
            'params': [6, 8.5, 10, 10]
        }
    }
}

# 3. Varlık (0 - 1,000,000 USD)
asset = {
    'min': 0,
    'max': 1_000_000,
    'sets': {
        'Low': {
            'type': 'trapezoidal',
            'params': [0, 0, 0, 150_000]
        },
        'Medium': {
            'type': 'trapezoidal',
            'params': [50_000, 250_000, 450_000, 650_000]
        },
        'High': {
            'type': 'trapezoidal',
            'params': [500_000, 700_000, 1_000_000, 1_000_000]
        }
    }
}

# 4. Gelir (0 - 100,000 USD/Yıl)
income = {
    'min': 0,
    'max': 100_000,
    'sets': {
        'Low': {
            'type': 'trapezoidal',
            'params': [0, 0, 10_000, 25_000]
        },
        'Medium': {
            'type': 'triangular',
            'params': [15_000, 35_000, 55_000]
        },
        'High': {
            'type': 'triangular',
            'params': [40_000, 60_000, 80_000]
        },
        'Very_High': {
            'type': 'trapezoidal',
            'params': [60_000, 80_000, 100_000, 100_000]
        }
    }
}

# 5. Faiz (0 - 10 %)
interest = {
    'min': 0,
    'max': 10,
    'sets': {
        'Low': {
            'type': 'trapezoidal',
            'params': [0, 0, 2, 5]
        },
        'Medium': {
            'type': 'trapezoidal',
            'params': [2, 4, 6, 8]
        },
        'High': {
            'type': 'trapezoidal',
            'params': [6, 8.5, 10, 10]
        }
    }
}

# --- ARA ÇIKIŞLAR ---

# Ev (0 - 10)
house = {
    'min': 0,
    'max': 10,
    'sets': {
        'Very_Low': {
            'type': 'trapezoidal',
            'params': [0, 0, 0, 3]
        },
        'Low': {
            'type': 'triangular',
            'params': [0, 3, 6]
        },
        'Medium': {
            'type': 'triangular',
            'params': [2, 5, 8]
        },
        'High': {
            'type': 'triangular',
            'params': [4, 7, 10]
        },
        'Very_High': {
            'type': 'trapezoidal',
            'params': [7, 10, 10, 10]
        }
    }
}

# Başvuru Sahibi (0 - 10)
applicant = {
    'min': 0,
    'max': 10,
    'sets': {
        'Low': {
            'type': 'trapezoidal',
            'params': [0, 0, 2, 4]
        },
        'Medium': {
            'type': 'triangular',
            'params': [2, 5, 8]
        },
        'High': {
            'type': 'trapezoidal',
            'params': [6, 8, 10, 10]
        }
    }
}

# Kredi Miktarı

# --- NİHAİ ÇIKIŞ ---

# Kredi (0 - 500,000 USD)
credit = {
    'min': 0,
    'max': 500_000,
    'sets': {
        'Very_Low': {
            'type': 'trapezoidal',
            'params': [0, 0, 0, 125_000]
        },
        'Low': {
            'type': 'triangular',
            'params': [0, 125_000, 250_000]
        },
        'Medium': {
            'type': 'triangular',
            'params': [125_000, 250_000, 375_000]
        },
        'High': {
            'type': 'triangular',
            'params': [250_000, 375_000, 500_000]
        },
        'Very_High': {
            'type': 'trapezoidal',
            'params': [375_000, 500_000, 500_000, 500_000]
        }
    }
}

# --- RULES ---

# Stage 1 Rules - House Evaluation
stage1_rules = [
    # Rule 1: If (Market_value is Low) then (House is Low)
    {'antecedents': [("Market_value", "Low")], 'consequent': ("House", "Low")},
    # Rule 2: If (Location is Bad) then (House is Low)
    {'antecedents': [("Location", "Bad")], 'consequent': ("House", "Low")},
    # Rule 3: If (Location is Bad) and (Market_value is Low) then (House is Very_low)
    {'antecedents': [("Location", "Bad"), ("Market_value", "Low")], 'consequent': ("House", "Very_Low")},
    # Rule 4: If (Location is Bad) and (Market_value is Medium) then (House is Low)
    {'antecedents': [("Location", "Bad"), ("Market_value", "Medium")], 'consequent': ("House", "Low")},
    # Rule 5: If (Location is Bad) and (Market_value is High) then (House is Medium)
    {'antecedents': [("Location", "Bad"), ("Market_value", "High")], 'consequent': ("House", "Medium")},
    # Rule 6: If (Location is Bad) and (Market_value is Very_High) then (House is High)
    {'antecedents': [("Location", "Bad"), ("Market_value", "Very_High")], 'consequent': ("House", "High")},
    # Rule 7: If (Location is Fair) and (Market_value is Low) then (House is Low)
    {'antecedents': [("Location", "Fair"), ("Market_value", "Low")], 'consequent': ("House", "Low")},
    # Rule 8: If (Location is Fair) and (Market_value is Medium) then (House is Medium)
    {'antecedents': [("Location", "Fair"), ("Market_value", "Medium")], 'consequent': ("House", "Medium")},
    # Rule 9: If (Location is Fair) and (Market_value is High) then (House is High)
    {'antecedents': [("Location", "Fair"), ("Market_value", "High")], 'consequent': ("House", "High")},
    # Rule 10: If (Location is Fair) and (Market_value is Very_High) then (House is Very_High)
    {'antecedents': [("Location", "Fair"), ("Market_value", "Very_High")], 'consequent': ("House", "Very_High")},
    # Rule 11: If (Location is Excellent) and (Market_value is Low) then (House is Medium)
    {'antecedents': [("Location", "Excellent"), ("Market_value", "Low")], 'consequent': ("House", "Medium")},
    # Rule 12: If (Location is Excellent) and (Market_value is Medium) then (House is High)
    {'antecedents': [("Location", "Excellent"), ("Market_value", "Medium")], 'consequent': ("House", "High")},
    # Rule 13: If (Location is Excellent) and (Market_value is High) then (House is Very_High)
    {'antecedents': [("Location", "Excellent"), ("Market_value", "High")], 'consequent': ("House", "Very_High")},
    # Rule 14: If (Location is Excellent) and (Market_value is Very_High) then (House is Very_High)
    {'antecedents': [("Location", "Excellent"), ("Market_value", "Very_High")], 'consequent': ("House", "Very_High")},
]

# Stage 2 Rules - Application Evaluation
stage2_rules = [
    # Rule 1: If (Asset is Low) and (Income is Low) then (Applicant is Low)
    {'antecedents': [("Asset", "Low"), ("Income", "Low")], 'consequent': ("Applicant", "Low")},
    # Rule 2: If (Asset is Low) and (Income is Medium) then (Applicant is Low)
    {'antecedents': [("Asset", "Low"), ("Income", "Medium")], 'consequent': ("Applicant", "Low")},
    # Rule 3: If (Asset is Low) and (Income is High) then (Applicant is Medium)
    {'antecedents': [("Asset", "Low"), ("Income", "High")], 'consequent': ("Applicant", "Medium")},
    # Rule 4: If (Asset is Low) and (Income is Very_High) then (Applicant is High)
    {'antecedents': [("Asset", "Low"), ("Income", "Very_High")], 'consequent': ("Applicant", "High")},
    # Rule 5: If (Asset is Medium) and (Income is Low) then (Applicant is Low)
    {'antecedents': [("Asset", "Medium"), ("Income", "Low")], 'consequent': ("Applicant", "Low")},
    # Rule 6: If (Asset is Medium) and (Income is Medium) then (Applicant is Medium)
    {'antecedents': [("Asset", "Medium"), ("Income", "Medium")], 'consequent': ("Applicant", "Medium")},
    # Rule 7: If (Asset is Medium) and (Income is High) then (Applicant is High)
    {'antecedents': [("Asset", "Medium"), ("Income", "High")], 'consequent': ("Applicant", "High")},
    # Rule 8: If (Asset is Medium) and (Income is Very_High) then (Applicant is High)
    {'antecedents': [("Asset", "Medium"), ("Income", "Very_High")], 'consequent': ("Applicant", "High")},
    # Rule 9: If (Asset is High) and (Income is Low) then (Applicant is Medium)
    {'antecedents': [("Asset", "High"), ("Income", "Low")], 'consequent': ("Applicant", "Medium")},
    # Rule 10: If (Asset is High) and (Income is Medium) then (Applicant is Medium)
    {'antecedents': [("Asset", "High"), ("Income", "Medium")], 'consequent': ("Applicant", "Medium")},
    # Rule 11: If (Asset is High) and (Income is High) then (Applicant is High)
    {'antecedents': [("Asset", "High"), ("Income", "High")], 'consequent': ("Applicant", "High")},
    # Rule 12: If (Asset is High) and (Income is Very_High) then (Applicant is High)
    {'antecedents': [("Asset", "High"), ("Income", "Very_High")], 'consequent': ("Applicant", "High")},
]

# Stage 3 Rules - Loan Amount Evaluation
stage3_rules = [
    # Rule 1: If (Income is Low) and (Interest is Medium) then (Credit is Very_low)
    {'antecedents': [("Income", "Low"), ("Interest", "Medium")], 'consequent': ("Credit", "Very_Low")},
    # Rule 2: If (Income is Low) and (Interest is High) then (Credit is Very_low)
    {'antecedents': [("Income", "Low"), ("Interest", "High")], 'consequent': ("Credit", "Very_Low")},
    # Rule 3: If (Income is Medium) and (Interest is High) then (Credit is Low)
    {'antecedents': [("Income", "Medium"), ("Interest", "High")], 'consequent': ("Credit", "Low")},
    # Rule 4: If (Applicant is Low) then (Credit is Very_low)
    {'antecedents': [("Applicant", "Low")], 'consequent': ("Credit", "Very_Low")},
    # Rule 5: If (House is Very_low) then (Credit is Very_low)
    {'antecedents': [("House", "Very_Low")], 'consequent': ("Credit", "Very_Low")},
    # Rule 6: If (Applicant is Medium) and (House is Very_low) then (Credit is Low)
    {'antecedents': [("Applicant", "Medium"), ("House", "Very_Low")], 'consequent': ("Credit", "Low")},
    # Rule 7: If (Applicant is Medium) and (House is Low) then (Credit is Low)
    {'antecedents': [("Applicant", "Medium"), ("House", "Low")], 'consequent': ("Credit", "Low")},
    # Rule 8: If (Applicant is Medium) and (House is Medium) then (Credit is Medium)
    {'antecedents': [("Applicant", "Medium"), ("House", "Medium")], 'consequent': ("Credit", "Medium")},
    # Rule 9: If (Applicant is Medium) and (House is High) then (Credit is High)
    {'antecedents': [("Applicant", "Medium"), ("House", "High")], 'consequent': ("Credit", "High")},
    # Rule 10: If (Applicant is Medium) and (House is Very_High) then (Credit is High)
    {'antecedents': [("Applicant", "Medium"), ("House", "Very_High")], 'consequent': ("Credit", "High")},
    # Rule 11: If (Applicant is High) and (House is Very_low) then (Credit is Low)
    {'antecedents': [("Applicant", "High"), ("House", "Very_Low")], 'consequent': ("Credit", "Low")},
    # Rule 12: If (Applicant is High) and (House is Low) then (Credit is Medium)
    {'antecedents': [("Applicant", "High"), ("House", "Low")], 'consequent': ("Credit", "Medium")},
    # Rule 13: If (Applicant is High) and (House is Medium) then (Credit is High)
    {'antecedents': [("Applicant", "High"), ("House", "Medium")], 'consequent': ("Credit", "High")},
    # Rule 14: If (Applicant is High) and (House is High) then (Credit is High)
    {'antecedents': [("Applicant", "High"), ("House", "High")], 'consequent': ("Credit", "High")},
    # Rule 15: If (Applicant is High) and (House is Very_High) then (Credit is Very_High)
    {'antecedents': [("Applicant", "High"), ("House", "Very_High")], 'consequent': ("Credit", "Very_High")},
]
