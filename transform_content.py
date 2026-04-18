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
        # Añadir cache-buster para evitar versiones viejas del CDN de OneDrive/SharePoint
        url_with_cache_buster = f"{url}&t={datetime.now().timestamp()}"
        response = requests.get(url_with_cache_buster, timeout=15)
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
        # Leer todas las hojas
        sheets = pd.read_excel(source, sheet_name=None)
        
        # Procesar hoja de Noticias (anteriormente Sheet1)
        df = sheets.get('Noticias', sheets.get('Sheet1', pd.DataFrame()))
        if df.empty:
            print("Error: No se encontró la hoja de Noticias.")
            return

        # Invertir el orden (inferiores primero)
        df = df.iloc[::-1]
        
        # Mapeo de columnas requeridas
        required_cols = ['Tema', 'Sub titulo', 'Titulo', 'Spanish', 'Original', 'Foto', 'Boton', 'Resumen']
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
                "lang": detect_language(row['Original']),
                "is_resumen": str(row['Resumen']).strip() == "1"
            }
            
            # Limpieza básica de URLs
            if item['link'] == "nan": item['link'] = "#"
            if item['thumbnail'] == "nan": item['thumbnail'] = "https://picsum.photos/600/400"

            news_list.append(item)

        # Procesar Encabezado
        header_df = sheets.get('Encabezado', pd.DataFrame())
        header_data = {}
        if not header_df.empty:
            row = header_df.iloc[0]
            header_data = {
                "title": str(row.get('Titulo', '')).strip(),
                "subtitle": str(row.get('Subtitulo', '')).strip(),
                "brand_black": str(row.get('Primera Linea Negra', '')).strip(),
                "brand_blue": str(row.get('Primera Linea Azul', '')).strip()
            }
            print(f"Éxito: Leído encabezado: {header_data['title']}")
        else:
            print("Aviso: No se encontró contenido en la hoja 'Encabezado'.")

        # Procesar Pie de Página
        footer_df = sheets.get('Pie de Página', pd.DataFrame())
        footer_data = {}
        if not footer_df.empty:
            row = footer_df.iloc[0]
            footer_data = {
                "line1": str(row.get('Primera Linea', '')).strip(),
                "line2": str(row.get('Segunda Linea', '')).strip()
            }
            print(f"Éxito: Leído pie de página: {footer_data['line1'][:30]}...")
        else:
            print("Aviso: No se encontró contenido en la hoja 'Pie de Página'.")

        # Construir salida final
        final_data = {
            "header": header_data,
            "footer": footer_data,
            "news": news_list
        }

        # Guardar JSON
        os.makedirs(os.path.dirname(output_json), exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
            
        print(f"Éxito: Se procesaron {len(news_list)} noticias y configuración a {output_json}")

    except Exception as e:
        print(f"Error durante la transformación: {str(e)}")

if __name__ == "__main__":
    # Obtener la mejor fuente disponible
    data_source = get_excel_data(ONEDRIVE_URL, LOCAL_EXCEL)
    transform_excel_to_json(data_source, "data/news.json")
