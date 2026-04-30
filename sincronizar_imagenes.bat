@echo off
:: ==========================================
:: MODO OCULTO (PowerShell Wrapper)
:: ==========================================
if "%~1"=="-hidden" goto :run
powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -ArgumentList '-hidden' -WindowStyle Hidden"
exit /b

:run
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: ==========================================
:: CONFIGURACION
:: ==========================================
set "REPO_DIR=..\imagenes"
set "REMOTE_REPO=https://github.com/agricien/imagenes.git"

:: 1. Inicializar repositorio si no existe
if not exist "%REPO_DIR%\.git" (
    if not exist "%REPO_DIR%" mkdir "%REPO_DIR%"
    cd /d "%REPO_DIR%"
    git init
    echo # imagenes > README.md
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin %REMOTE_REPO%
    cd ..
)

:: 2. Ejecutar Sincronizacion de Google Drive (Python)
python sync_gdrive.py > nul 2>&1

:: 3. Git Add, Commit y Push
cd /d "%REPO_DIR%"
git add .
:: Solo subir si hay cambios
git diff --cached --quiet
if %ERRORLEVEL% neq 0 (
    git commit -m "Sincronizacion automatica Google Drive: %date% %time%"
    git push origin main
)

exit /b
