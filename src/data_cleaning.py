import pandas as pd
import numpy as np

#loading the file
df = pd.read_csv("sales_data_raw.csv")
print(df.head())
print(df.columns)
#cleaning the columns
df.columns - df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
#removing spaces in the text
df['prodname'] = df['prodname'].str.strip()
df['category'] = df['category'].str.strip()
df['category'] = df['category'].str.replace('""', '')

#fixing the numbers
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
#checking for mising numbers
print(df.isnull().sum())

#filling missing data twith the median
median_price = df['price'].median()
df['price'] = df['price'].fillna(median_price)

df['qty'] = df['qty'].fillna(0)
#dropping rows
df = df[df['price'] > 0]
df = df[df['qty'] > 0]
#saving it
df.to_csv("sales_dat_clean.csv", index=False)
print("FInished cleaning data")


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
