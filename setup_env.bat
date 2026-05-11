@echo off
SETLOCAL

:: ==========================================
:: 1. CONFIGURACIÓN (Variables)
:: ==========================================
SET VENV_DIR=.venv
SET REQ_FILE=requirements.txt

echo ==================================================
echo Iniciando configuracion del entorno de desarrollo...
echo ==================================================
echo.

:: ==========================================
:: 2. VALIDACIÓN DE DEPENDENCIAS EXTERNAS
:: ==========================================
echo [1/3] Verificando herramientas base...
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] 'uv' no esta instalado o no esta en el PATH del sistema.
    echo Por favor, instala uv antes de continuar.
    exit /b 1
)
echo [OK] 'uv' encontrado.

:: ==========================================
:: 3. CREACIÓN DEL ENTORNO VIRTUAL
:: ==========================================
echo.
echo [2/3] Preparando entorno virtual...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creando nuevo entorno virtual en '%VENV_DIR%'...
    uv venv %VENV_DIR%
) else (
    echo [INFO] El entorno virtual ya existe. Se omitira la creacion.
)

:: ==========================================
:: 4. INSTALACIÓN DE PAQUETES
:: ==========================================
echo.
echo [3/3] Instalando dependencias del proyecto...
if exist "%REQ_FILE%" (
    :: Usamos 'call' para que el script no se detenga al ejecutar otro .bat
    call "%VENV_DIR%\Scripts\activate.bat"
    uv pip install -r "%REQ_FILE%"
) else (
    echo [ADVERTENCIA] No se encontro el archivo '%REQ_FILE%'.
    echo El entorno fue creado, pero no se instalaron dependencias.
)

:: ==========================================
:: 5. FINALIZACIÓN
:: ==========================================
echo.
echo ==================================================
echo [EXITO] Entorno configurado correctamente.
echo.
echo Para empezar a trabajar, activa el entorno manualmente ejecutando:
echo call %VENV_DIR%\Scripts\activate.bat
echo ==================================================
ENDLOCAL
pause