import pandas as pd
import json
import os
from datetime import datetime

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
            # Special case for some .com sites that are English but have "noticias" mentions? 
            # Rare. Usually if it has "cr" or "noticias" it's Spanish.
            return "Español"
            
    for domain in english_only:
        if domain in url:
            return "English"
            
    return "English" # Default to English for international sources if no Spanish indicator

def transform_excel_to_json(excel_path, output_json):
    if not os.path.exists(excel_path):
        print(f"Error: No se encontró el archivo {excel_path}")
        return

    try:
        # Leer Excel
        df = pd.read_excel(excel_path)
        
        # Mapeo de columnas requeridas
        # Tema	Sub titulo	Titulo	Spanish	Original	Foto
        required_cols = ['Tema', 'Sub titulo', 'Titulo', 'Spanish', 'Original', 'Foto']
        for col in required_cols:
            if col not in df.columns:
                print(f"Advertencia: Falta la columna '{col}' en el Excel.")
                df[col] = "" # Crear vacía para evitar errores

        news_list = []
        today = datetime.now().strftime("%Y-%m-%d")

        for _, row in df.iterrows():
            if pd.isna(row['Titulo']) or str(row['Titulo']).strip() == "":
                continue

            item = {
                "category": str(row['Tema']).strip(),
                "title": str(row['Titulo']).strip(),
                "summary": str(row['Sub titulo']).strip(),
                "content": str(row['Spanish']).strip(),
                "link": str(row['Original']).strip(),
                "thumbnail": str(row['Foto']).strip(),
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
            
        print(f"Éxito: Se procesaron {len(news_list)} noticias desde {excel_path} a {output_json}")

    except Exception as e:
        print(f"Error durante la transformación: {str(e)}")

if __name__ == "__main__":
    transform_excel_to_json("noticias.xlsx", "data/news.json")
