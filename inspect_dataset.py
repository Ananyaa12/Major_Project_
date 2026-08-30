import pandas as pd
from pathlib import Path

p = Path('diabetes_012_health_indicators_BRFSS2015.csv')
df = pd.read_csv(p)
print(df.head())
print('\nShape:', df.shape)
print('\nColumns:', list(df.columns))
print('\nDtypes:\n', df.dtypes)
print('\nTarget distribution:\n', df['Diabetes_012'].value_counts().to_string())
print('\nMissing values:\n', df.isna().sum().sum())
