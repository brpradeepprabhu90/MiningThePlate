import matplotlib;
matplotlib.use('TkAgg')  # Use a non-interactive backend for environments without display
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


df_exposures = pd.read_excel('FullData.xlsx',sheet_name='Table S1')
df_results = pd.read_excel('FullData.xlsx',sheet_name='Table S6')

#Merge the two dataframes on the 'exposure' column
df_merged = pd.merge(df_exposures, df_results, on='exposureID', how='inner')
df_ivw = df_merged[df_merged['method'] == 'Inverse variance weighted']
top_correlations =df_ivw.sort_values(by='pval', ascending=True)[['exposureID', 'outcome', 'or', 'pval']]
print("Top Food-Behavior Correlations:")
print(top_correlations.head())
df_ivw['is_significant'] = (df_ivw['pval'] < 0.05).astype(int)
print("Summary of IVW Results:")
print(df_ivw)
features = ['nsnp', 'b', 'se', 'or']
missing_cols = [col for col in features + ['is_significant'] if col not in df_ivw.columns]

if missing_cols:
    print(f"CRITICAL ERROR: The following columns are missing from the dataframe: {missing_cols}")
    print(f"Available columns are: {df_ivw.columns.tolist()}")
else:
    # 4. Safely drop NAs if all columns exist
    df_model = df_ivw.dropna(subset=features + ['is_significant'])
    
    X = df_model[features]
    y = df_model['is_significant']
    print(f"Successfully prepared data. Model has {len(df_model)} rows.")
df_model = df_ivw.dropna(subset=features + ['is_significant'])
X = df_model[features]
y = df_model['is_significant']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
print("\nPredictive Model Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

feature_importances = pd.Series(clf.feature_importances_, index=features)
feature_importances.sort_values(ascending=False).plot(kind='bar', title='Feature Importance in Predicting Significance')
plt.ylabel('Importance Score')
plt.show()