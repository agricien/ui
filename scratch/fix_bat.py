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
echo [2/2] Buscando noticias RSS adicionales...
python scraper.py
echo.
echo ==========================================
echo Proceso completado. Tu web esta actualizada.
echo ==========================================
pause
"""

# Asegurar CRLF y escribir en binario para evitar problemas de codificación
with open('actualizar_blog.bat', 'wb') as f:
    # Reemplazar \n por \r\n y codificar
    formatted_content = bat_content.replace('\n', '\r\n').encode('ascii', errors='replace')
    f.write(formatted_content)

print("Archivo actualizar_blog.bat creado correctamente con cd /d %~dp0")
