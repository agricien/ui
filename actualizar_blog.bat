@echo off
setlocal
chcp 65001 > nul
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
echo Proceso completado. Tu web está actualizada.
echo ==========================================
pause
