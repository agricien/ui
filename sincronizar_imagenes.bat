@echo off
:: ==========================================
:: MODO OCULTO (PowerShell Wrapper)
:: ==========================================
if "%~1"=="-hidden" goto :run
powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -ArgumentList '-hidden' -WindowStyle Hidden"
exit /b

:run
setlocal enabledelayedexpansion

:: ==========================================
:: CONFIGURACION
:: ==========================================
:: RUTA ORIGEN: Ajusta esta ruta a donde se sincroniza tu OneDrive
set "ONEDRIVE_PATH=%USERPROFILE%\OneDrive - Agricien\imagenes"

:: Intentar detectar rutas alternativas si la anterior no existe
if not exist "!ONEDRIVE_PATH!" set "ONEDRIVE_PATH=%USERPROFILE%\OneDrive\imagenes"
if not exist "!ONEDRIVE_PATH!" set "ONEDRIVE_PATH=%USERPROFILE%\Agricien\imagenes"

set "REPO_DIR=imagenes"
set "REMOTE_REPO=git@github.com:agricien/imagenes.git"

:: Cambiar al directorio del script
cd /d "%~dp0"

:: 1. Verificar Carpeta Origen
if not exist "%ONEDRIVE_PATH%" (
    :: Si no se encuentra, registrar error y salir (como es oculto no podemos pausar)
    echo [%date% %time%] ERROR: No se encontro la carpeta local: "%ONEDRIVE_PATH%" >> sincronizacion_log.txt
    exit /b
)

:: 2. Inicializar repositorio si no existe
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

:: 3. Sincronizar usando ROBOCOPY (Modo Espejo / Mirror)
:: /MIR: Espeja la carpeta (borra en destino lo que no esta en origen)
:: /XD .git: Protege la carpeta de configuracion de Git
robocopy "%ONEDRIVE_PATH%" "%REPO_DIR%" /MIR /XD .git /R:3 /W:5 > nul

:: 4. Git Add, Commit y Push
cd /d "%REPO_DIR%"
git add .
:: Solo subir si hay cambios
git diff --cached --quiet
if %ERRORLEVEL% neq 0 (
    git commit -m "Sincronizacion automatica (OneDrive Local): %date% %time%"
    git push origin main
)

exit /b

