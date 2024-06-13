import pandas as pd
import numpy as np

correct_headers = ["Commodity", "Date", "Unit", "Minimum", "Maximum", "Average"]

file_with_headers_path = "data/cleaned_kalimati_prices.csv"
data_with_headers = pd.read_csv(file_with_headers_path)

data_with_headers = data_with_headers.drop(columns=["SN"])

file_without_headers_path = (
    "data/kalimati-tarkari-prices-from-sep-2023-to-june-2024.csv"
)
data_without_headers = pd.read_csv(
    file_without_headers_path, header=None, names=correct_headers
)

data_without_headers = pd.read_csv(file_without_headers_path)

merged_data = pd.concat([data_with_headers, data_without_headers]).drop_duplicates()

merged_data["Date"] = pd.to_datetime(
    merged_data["Date"], errors="coerce", infer_datetime_format=True
)
merged_data = merged_data.dropna(subset=["Date"])

price_columns = ["Minimum", "Maximum", "Average"]
for col in price_columns:
    merged_data[col] = merged_data[col].replace("[\$,Rs]", "", regex=True).astype(float)

unit_mappings = {
    "Kg": "Kg",
    "KG": "Kg",
    "1 Pc": "Per piece",
    "Per Dozen": "Per dozen",
    "Each": "Per piece",
}

merged_data["Unit"] = merged_data["Unit"].replace(unit_mappings)


merged_data = merged_data.dropna()

cleaned_file_path = "data/new_cleaned_kalimati_prices.csv"
merged_data.to_csv(cleaned_file_path, index=False)

print(f"Cleaned file saved to: {cleaned_file_path}")
