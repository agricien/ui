@echo off
:: ==============================================================================
:: SCRIPT PRINCIPAL DE ACTUALIZACIÓN DEL BLOG (AgriCien)
:: ==============================================================================

:: Comprobar si ya se esta ejecutando en modo oculto (evita la ventana negra)
if "%~1"=="-hidden" goto :run

:: Si no tiene el flag -hidden, relanzar el script usando PowerShell en modo oculto
powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -ArgumentList '-hidden' -WindowStyle Hidden"
exit /b

:run
setlocal
cd /d "%~dp0"

:: 1. Sincronizar imagenes desde Google Drive (Llama al script secundario)
call .\sincronizar_imagenes.bat -hidden

:: 2. Sincronizar datos desde OneDrive (Ejecuta el transformador de Excel a JSON)
python transform_content.py > nul 2>&1

:: 3. Subiendo cambios a GitHub (Actualiza el repositorio de la web)
git add . > nul 2>&1
git commit -m "Actualizacion automatica: %date% %time%" > nul 2>&1
git push > nul 2>&1

exit /b

