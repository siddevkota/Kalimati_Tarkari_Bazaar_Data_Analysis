import pandas as pd
import numpy as np

# Define correct headers excluding 'SN' for the CSV without headers
correct_headers = ['Commodity', 'Date', 'Unit', 'Minimum', 'Maximum', 'Average']

# Load the CSV with correct headers including 'SN'
file_with_headers_path = 'data/kalimati-tarkari-prices-from-may-2021-to-september-2023.csv'
data_with_headers = pd.read_csv(file_with_headers_path)

# Remove the 'SN' column
data_with_headers = data_with_headers.drop(columns=['SN'])

# Load the CSV without headers and apply correct headers manually
file_without_headers_path = 'data/kalimati_tarkari_dataset_cleaned.csv'
data_without_headers = pd.read_csv(file_without_headers_path, header=None, names=correct_headers)

# Merge the datasets and remove duplicates based on 'Date' and other columns
merged_data = pd.concat([data_with_headers, data_without_headers]).drop_duplicates()

# Convert 'Date' to datetime format
merged_data['Date'] = pd.to_datetime(merged_data['Date'])

# Remove 'Rs' from prices and convert them to numeric values
price_columns = ['Minimum', 'Maximum', 'Average']
for col in price_columns:
    merged_data[col] = merged_data[col].replace('[\$,Rs]', '', regex=True).astype(float)

# Standardize 'Unit' values
unit_mappings = {
    'Kg': 'Kg',
    'KG': 'Kg',
    '1 Pc': 'Per piece',
    'Per dozen': 'Per dozen',
    'Each': 'Per piece'
}

merged_data['Unit'] = merged_data['Unit'].replace(unit_mappings)

# Handle missing values (if any)
merged_data = merged_data.dropna()  # Simple approach: drop missing values

# Save the cleaned dataframe
cleaned_file_path = 'data/cleaned_kalimati_tarkari_prices.csv'
merged_data.to_csv(cleaned_file_path, index=False)