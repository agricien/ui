@echo off
setlocal enabledelayedexpansion

:: ==========================================
:: CONFIGURACION
:: ==========================================
set "URL=https://agricien-my.sharepoint.com/:f:/p/edgar_mendez/IgBZVjiP8iH8T5-RWYIelhgQAf2HJ1IftQkF7T2TWPNTR4U?e=tDuSgV&download=1"
set "REPO_DIR=imagenes"
set "TEMP_ZIP=onedrive_media.zip"
set "TEMP_DIR=temp_extract"
set "REMOTE_REPO=git@github.com:agricien/imagenes.git"

echo ==========================================
echo    SINCRONIZADOR ONEDRIVE -> GITHUB
echo ==========================================

:: 1. Inicializar repositorio si no existe
if not exist "%REPO_DIR%\.git" (
    echo [INFO] Inicializando repositorio local...
    if not exist "%REPO_DIR%" mkdir "%REPO_DIR%"
    cd /d "%REPO_DIR%"
    git init
    if not exist "README.md" echo # imagenes > README.md
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin %REMOTE_REPO%
    echo [INFO] Repositorio configurado.
    cd ..
)

:: 2. Descargar contenido desde OneDrive
echo [1/4] Descargando archivos desde OneDrive...
curl -L -o "%TEMP_ZIP%" "%URL%"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] No se pudo descargar el archivo de OneDrive.
    pause
    exit /b
)

:: 3. Descomprimir y Sincronizar
echo [2/4] Procesando archivos...
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"
tar -xf "%TEMP_ZIP%" -C "%TEMP_DIR%"

:: Limpiar el repo local (excepto .git y README.md) para detectar borrados
echo [3/4] Sincronizando cambios (deteccion de borrados)...
for /d %%i in ("%REPO_DIR%\*") do (
    if /i not "%%~nxi"==".git" rd /s /q "%%i"
)
for %%i in ("%REPO_DIR%\*") do (
    if /i not "%%~nxi"==".git" if /i not "%%~nxi"=="README.md" del /q "%%i"
)

:: Copiar nuevos archivos desde la descarga
xcopy /s /e /y "%TEMP_DIR%\*" "%REPO_DIR%\" > nul

:: 4. Git Add, Commit y Push
echo [4/4] Subiendo a GitHub...
cd /d "%REPO_DIR%"
git add .
:: Verificar si hay cambios antes de hacer commit
git diff --cached --quiet
if %ERRORLEVEL% neq 0 (
    git commit -m "Sincronizacion automatica: %date% %time%"
    git push origin main
    echo [SUCCESS] Cambios subidos correctamente.
) else (
    echo [INFO] No hay cambios detectados.
)

:: Limpieza final
cd ..
rd /s /q "%TEMP_DIR%"
del "%TEMP_ZIP%"

echo ==========================================
echo Proceso completado exitosamente.
echo ==========================================
timeout /t 5
