import requests
import pandas as pd
import io

url = "https://agricien-my.sharepoint.com/:x:/p/edgar_mendez/IQD8LB_nWF1PT6TJzmqjgdHnAbe4nSenASMXQqSJHh0pjFA?download=1"

try:
    print(f"Intentando descargar desde: {url}")
    response = requests.get(url)
    response.raise_for_status()
    
    # Intentar leer con pandas
    df = pd.read_excel(io.BytesIO(response.content))
    print("Éxito al leer el Excel de OneDrive!")
    print("Columnas encontradas:", df.columns.tolist())
    print("Primeras 2 filas:")
    print(df.head(2))
    
except Exception as e:
    print(f"Error: {e}")
