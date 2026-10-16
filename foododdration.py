import pandas as pd

# 1. Load the "Rules Engine" Databases
# Table S2: Overall Food to ASD Risk
df_risk = pd.read_excel('FullData.xlsx', sheet_name='Table S2')
# Table S8: Immune and Metabolite Mediators
df_immune = pd.read_excel('FullData.xlsx', sheet_name='Table S8')
# Table S7: Food to Gut Microbiome impacts
df_microbiome = pd.read_excel('FullData.xlsx', sheet_name='Table S7')

# Standardize columns for easy querying
for df in [df_risk, df_immune, df_microbiome]:
    df.columns = df.columns.str.strip().str.lower()

def generate_precision_forecast(food_target):
    print(f"=== PRECISION NEURO-NUTRITIONAL FORECAST: {food_target.upper()} ===")
    
    # 1. Genomic Sensitivity Scoring (ASD Risk)
    risk_data = df_risk[(df_risk['exposure'].str.contains(food_target, case=False, na=False)) & 
                        (df_risk['method'] == 'Inverse variance weighted')]
    
    if not risk_data.empty:
        or_val = risk_data['or'].values[0]
        pval = risk_data['pval'].values[0]
        if or_val > 1 and pval < 0.05:
            print(f"⚠️ HIGH RISK PREDICTOR: Odds Ratio {or_val:.2f} for behavioral flare-ups (p={pval:.4f}).")
        elif or_val < 1 and pval < 0.05:
            print(f"✅ PROTECTIVE PREDICTOR: Odds Ratio {or_val:.2f} (Reduces behavioral risk).")
        else:
            print(f"ℹ️ NEUTRAL/INCONCLUSIVE: No significant population-level risk detected.")
    
    # 2. Immune & Metabolite Mediators (Biological Cues)
    immune_data = df_immune[df_immune['exposure'].str.contains(food_target, case=False, na=False)]
    if not immune_data.empty:
        print("\n🧬 IMMUNE / METABOLIC PATHWAYS ACTIVATED:")
        for _, row in immune_data.iterrows():
            print(f"  - Alters: {row['metabolite']}")
            print(f"  - Mediates ASD effect by: {row['mediated proportion']}")
            
    # 3. GI Distress / Microbiome Shifts
    micro_data = df_microbiome[(df_microbiome['exposure'].str.contains(food_target, case=False, na=False)) & 
                               (df_microbiome['pval'] < 0.05)]
    if not micro_data.empty:
        print("\n🦠 MICROBIOME DISRUPTION PREDICTIONS (Leaky Gut Indicators):")
        # Show top 3 most significant bacterial shifts
        top_shifts = micro_data.sort_values('pval').head(3)
        for _, row in top_shifts.iterrows():
            direction = "Decreases" if row['b'] < 0 else "Increases"
            print(f"  - {direction} {row['outcome']} (Effect Size: {row['b']:.2f})")

    print("==================================================================\n")

# --- Test the Algorithm ---
# Simulate the app predicting outcomes for specific meals:
generate_precision_forecast('Wholemeal pasta')
generate_precision_forecast('Cheese spread')
generate_precision_forecast('Banana')