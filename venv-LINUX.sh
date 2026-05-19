#!/usr/bin/env bash

# ==========================================
# 1. CONFIGURACIÓN (Variables)
# ==========================================
VENV_DIR=".venv"
REQ_FILE="requirements.txt"

# ==========================================
# 4. CAPA DE PRESENTACIÓN (DRY)
# ==========================================
print_banner() {
    echo "=================================================="
    echo "$1"
    echo "=================================================="
    echo ""
}

print_success() {
    echo ""
    print_banner "[ÉXITO] Entorno configurado correctamente."
    echo "Para empezar a trabajar, activa el entorno ejecutando:"
    echo "source ${VENV_DIR}/bin/activate"
    echo "=================================================="
}

fatal_error() {
    echo ""
    print_banner "[FATAL] La configuración se detuvo debido a un error."
    exit 1
}

# ==========================================
# 3. MÓDULOS DE LÓGICA (Alta Cohesión)
# ==========================================
ensure_uv() {
    echo "[1/3] Verificando herramientas base (uv)..."
    if ! command -v uv &> /dev/null; then
        echo "[INFO] 'uv' no encontrado. Iniciando instalación automática..."
        
        # Validación de herramientas requeridas para la descarga
        if ! command -v curl &> /dev/null; then
            echo "[ERROR] 'curl' es requerido para instalar 'uv' de forma automática."
            return 1
        fi

        # Instalación oficial de uv mediante el script de Astral
        if curl -LsSf https://astral.sh/uv/install.sh | sh; then
            # Añadir temporalmente al PATH para la ejecución actual del script
            export PATH="$HOME/.local/bin:$PATH"
            echo "[OK] 'uv' instalado correctamente."
        else
            echo "[ERROR] No se pudo instalar 'uv' automáticamente."
            return 1
        fi
    else
        echo "[OK] 'uv' se encuentra instalado en el sistema."
    fi
    return 0
}

setup_virtualenv() {
    echo ""
    echo "[2/3] Preparando entorno virtual..."
    if [ ! -f "${VENV_DIR}/bin/activate" ]; then
        echo "[INFO] Creando nuevo entorno virtual en '${VENV_DIR}'..."
        uv venv "${VENV_DIR}"
    else
        echo "[OK] El entorno virtual ya existe. Se omitirá la creación."
    fi
    return 0
}

install_dependencies() {
    echo ""
    echo "[3/3] Instalando dependencias del proyecto..."
    if [ -f "${REQ_FILE}" ]; then
        # Activar el entorno localmente dentro del subproceso del script
        source "${VENV_DIR}/bin/activate"
        if uv pip install -r "${REQ_FILE}"; then
            echo "[OK] Dependencias instaladas exitosamente."
        else
            echo "[ERROR] Falló la instalación de dependencias."
            return 1
        fi
    else
        echo "[ADVERTENCIA] No se encontró el archivo '${REQ_FILE}'."
        echo "El entorno fue creado, pero no se instalaron dependencias."
    fi
    return 0
}

# ==========================================
# 2. FLUJO PRINCIPAL (Orquestador / Capa de Negocio)
# ==========================================
main() {
    print_banner "Iniciando configuracion del entorno de desarrollo (Linux)"
    
    ensure_uv || fatal_error
    setup_virtualenv || fatal_error
    install_dependencies || fatal_error
    
    print_success
}

# Ejecución del orquestador
main