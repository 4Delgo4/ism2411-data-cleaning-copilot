import pandas as pd
import numpy as np

#loading the file
df = pd.read_csv("data/raw/sales_data_raw.csv")
load_data = df
print(df.head())
print(df.columns)
#cleaning the columns
def clean_column_names(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df


#fixing the numbers

#checking for mising number
print(df.isnull().sum())
#Co-pilot assisted line of code
"""
    Fill common missing values in-place on a copy of the DataFrame and return it.

    What it is doing:
    - Converts 'price' and 'qty' to numeric (coercing errors to NaN).
    - For 'price': fill empty with the column median (if median is NaN, fills with 0).
    - For 'qty': fill empty with 0.
    - Leaves other columns untouched.
    """
def handle_missing_values(df):
   
    if df is None:
        raise ValueError("Input DataFrame is None")

    df = df.copy()

    # Price: coerce to numeric and fill missing with median (or 0 if median is NaN)
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        median_price = df['price'].median(skipna=True)
        if np.isnan(median_price):
            median_price = 0
        df['price'] = df['price'].fillna(median_price)

    # Qty: coerce to numeric and fill missing with 0
    if 'qty' in df.columns:
        df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
        df['qty'] = df['qty'].fillna(0)
    df = df[df['price'] > 0]
    df = df[df['qty'] > 0]

    return df

#Co-pilot assisted lines of code
"""
    Remove rows that are clearly invalid and return a filtered copy.

    What it does:
    - Drop rows where 'price' is present and <= 0.
    - Drop rows where 'qty' is present and <= 0.
    - Drop rows where 'prodname' exists but is empty.
    - Keeps other rows unchanged.

    Returns a copy of the DataFrame with the invalid rows removed.
    """
def remove_invalid_rows(df):
    
    if df is None:
        raise ValueError("Input DataFrame is None")

    df = df.copy()

    # Remove non-positive prices
    if 'price' in df.columns:
        # ensure numeric type before comparison
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df[df['price'] > 0]

    # Removing prices below Zero
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df[df['price'] > 0]

    # Remove rows with blank product names (if the column exists)
    if 'prodname' in df.columns:
        # treat empty strings and whitespace-only strings as invalid
        df = df[df['prodname'].notna() & (df['prodname'].astype(str).str.strip() != '')]

    # Reset index after filtering for cleanliness
    df = df.reset_index(drop=True)
    return df

def load_data(path):
    return pd.read_csv(path)



if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())
