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
    
    # Determine layout
    num_vars = len(variables)
    cols = 2
    rows = (num_vars + 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows))
    axes = axes.flatten()
    
    for i, (var_name, var_data) in enumerate(variables.items()):
        ax = axes[i]
        
        # Generate x values
        # Use numpy for smoother plotting
        x = np.linspace(var_data['min'], var_data['max'], 500)
        
        for set_name, set_data in var_data['sets'].items():
            # Calculate membership for each x
            y = [calculate_membership(val, set_data['type'], set_data['params']) for val in x]
            ax.plot(x, y, label=set_name, linewidth=2)
            
            # Fill under the curve for better visualization
            ax.fill_between(x, y, alpha=0.1)
            
        ax.set_title(f'Variable: {var_name}')
        ax.set_xlabel('Value')
        ax.set_ylabel('Membership Degree')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        
    # Hide empty subplots if any
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
        
    plt.tight_layout()
    output_file = "membership_functions.png"
    plt.savefig(output_file)
    print(f"Graph saved to {output_file}")
    # plt.show() # Commented out for headless environment

if __name__ == "__main__":
    plot_membership_functions()
