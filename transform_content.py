import pandas as pd
import json
import os
import requests
import io
from datetime import datetime

# URL de descarga directa de OneDrive/SharePoint
ONEDRIVE_URL = "https://agricien-my.sharepoint.com/:x:/p/edgar_mendez/IQD8LB_nWF1PT6TJzmqjgdHnAbe4nSenASMXQqSJHh0pjFA?download=1"
LOCAL_EXCEL = "noticias.xlsx"

def detect_language(url):
    """Simple heuristic to detect if the source is English or Spanish."""
    if not url or pd.isna(url):
        return "Español"
    
    url = str(url).lower()
    spanish_indicators = [
        '.cr', '.es', 'latam', 'mund', 'noticias', 'agroclima', 
        'español', 'spanish', 'el-pais', 'abril', 'mayo'
    ]
    
    # Common English-only domains
    english_only = ['usda.gov', 'croplife.com', 'agribusinessglobal', 'topconpositioning.com', 'github.com']
    
    for indicator in spanish_indicators:
        if indicator in url:
            return "Español"
            
    for domain in english_only:
        if domain in url:
            return "English"
            
    return "English" # Default to English for international sources if no Spanish indicator

def get_excel_data(url, local_path):
    """Intenta descargar el Excel desde OneDrive, si falla usa el local."""
    try:
        print(f"Intentando descargar Excel desde la nube...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("Éxito: Datos obtenidos desde OneDrive.")
        return io.BytesIO(response.content)
    except Exception as e:
        print(f"Aviso: No se pudo obtener el Excel desde la nube ({e}).")
        if os.path.exists(local_path):
            print(f"Usando archivo local de respaldo: {local_path}")
            return local_path
        else:
            print("Error: No existe el archivo local de respaldo.")
            return None

def transform_excel_to_json(source, output_json):
    if source is None:
        print("Error: No hay fuente de datos disponible.")
        return

    try:
        # Leer Excel
        df = pd.read_excel(source)
        
        # Mapeo de columnas requeridas
        required_cols = ['Tema', 'Sub titulo', 'Titulo', 'Spanish', 'Original', 'Foto', 'Boton']
        for col in required_cols:
            if col not in df.columns:
                print(f"Advertencia: Falta la columna '{col}' en el Excel.")
                df[col] = "" 

        news_list = []
        today = datetime.now().strftime("%Y-%m-%d")

        for _, row in df.iterrows():
            if pd.isna(row['Titulo']) or str(row['Titulo']).strip() == "":
                continue

            # Determinar texto del botón (Prioridad: Columna G "Boton")
            btn_text = str(row['Boton']).strip()
            if btn_text == "" or btn_text == "nan":
                lang = detect_language(row['Original'])
                btn_text = f"Ver Original [{lang}]"

            item = {
                "category": str(row['Tema']).strip(),
                "title": str(row['Titulo']).strip(),
                "summary": str(row['Sub titulo']).strip(),
                "content": str(row['Spanish']).strip(),
                "link": str(row['Original']).strip(),
                "thumbnail": str(row['Foto']).strip(),
                "button_text": btn_text,
                "published": today,
                "lang": detect_language(row['Original'])
            }
            
            # Limpieza básica de URLs
            if item['link'] == "nan": item['link'] = "#"
            if item['thumbnail'] == "nan": item['thumbnail'] = "https://picsum.photos/600/400"

            news_list.append(item)

        # Guardar JSON
        os.makedirs(os.path.dirname(output_json), exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
            
        print(f"Éxito: Se procesaron {len(news_list)} noticias a {output_json}")

    except Exception as e:
        print(f"Error durante la transformación: {str(e)}")

if __name__ == "__main__":
    # Obtener la mejor fuente disponible
    data_source = get_excel_data(ONEDRIVE_URL, LOCAL_EXCEL)
    transform_excel_to_json(data_source, "data/news.json")
