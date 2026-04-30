@echo off
:: ==============================================================================
:: SCRIPT DE SINCRONIZACIÓN DE IMÁGENES (Google Drive -> GitHub)
:: ==============================================================================

:: MODO OCULTO: Se asegura de que no se abra una ventana de comandos
if "%~1"=="-hidden" goto :run
powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -ArgumentList '-hidden' -WindowStyle Hidden"
exit /b

:run
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: ==============================================================================
:: CONFIGURACION
:: ==============================================================================
:: REPO_DIR: Ubicación de la carpeta de imágenes (ahora fuera del repo UI para evitar errores)
set "REPO_DIR=..\imagenes"
set "REMOTE_REPO=https://github.com/agricien/imagenes.git"

:: 1. Inicializar repositorio si no existe (Primera ejecución)
if not exist "%REPO_DIR%\.git" (
    if not exist "%REPO_DIR%" mkdir "%REPO_DIR%"
    cd /d "%REPO_DIR%"
    git init
    echo # imagenes > README.md
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin %REMOTE_REPO%
    cd /d "%~dp0"
)

:: 2. Ejecutar Sincronizacion de Google Drive (Script de Python)
:: Este paso descarga, borra y renombra archivos según lo que haya en Drive.
python sync_gdrive.py > nul 2>&1

:: 3. Git Add, Commit y Push (Sincroniza con el repositorio de imágenes de GitHub)
cd /d "%REPO_DIR%"
git add .
:: Solo realizar el commit y push si Git detecta cambios reales en los archivos
git diff --cached --quiet
if %ERRORLEVEL% neq 0 (
    git commit -m "Sincronizacion automatica Google Drive: %date% %time%"
    git push origin main
)

exit /b
