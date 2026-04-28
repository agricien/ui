@echo off
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
git add .
git commit -m "Actualizacion: Soporte para Temas, Subtemas y Banner dinamico"
git push
echo.
echo ==========================================
echo Proceso completado exitosamente. 
echo La ventana se cerrara en 5 segundos...
echo ==========================================
timeout /t 5
