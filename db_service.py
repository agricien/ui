import pandas as pd
import requests

SPREADSHEET_ID = '1sgtvDNvVID6hQKaoIR-I7BuxsGr3NO1db0qOGdM3iaE'
SPREADSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx"

# Diccionario mágico para realizar los POSTs engañando a Google Forms
FORMS_MAPPING = {
    "ConfiguracionGlobal": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLScVGvNVW6N5iyYkdYTVXOOFcoNxv9YgPB7iHroQVI0QrXNZfQ/formResponse",
        "fields": {
            "cookie_banner_text": "entry.1583085490",
            "logo_url": "entry.55404181",
            "search_icon_enabled": "entry.99213234",
            "language_selector_enabled": "entry.1944161046",
            "footer_copyright_text": "entry.817734733"
        }
    },
    "MenuNavegacion": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSfL4N01Zap68XCWY5UCTX5pJQC-_zvLLDHRHXUG6hhnLaJjqA/formResponse",
        "fields": {
            "parent_id_o_categoria": "entry.1459778462",
            "titulo": "entry.843755784",
            "url_destino": "entry.617062620",
            "orden_visualizacion": "entry.1320337338"
        }
    },
    "SeccionHero": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSfR_04cCr3FU3sOEnE4X9gvY--j4P44H1nNYA0AqSTucSCqyg/formResponse",
        "fields": {
            "etiqueta_superior": "entry.1330578786",
            "titulo_principal": "entry.2051008219",
            "texto_descripcion": "entry.1046791246",
            "boton_primario_texto": "entry.1831435285",
            "boton_primario_link": "entry.1808228904",
            "imagen_url": "entry.2147150245"
        }
    },
    "Beneficios": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSd7JALb1_StDHhP8b2w9pjVhxQGzQF1kjY8MODAdHND4ujttA/formResponse",
        "fields": {
            "titulo_seccion_global": "entry.737906140",
            "titulo_beneficio_individual": "entry.1980424419",
            "descripcion_beneficio": "entry.1558789970",
            "imagen_url": "entry.14609263",
            "orden_aparicion": "entry.622716332"
        }
    },
    "ProductosEquipos": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSe5WeyVr8ntWjlPtIskSqueMVOihAOOCktiJRzn1I0xFi1c4A/formResponse",
        "fields": {
            "modelo_nombre": "entry.266770510",
            "imagen_referencia_url": "entry.663222153",
            "tamano_pantalla": "entry.845249902",
            "memoria_disponible": "entry.484203162",
            "puertos_conexiones": "entry.220689556",
            "sistema_operativo": "entry.566718222"
        }
    },
    "ProductosRelacionados": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSdArlHxWEIGmo18xkJjJyTR488diWJAxuVRBkGjGYde1HHWhw/formResponse",
        "fields": {
            "nombre_producto": "entry.1822292456",
            "imagen_url": "entry.323601208",
            "descripcion_corta": "entry.391276352",
            "accion_texto": "entry.1999713106",
            "accion_link": "entry.989527757",
            "mostrar_en_inicio": "entry.2072132249"
        }
    },
    "LlamadoAccion_CTA": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSf8NL5UmFX7PV0e7tdrNq-9JjQG43LcdtjLEANAMEmqgK5n2A/formResponse",
        "fields": {
            "titulo_invitacion": "entry.1684820214",
            "boton1_texto": "entry.1447118903",
            "boton1_link": "entry.1591725433",
            "boton2_texto": "entry.1354073510",
            "boton2_link": "entry.1255057595"
        }
    }
}

# No usamos una lista estática de índices ya que Google puede reordenar las hojas.
# En su lugar, detectaremos la hoja correcta buscando las columnas específicas.

def fetch_database():
    """
    Descarga el xlsx de Google Drive, lee todas las hojas y devuelve un diccionario 
    estructurado normalizado para ser consumido por la UI.
    Si el documento es privado, levantará una excepción de Pandas o red.
    """
    try:
        # read_excel con sheet_name=None trae todas las hojas
        all_sheets_dict = pd.read_excel(SPREADSHEET_URL, sheet_name=None)
        
        db = {table_name: [] for table_name in FORMS_MAPPING.keys()}
        
        for sheet_name, df in all_sheets_dict.items():
            # Normalización agresiva: minúsculas, sin espacios y quitar paréntesis
            cols = [str(c).lower().strip().split(" (")[0].replace(" ", "_") for c in df.columns]
            
            # Buscar a qué tabla pertenece esta hoja según sus columnas
            for table_name, config in FORMS_MAPPING.items():
                target_fields = [f.lower().strip().replace(" ", "_") for f in config["fields"].keys()]
                # Si la hoja contiene los campos principales de la tabla
                if all(field in cols for field in target_fields):
                    df = df.fillna("")
                    # Convertimos los nombres de las columnas reales del DF a los nombres semánticos de nuestro mapping
                    # para asegurar que el resto de la app funcione con las llaves consistentes.
                    actual_cols = df.columns.tolist()
                    mapping_correction = {}
                    for i, normalized in enumerate(cols):
                        for target in target_fields:
                            if normalized == target:
                                mapping_correction[actual_cols[i]] = target
                    
                    df = df.rename(columns=mapping_correction)
                    db[table_name] = df.to_dict(orient='records')
                    break 
                    
        return db
    except Exception as e:
        print(f"Error fetching database: {e}")
        return {table_name: [] for table_name in FORMS_MAPPING.keys()}

def get_latest(table_data):
    """Retorna la última fila insertada en la tabla o un dict vacío si no hay datos"""
    if len(table_data) > 0:
        return table_data[-1]
    return {}

def post_to_google_form(table_name: str, payload_data: dict) -> bool:
    """
    Envía datos pre-llenados desde el formulario Flet hacia Google Forms vía HTTP POST.
    Retorna True si fue exitoso (200 OK de Google Forms).
    """
    if table_name not in FORMS_MAPPING:
        return False
        
    config = FORMS_MAPPING[table_name]
    url = config["url"]
    
    # Construir el query params para las `entry.XXX`
    form_data = {}
    for semantic_key, entry_id in config["fields"].items():
        # Captura el valor introducido en Flet, por si falto proveemos un espacio en blanco
        form_data[entry_id] = payload_data.get(semantic_key, "")
        
    try:
        response = requests.post(url, data=form_data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error posting data for {table_name}: {e}")
        return False
