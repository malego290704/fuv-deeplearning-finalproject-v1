import pandas as pd
import numpy as np
from datetime import datetime

# 1. Load the data
# Assuming your file is named 'stock_data.csv'
df = pd.read_csv('./v1-data/AAPL-NASDAQ.csv')

# --- LOG RETURNS ---
# Formula: ln(Price_t / Price_t-1)
cols_to_log = ['low', 'high', 'open', 'close', 'volume']
for col in cols_to_log:
    # We use np.log(df[col] / df[col].shift(1))
    df[col] = np.log(df[col] / df[col].shift(1))

# Since the first row will now be NaN (no previous day), we drop it
df = df.dropna().reset_index(drop=True)


# --- YEAR NORMALIZATION ---
# Range 0...1 where 0=1970 and 1=2030
year_min = 1970
year_max = 2030
df['year'] = (df['year'] - year_min) / (year_max - year_min)


# --- DAYS NORMALIZATION ---
# Range 0...1 where 0=0 and 1=Total days from 1970-01-01 to 2030-12-31
epoch_start = datetime(1970, 1, 1)
epoch_end = datetime(2030, 12, 31)
total_days_limit = (epoch_end - epoch_start).days

df['days'] = df['days'] / total_days_limit


# --- CYCLICAL ENCODING ---
def encode_cyclical(data, col, max_val):
    data[col + '_sin'] = np.sin(2 * np.pi * data[col] / max_val)
    data[col + '_cos'] = np.cos(2 * np.pi * data[col] / max_val)
    return data

# Month: 1-12
df = encode_cyclical(df, 'month', 12)
# Day: 1-31
df = encode_cyclical(df, 'day', 31)
# Weekday: 0-6 (or 1-7 depending on your source, your data shows Friday=5)
df = encode_cyclical(df, 'weekday', 7)

# Remove the original columns that were cyclically encoded
df = df.drop(columns=['month', 'day', 'weekday'])


# --- SAVE OUTPUT ---
df.to_csv('./v1-data-ready/AAPL-NASDAQ.csv', index=False)

print("Processing complete. Saved as 'processed_stock_data.csv'")
print(df.head())