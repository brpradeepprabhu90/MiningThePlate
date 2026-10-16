import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Load the Risk Dataset
df_risk = pd.read_excel('FullData.xlsx', sheet_name='Table S2')
df_risk.columns = df_risk.columns.str.strip().str.lower()

def get_multiple_forecasts(food_list):
    results = []
    
    for food in food_list:
        # Find the food in the dataset using the standard MR method
        risk_data = df_risk[(df_risk['exposure'].str.contains(food, case=False, na=False)) & 
                            (df_risk['method'] == 'Inverse variance weighted')]
        print(f"Processing {food} - Found {len(risk_data)} matching records.")
        # If the food exists, grab its Odds Ratio; otherwise default to 1.0 (No effect)
        if not risk_data.empty:
            or_val = np.mean(risk_data['or'].values)
            pval = np.mean(risk_data['pval'].values)
        else:
            or_val = 1.0
            pval = 1.0
            
        results.append({
            'Food': food.title(),
            'Odds_Ratio': or_val,
            'Is_Significant': pval < 0.05
        })
        
    return pd.DataFrame(results)

# 2. Define the list of foods you want to compare
foods_to_test = ['Cheese spread', 'Wholemeal pasta', 'Banana', 'Apple', 'Chocolate', 'Broccoli','Fish','Vegetarian','Milk','Eggs', 'Onion','Mango']  # Add more foods as needed

# 3. Get the combined data
df_comparison = get_multiple_forecasts(foods_to_test)

# 4. Plot the Comparative Bar Graph
plt.figure(figsize=(10, 6))

# Color coding: Red for high risk (OR > 1), Green for protective (OR < 1), Gray for neutral
colors = ['red' if row['Odds_Ratio'] > 1.1 else 'green' if row['Odds_Ratio'] < 0.9 else 'gray' 
          for index, row in df_comparison.iterrows()]

bars = plt.bar(df_comparison['Food'], df_comparison['Odds_Ratio'], color=colors, edgecolor='black')

# Add a baseline indicating "No Effect" (Odds Ratio = 1)
plt.axhline(y=1, color='black', linestyle='--', linewidth=2, label='Baseline (No Effect, OR=1)')

# Add formatting and labels
plt.title('Precision Neuro-Nutritional Forecast: Food Comparison', fontsize=14, fontweight='bold')
plt.ylabel('Overall Behavioral Odds Ratio\n(Higher = More Risk)', fontsize=12)
plt.xlabel('Food Group', fontsize=12)
plt.xticks(rotation=45, ha='right')

# Add value labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f'{yval:.1f}', 
             ha='center', va='bottom', fontweight='bold')

plt.legend()
plt.tight_layout()

# Save and show the plot
plt.savefig('combined_food_forecast.png')
plt.show()