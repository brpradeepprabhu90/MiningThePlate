import pandas as pd
import numpy as np
# 1. Load the Genomic Risk Dataset (MR Analysis)
df_risk = pd.read_excel('FullData.xlsx', sheet_name='Table S2')
df_risk.columns = df_risk.columns.str.strip().str.lower()

def get_genomic_risk(food_target):
    """Fetches the Odds Ratio (OR) for a specific food from the MR dataset."""
    risk_data = df_risk[(df_risk['exposure'].str.contains(food_target, case=False, na=False)) & 
                        (df_risk['method'] == 'Inverse variance weighted')]
    
    # Return the exact Odds Ratio if found, otherwise default to 1.0 (Neutral Baseline)
    if not risk_data.empty:
        return np.mean(risk_data['or'].values)
    return 1.0 

def calculate_pbrs(food_item, meal_composition, current_stims):
    """
    Calculates the Personalized Behavioral Risk Score (PBRS).
    Lower score = Higher behavioral regulation (Peace).
    Higher score = High probability of dysregulation.
    """
    print(f"--- Analyzing Meal: {food_item.title()} ---")
    
    # Tier 1: Genomic Risk (Data-Driven from Dataset)
    genomic_weight = get_genomic_risk(food_item)
    print(f"Tier 1 - Genomic Risk (Odds Ratio): {genomic_weight:.2f}")
    
    # Tier 2: Metabolic Stability
    protein = meal_composition.get('protein_grams', 0)
    sugar = meal_composition.get('sugar_grams', 0) 
    
    # Prevent division by zero (assume minimum sugar of 0.1g for the math to work)
    metabolic_stability = protein / max(sugar, 0.1) 
    print(f"Tier 2 - Metabolic Stability (Protein-to-Sugar Ratio): {metabolic_stability:.2f}")
    
    # Tier 3: Biomarker Correlation (External Stims)
    # Apply a +5.0 penalty if physical pain indicators (stims) are currently present
    pain_indicator_score = 5.0 if current_stims else 0.0
    print(f"Tier 3 - Biomarker Penalty (Stims Present): {pain_indicator_score}")
    
    # Final PBRS Calculation
    # High genomic risk is mathematically worsened by low metabolic stability (sugar crash)
    # We enforce a minimum stability of 0.1 so the score doesn't break on zero-sugar meals
    predicted_risk = (genomic_weight / max(metabolic_stability, 0.1)) + pain_indicator_score
    
    print(f"=> Final Personalized Behavioral Risk Score (PBRS): {predicted_risk:.2f}\n")
    return predicted_risk

# ==========================================
# Run Precision Forecast Scenarios
# ==========================================

# Scenario 1: A highly triggering meal 
# (Genetically sensitive food, low protein, high sugar, existing physical stims)
calculate_pbrs(
    food_item='Wholemeal pasta', 
    meal_composition={'protein_grams': 7, 'sugar_grams': 2},
    current_stims=True
)

# Scenario 2: A highly protective meal 
# (Genetically protective food, high protein, balanced sugar, no physical stims)
calculate_pbrs(
    food_item='Banana', 
    meal_composition={'protein_grams': 15, 'sugar_grams': 14},
    current_stims=False
)

# Scenario 3: A neutral food, but a poor metabolic mix
# (Food not linked to ASD, but causes a massive sugar crash)
calculate_pbrs(
    food_item='Apple', 
    meal_composition={'protein_grams': 0.1, 'sugar_grams': 0},
    current_stims=False
)

calculate_pbrs(
    food_item='Vegetable Soup', 
    meal_composition={'protein_grams': 5, 'sugar_grams': 1},
    current_stims=False
)

calculate_pbrs(
    food_item='Cheese Spread', 
    meal_composition={'protein_grams': 2, 'sugar_grams': 2},
    current_stims=True
)