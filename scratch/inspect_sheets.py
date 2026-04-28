import pandas as pd
import requests
import io
import sys

# Set encoding for stdout to handle emojis
sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1sgtvDNvVID6hQKaoIR-I7BuxsGr3NO1db0qOGdM3iaE'
SPREADSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx"

def inspect():
    try:
        response = requests.get(SPREADSHEET_URL)
        if response.status_code == 200:
            all_sheets = pd.read_excel(io.BytesIO(response.content), sheet_name=None)
            print(f"Total sheets: {len(all_sheets)}")
            for name in all_sheets.keys():
                df = all_sheets[name]
                print(f"Sheet: {name}")
                print(f"  Columns: {df.columns.tolist()}")
                if not df.empty:
                    print(f"  First row (keys): {df.iloc[0].keys().tolist()}")
                else:
                    print("  Empty sheet")
                print("-" * 20)
        else:
            print(f"Failed to download: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
