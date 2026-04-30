@echo off
:: Comprobar si ya se esta ejecutando en modo oculto
if "%~1"=="-hidden" goto :run

:: Si no, relanzar el script en una ventana oculta de PowerShell
powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -ArgumentList '-hidden' -WindowStyle Hidden"
exit /b

:run
setlocal
cd /d "%~dp0"

:: 1. Sincronizar con OneDrive
python transform_content.py > nul 2>&1

:: 2. Subiendo cambios a GitHub
git add . > nul 2>&1
git commit -m "Actualizacion automatica: %date% %time%" > nul 2>&1
git push > nul 2>&1

exit /b

