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
git add data/news.json
git commit -m "Actualizacion automatica de noticias desde Excel"
git push
echo.
echo ==========================================
echo Proceso completado. Tu web en internet se
echo actualizara en un par de minutos.
echo ==========================================
pause
"""

with open('actualizar_blog.bat', 'wb') as f:
    # Asegurar CRLF y codificación compatible
    formatted_content = bat_content.replace('\n', '\r\n').encode('ascii', errors='replace')
    f.write(formatted_content)

print("Archivo actualizar_blog.bat actualizado con exito.")
