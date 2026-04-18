import os

bat_content = r"""@echo off
setlocal
cd /d "%~dp0"
echo ==========================================
echo    ACTUALIZADOR DE CONTENIDO AGRICIEN
echo ==========================================
echo.
echo [1/2] Sincronizando con OneDrive...
python transform_content.py
echo.
echo [2/2] Subiendo cambios a GitHub...
git add data/news.json index.html transform_content.py
git commit -m "Actualizacion automatica de noticias y UI"
git push
echo.
echo ==========================================
echo Proceso completado exitosamente. 
echo La ventana se cerrara en 5 segundos...
echo ==========================================
timeout /t 5
"""

with open('actualizar_blog.bat', 'wb') as f:
    # Asegurar CRLF y codificación compatible
    formatted_content = bat_content.replace('\n', '\r\n').encode('ascii', errors='replace')
    f.write(formatted_content)

print("Archivo actualizar_blog.bat optimizado para cierre automatico.")
