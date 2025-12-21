import matplotlib.pyplot as plt
import numpy as np
from variables import (
    market_value, location, asset, income, interest,
    house, applicant, credit
)
from fuzzy_system.core import calculate_membership

def plot_membership_functions():
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
    
    for var_name, var_data in variables.items():
        # Create a new figure for each variable
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Generate x values
        x = np.linspace(var_data['min'], var_data['max'], 500)
        
        for set_name, set_data in var_data['sets'].items():
            # Calculate membership for each x
            y = [calculate_membership(val, set_data['type'], set_data['params']) for val in x]
            ax.plot(x, y, label=set_name, linewidth=2)
            
            # Fill under the curve for better visualization
            ax.fill_between(x, y, alpha=0.1)
            
        ax.set_title(f'Membership Functions: {var_name}')
        ax.set_xlabel('Value')
        ax.set_ylabel('Membership Degree')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        
        plt.tight_layout()
        output_file = f"membership_{var_name.lower()}.png"
        plt.savefig(output_file)
        plt.close(fig)  # Close the figure to free memory
        print(f"Graph saved to {output_file}")
    
    print(f"\nAll {len(variables)} membership function graphs have been saved.")

if __name__ == "__main__":
    plot_membership_functions()
