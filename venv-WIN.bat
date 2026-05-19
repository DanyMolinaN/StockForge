@echo off
SETLOCAL EnableDelayedExpansion

:: ==========================================
:: 1. CONFIGURACIÓN (Variables)
:: ==========================================
SET VENV_DIR=.venv
SET REQ_FILE=requirements.txt

call :PrintBanner "Iniciando configuracion del entorno de desarrollo"

:: ==========================================
:: 2. FLUJO PRINCIPAL (Orquestador / Capa de Negocio)
:: ==========================================
call :EnsureUV
if !ERRORLEVEL! neq 0 goto :FatalError

call :SetupVirtualEnv
call :InstallDependencies

call :PrintSuccess
goto :EndScript

:: ==========================================
:: 3. MÓDULOS DE LÓGICA (Alta Cohesión)
:: ==========================================

:EnsureUV
echo [1/3] Verificando herramientas base (uv)...
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] 'uv' no encontrado. Iniciando instalacion automatica...
    :: Se invoca PowerShell para instalar uv segun la documentacion oficial de Astral
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    
    if !ERRORLEVEL! neq 0 (
        echo [ERROR] No se pudo instalar 'uv' automaticamente.
        exit /b 1
    )
    
    :: Se recarga la variable de entorno PATH localmente para detectar uv inmediatamente
    FOR /F "tokens=2* delims= " %%A IN ('REG QUERY "HKCU\Environment" /v PATH') DO SET "USER_PATH=%%B"
    SET "PATH=%USER_PATH%;%PATH%"
    
    echo [OK] 'uv' instalado correctamente.
) else (
    echo [OK] 'uv' se encuentra instalado en el sistema.
)
exit /b 0

:SetupVirtualEnv
echo.
echo [2/3] Preparando entorno virtual...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Creando nuevo entorno virtual en '%VENV_DIR%'...
    uv venv %VENV_DIR%
) else (
    echo [OK] El entorno virtual ya existe. Se omitira la creacion.
)
exit /b 0

:InstallDependencies
echo.
echo [3/3] Instalando dependencias del proyecto...
if exist "%REQ_FILE%" (
    call "%VENV_DIR%\Scripts\activate.bat"
    uv pip install -r "%REQ_FILE%"
    echo [OK] Dependencias instaladas exitosamente.
) else (
    echo [ADVERTENCIA] No se encontro '%REQ_FILE%'. El entorno esta vacio.
)
exit /b 0

:: ==========================================
:: 4. CAPA DE PRESENTACIÓN (DRY)
:: ==========================================

:PrintBanner
echo ==================================================
echo %~1
echo ==================================================
echo.
exit /b 0

:PrintSuccess
echo.
call :PrintBanner "[EXITO] Entorno configurado correctamente."
echo Para activar el entorno, ejecuta:
echo call %VENV_DIR%\Scripts\activate.bat
echo ==================================================
exit /b 0

:FatalError
echo.
call :PrintBanner "[FATAL] La configuracion se detuvo debido a un error."
exit /b 1

:EndScript
ENDLOCAL
pause