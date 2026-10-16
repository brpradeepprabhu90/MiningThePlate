import matplotlib;
matplotlib.use('TkAgg') 
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

df_s5 = pd.read_excel('FullData.xlsx', sheet_name='Table S5')
df_s6 = pd.read_excel('FullData.xlsx', sheet_name='Table S6')
df_s7 = pd.read_excel('FullData.xlsx', sheet_name='Table S7')

for df in [df_s5, df_s6, df_s7]:
    df.columns = df.columns.str.strip().str.lower()

columns_to_keep= ['nsnp', 'b', 'se', 'or', 'pval','method']

df_combined = pd.concat([df_s5[columns_to_keep], df_s6[columns_to_keep], df_s7[columns_to_keep]], ignore_index=True)

df_ivw = df_combined[df_combined['method'] == 'Inverse variance weighted'].copy()
df_ivw['is_significant'] = (df_ivw['pval'] < 0.05).astype(int)
print("Combined IVW Results:")
print(df_ivw.head())

features = ['nsnp', 'b', 'se', 'or']
df_model = df_ivw.dropna(subset=features + ['is_significant'])
x = df_model[features]
y = df_model['is_significant']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
print("\nPredictive Model Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

print(f"Prepared combined data for modeling. Total rows: {len(df_model)}")

feature_importances = pd.Series(clf.feature_importances_, index=features)
feature_importances.sort_values(ascending=True).plot(kind='barh', title='Feature Importance')
plt.xlabel('Importance Score')
plt.show()