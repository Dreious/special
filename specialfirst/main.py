
from credit_system import calculate_credit

def format_number_text(value):
    if value >= 1_000_000:
        return f"{value/1_000_000:.0f} Milyon" if value % 1_000_000 == 0 else f"{value/1_000_000:.1f} Milyon"
    elif value >= 1_000:
        return f"{value/1_000:.0f} Bin" if value % 1_000 == 0 else f"{value/1_000:.1f} Bin"
    return str(value)

def format_input_display(key, value):
    if key in ["Market_value", "Asset", "Income"]:
        return f"${value:,.0f} ({format_number_text(value)} Dolar)"
    elif key == "Credit_Amount": # For usage in results if needed
        return f"${value:,.2f} ({format_number_text(value)} Dolar)"
    elif key == "Interest":
        return f"% {value}"
    elif key in ["Location", "House_Score", "Applicant_Score"]:
        return f"{value} / 10"
    return str(value)

def run_scenarios():
    # system = CreditEvaluationSystem() # Removed OOP instantiation

    scenarios = [
        {
            "name": "Senaryo 1: Düşük Profil (Öğrenci/Giriş Seviyesi)",
            "inputs": {
                "Market_value": 150000,
                "Location": 3, # Orta/Kötü
                "Asset": 20000,
                "Income": 25000,
                "Interest": 15 # Yüksek
            }
        },
        {
            "name": "Senaryo 2: Orta Profil (Ortalama Aile)",
            "inputs": {
                "Market_value": 400000,
                "Location": 5, # Orta
                "Asset": 150000,
                "Income": 70000,
                "Interest": 10 # Orta
            }
        },
        {
            "name": "Senaryo 3: Yüksek Profil (Zengin Profesyonel)",
            "inputs": {
                "Market_value": 850000,
                "Location": 9, # Mükemmel
                "Asset": 800000,
                "Income": 180000,
                "Interest": 5 # Düşük
            }
        },
        {
            "name": "Senaryo 4: Yüksek Varlık ama Düşük Gelir (Emekli)",
            "inputs": {
                "Market_value": 600000,
                "Location": 8, # Mükemmel
                "Asset": 900000,
                "Income": 30000, # Düşük
                "Interest": 8 # Düşük/Orta
            }
        },
        {
            "name": "Senaryo 5: Yüksek Gelir ama Düşük Varlık (Genç Profesyonel)",
            "inputs": {
                "Market_value": 300000,
                "Location": 6, # Orta/İyi
                "Asset": 30000, # Düşük
                "Income": 150000, # Yüksek
                "Interest": 12 # Orta
            }
        }
    ]

    print(f"{'='*80}")
    print(f"{'BULANIK MANTIK KREDİ DEĞERLENDİRME SİSTEMİ - TEST SONUÇLARI':^80}")
    print(f"{'='*80}\n")

    for sc in scenarios:
        print(f"--- {sc['name']} ---")
        print("Girişler:")
        for k, v in sc['inputs'].items():
            formatted_val = format_input_display(k, v)
            print(f"  {k:12}: {formatted_val}")
        
        try:
            results = calculate_credit(sc['inputs'])
            
            print("\nSonuçlar:")
            print(f"  Ev Puanı         : {results['House_Score']:.2f} / 10")
            print(f"  Başvuru Puanı    : {results['Applicant_Score']:.2f} / 10")
            
            # Format Credit Amount using the helper
            credit_val = results['Credit_Amount']
            # We use the raw value for the helper, so no :,.2f inside the call
            # But the helper does .0f or .1f. For detailed credit amount, user usually likes cents.
            # Let's keep the user request style: "600 Bin Dolar"
            # But specific amount might be 459,784.33
            # Let's do: $459,784.33 (460 Bin Dolar)
            
            credit_text = format_number_text(credit_val)
            print(f"  KREDİ MİKTARI    : ${credit_val:,.2f} ({credit_text} Dolar)")

        except Exception as e:
            print(f"\nHata: {e}")
        
        print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    run_scenarios()
