import pandas as pd
import json

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1sgtvDNvVID6hQKaoIR-I7BuxsGr3NO1db0qOGdM3iaE/export?format=xlsx"
all_sheets_dict = pd.read_excel(SPREADSHEET_URL, sheet_name=None)
out = {}
for name, df in all_sheets_dict.items():
    out[name] = {
        "columns": df.columns.tolist(),
        "n_rows": len(df)
    }

with open("debug_out.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
