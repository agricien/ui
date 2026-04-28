import pandas as pd
import requests
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')

ONEDRIVE_URL = "https://agricien-my.sharepoint.com/:x:/p/edgar_mendez/IQD8LB_nWF1PT6TJzmqjgdHnASgL66q1zJxg5xydZHwRRVA?download=1"

def inspect():
    try:
        response = requests.get(ONEDRIVE_URL)
        if response.status_code == 200:
            all_sheets = pd.read_excel(io.BytesIO(response.content), sheet_name=None)
            print(f"Total sheets: {len(all_sheets)}")
            for name in all_sheets.keys():
                df = all_sheets[name]
                print(f"Sheet: {name}")
                print(f"  Columns: {df.columns.tolist()}")
                if not df.empty:
                    print(f"  First row (keys): {df.iloc[0].keys().tolist()}")
                    if 'SubTema' in df.columns:
                        print(f"  Sample SubTema: {df['SubTema'].iloc[0]}")
                else:
                    print("  Empty sheet")
                print("-" * 20)
        else:
            print(f"Failed to download: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
