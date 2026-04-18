import os
import requests
import io
import pandas as pd

# Simular fallo de URL
ONEDRIVE_URL = "https://broken-url.com/noticias.xlsx"
LOCAL_EXCEL = "noticias.xlsx"

def get_excel_data(url, local_path):
    try:
        print(f"Intentando descargar desde: {url}")
        response = requests.get(url, timeout=2) # Timeout corto
        response.raise_for_status()
        return io.BytesIO(response.content)
    except Exception as e:
        print(f"Aviso: Falló la nube ({e}).")
        if os.path.exists(local_path):
            print(f"Usando local: {local_path}")
            return local_path
        return None

source = get_excel_data(ONEDRIVE_URL, LOCAL_EXCEL)
if source == LOCAL_EXCEL:
    print("TEST FALLBACK: EXITOSO")
else:
    print("TEST FALLBACK: FALLIDO")
