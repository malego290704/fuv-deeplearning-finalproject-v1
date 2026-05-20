import pandas as pd
import requests
import json

# --- CONFIGURATION ---
CSV_FILE = "./v1-data-normalized/AAPL-NASDAQ.csv"
API_URL = "https://dlmdminh.cung.io.vn/predict"
# List the columns that need to be divided by 1,000
COLUMNS_TO_SCALE = ['volume', 'year', 'days', 'month_sin', 'month_cos', 'day_sin', 'day_cos', 'weekday_sin', 'weekday_cos']


def test_api_with_30_rows():
    try:
        try:
            health = requests.get("https://dlmdminh.cung.io.vn/predict", timeout=5)
            print(f"Health check: {health.json()}")
        except:
            print("Server is not responding to health check. Is main.py running?")
            return
        # 1. Read first 30 lines
        df = pd.read_csv(CSV_FILE, nrows=30)
        
        # 2. Divide specified columns by 1000
        for col in COLUMNS_TO_SCALE:
            if col in df.columns:
                df[col] = df[col] / 1000.0

        # 3. Convert the entire 30-row table into a nested list
        # Resulting shape: [[row1_cols], [row2_cols], ... [row30_cols]]
        matrix = df.values.tolist()

        # 4. Prepare the payload
        # The API expects {"data": [[...], [...]]}
        payload = {"data": matrix}

        print(f"Sending table of shape ({len(matrix)} rows, {len(matrix[0])} columns)...")

        # 5. Send to API
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            print("Successfully received prediction:")
            print(response.json())
        else:
            print(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_api_with_30_rows()