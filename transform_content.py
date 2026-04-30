import pandas as pd
import json
import os
import requests
import io
import urllib.parse
from datetime import datetime

# URL de descarga directa de OneDrive/SharePoint
ONEDRIVE_URL = "https://agricien-my.sharepoint.com/:x:/p/edgar_mendez/IQD8LB_nWF1PT6TJzmqjgdHnASgL66q1zJxg5xydZHwRRVA?download=1"
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
        # Leer todas las hojas (sheet_name=None devuelve un OrderedDict con el orden del Excel)
        sheets = pd.read_excel(source, sheet_name=None)
        
        # Hojas de sistema que no son temas
        system_sheets = ['Encabezado', 'Pie de Página', 'Imagen Empresa', 'Banner', 'Hoja1', 'Logos']
        
        # Mapeo de columnas requeridas para temas
        required_cols = ['SubTema', 'Sub titulo', 'Titulo', 'Spanish', 'Original', 'Foto', 'Boton', 'Resumen']
        
        news_list = []
        today = datetime.now().strftime("%Y-%m-%d")

        # Procesar Logos
        logos_data = {}
        logos_df = sheets.get('Logos', pd.DataFrame())
        if not logos_df.empty:
            logos_df = logos_df.fillna("")
            for _, row in logos_df.iterrows():
                t = str(row.get('Tema', '')).strip()
                s = str(row.get('SubTema', '')).strip()
                l = str(row.get('Logo', '')).strip()
                if t and s and l:
                    if t not in logos_data: logos_data[t] = {}
                    logos_data[t][s] = l
            print(f"Éxito: Leídos {len(logos_df)} registros de Logos.")

        # Procesar Banner
        banner_data = []
        banner_df = sheets.get('Banner', pd.DataFrame())
        if not banner_df.empty:
            banner_df = banner_df.fillna("")
            for _, row in banner_df.iterrows():
                if pd.isna(row.get('Titulo')) or str(row.get('Titulo')).strip() == "":
                    continue
                # Procesar URL de Foto (image) en el Banner
                banner_photo = str(row.get('Foto', '')).strip()
                if banner_photo == "" or banner_photo == "nan":
                    banner_img_url = "https://picsum.photos/1200/600"
                elif banner_photo.startswith("http"):
                    banner_img_url = banner_photo
                else:
                    banner_img_url = "https://agricien.github.io/imagenes/" + urllib.parse.quote(banner_photo)

                banner_data.append({
                    "title": str(row.get('Titulo', '')).strip(),
                    "subtitle": str(row.get('Sub titulo', '')).strip(),
                    "image": banner_img_url,
                    "link": str(row.get('Original', '')).strip(),
                    "button_text": str(row.get('Boton', 'Saber Más')).strip()
                })
            print(f"Éxito: Leídos {len(banner_data)} elementos para el Banner.")

        # Procesar Temas en el ORDEN de las hojas
        theme_sheets = [s for s in sheets.keys() if s not in system_sheets]
        
        # Si existe 'Noticias' (legacy)
        if 'Noticias' in sheets and 'Noticias' not in theme_sheets:
            theme_sheets.append('Noticias')

        # Guardar el orden de las categorías para la UI
        categories_order = theme_sheets.copy()

        for sheet_name in theme_sheets:
            df = sheets[sheet_name]
            if df.empty: continue
            
            # Normalizar columnas
            cols = [str(c).strip() for c in df.columns]
            
            if 'SubTema' not in cols and 'Tema' in cols:
                df = df.rename(columns={'Tema': 'SubTema'})
            
            for col in required_cols:
                if col not in df.columns:
                    df[col] = ""

            for _, row in df.iterrows():
                if pd.isna(row['Titulo']) or str(row['Titulo']).strip() == "":
                    continue

                btn_text = str(row['Boton']).strip()
                if btn_text == "" or btn_text == "nan":
                    lang = detect_language(row['Original'])
                    btn_text = f"Ver Original [{lang}]"

                # Procesar URL de Foto (thumbnail)
                photo_val = str(row['Foto']).strip()
                if photo_val == "" or photo_val == "nan":
                    photo_url = "https://picsum.photos/600/400"
                elif photo_val.startswith("http"):
                    photo_url = photo_val
                else:
                    # Es solo un nombre de archivo, construir URL de GitHub imagenes
                    base_url = "https://agricien.github.io/imagenes/"
                    # Codificar el nombre del archivo (ej: espacios -> %20)
                    photo_url = base_url + urllib.parse.quote(photo_val)

                item = {
                    "category": sheet_name,
                    "sub_category": str(row['SubTema']).strip(),
                    "title": str(row['Titulo']).strip(),
                    "summary": str(row['Sub titulo']).strip(),
                    "content": str(row['Spanish']).strip(),
                    "link": str(row['Original']).strip(),
                    "thumbnail": photo_url,
                    "button_text": btn_text,
                    "published": today,
                    "lang": detect_language(row['Original']),
                    "is_resumen": str(row['Resumen']).strip() == "1"
                }
                
                if item['link'] == "nan": item['link'] = "#"

                news_list.append(item)
            print(f"Éxito: Procesada hoja de tema: {sheet_name} ({len(df)} filas)")

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
        
        # Procesar Pie de Página
        footer_df = sheets.get('Pie de Página', pd.DataFrame())
        footer_data = {}
        if not footer_df.empty:
            row = footer_df.iloc[0]
            footer_data = {
                "line1": str(row.get('Primera Linea', '')).strip(),
                "line2": str(row.get('Segunda Linea', '')).strip()
            }

        # Procesar Imagen Empresa
        company_df = sheets.get('Imagen Empresa', pd.DataFrame())
        company_data = {"logo": "", "main_theme": "Resumen"}
        if not company_df.empty:
            row = company_df.iloc[0]
            company_data = {
                "logo": str(row.get('Logo', '')).strip(),
                "main_theme": str(row.get('Tema Principal', 'Resumen')).strip()
            }

        # Construir salida final
        final_data = {
            "header": header_data,
            "footer": footer_data,
            "company": company_data,
            "banner": banner_data,
            "categories_order": categories_order,
            "subtheme_logos": logos_data,
            "news": news_list
        }

        # Guardar JSON
        os.makedirs(os.path.dirname(output_json), exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
            
        print(f"Éxito: Se procesaron {len(news_list)} items, {len(categories_order)} categorías y {len(banner_data)} banners.")

    except Exception as e:
        print(f"Error durante la transformación: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Obtener la mejor fuente disponible
    data_source = get_excel_data(ONEDRIVE_URL, LOCAL_EXCEL)
    transform_excel_to_json(data_source, "data/news.json")

