import requests
import re
import os
import sys
from datetime import datetime

# ==========================================
# CONFIGURACION
# ==========================================
FOLDER_ID = "1Z1j6efSoIOpfDTrp97-TdzWocNjDlmFM"
OUTPUT_DIR = "../imagenes"

def get_file_list(folder_id):
    """Obtiene la lista de archivos de una carpeta publica de Google Drive."""
    url = f"https://drive.google.com/embeddedfolderview?id={folder_id}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Buscar el ID y el nombre usando la estructura del HTML de la vista embebida
        # Formato: id="entry-ID" ... flip-entry-title">Nombre</div>
        matches = re.findall(r'id="entry-([\w-]+)".*?class="flip-entry-title">([^<]+)</div>', response.text, re.DOTALL)
        
        files = []
        seen = set()
        for fid, name in matches:
            if fid not in seen:
                name = name.strip()
                ext = os.path.splitext(name)[1].lower()
                if ext in ['.jpg', '.jpeg', '.jfif', '.png', '.webp', '.gif', '.mp4', '.mov', '.avi', '.webm']:
                    files.append((fid, name))
                    seen.add(fid)
        return files
    except Exception as e:
        print(f"Error al listar archivos: {e}")
        return []


def download_file(file_id, name, output_path):
    """Descarga un archivo publico de Google Drive."""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Error descargando {name}: {e}")
        return False

def sync():
    print(f"Iniciando sincronizacion de Google Drive (ID: {FOLDER_ID})...")
    
    files = get_file_list(FOLDER_ID)
    if not files:
        print("No se encontraron archivos o la carpeta no es publica.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Lista de archivos actuales en la carpeta local para detectar borrados
    local_files = set(os.listdir(OUTPUT_DIR))
    if ".git" in local_files: local_files.remove(".git")
    if "README.md" in local_files: local_files.remove("README.md")
    
    remote_names = set()

    for fid, name in files:
        remote_names.add(name)
        file_path = os.path.join(OUTPUT_DIR, name)
        
        # Si el archivo ya existe, podriamos saltarlo (o comparar tamaños)
        # Para simplificar, descargamos si no existe
        if not os.path.exists(file_path):
            print(f"Descargando: {name}")
            download_file(fid, name, file_path)
        else:
            print(f"Ya existe: {name}")

    # Borrar archivos locales que ya no estan en Drive
    for local_name in local_files:
        if local_name not in remote_names:
            print(f"Borrando archivo eliminado en Drive: {local_name}")
            os.remove(os.path.join(OUTPUT_DIR, local_name))

    print("Sincronizacion completada.")

if __name__ == "__main__":
    sync()
