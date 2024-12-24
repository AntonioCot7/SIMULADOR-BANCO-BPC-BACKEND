#!/bin/bash

# Verificar si se pasa un stage, si no se usa "test" como valor predeterminado
STAGE="${1:-test}"

# Lista de servicios
services=(TABLA-CUENTA TABLA-PAGOS TABLA-PRESTAMOS TABLA-SOLICITUD-PRESTAMO TABLA-SOPORTE TABLA-TARJETAS TABLA-TOKENS_ACCESO TABLA-TRANSACCION TABLA-USUARIOS)

# Directorio base donde están las carpetas de las tablas
BASE_DIR="../../"  # Ajusta este valor si la estructura es diferente

# Guardar el directorio de inicio (Deploy/scripts) para regresar allí después de cada despliegue
START_DIR="$(pwd)"

# Función para verificar si un directorio existe
check_directory() {
  if [ ! -d "$1" ]; then
    echo "Error: El directorio $1 no existe. Abortando."
    exit 1
  fi
}

for service in "${services[@]}"
do
  echo "Deploying $service to stage $STAGE..."

  # Cambiar al directorio del servicio usando una ruta relativa
  SERVICE_DIR="$BASE_DIR$service"
  check_directory "$SERVICE_DIR"  # Verifica que el directorio existe

  cd "$SERVICE_DIR" || { echo "No se pudo cambiar al directorio $SERVICE_DIR"; exit 1; }

  # Para ciertos servicios, instalar dependencias si no existen
  if [[ "$service" == "TABLA-PRESTAMOS" || "$service" == "TABLA-SOLICITUD-PRESTAMO" || "$service" == "TABLA-SOPORTE" ]]; then
    if [ ! -f package.json ]; then
      echo "package.json no encontrado. Creando uno nuevo..."
      npm init -y
    fi

    # Verificar si las dependencias están instaladas
    if [ ! -d "node_modules" ]; then
      echo "Running npm install in $service..."
      npm install || { echo "Error al ejecutar npm install en $service"; exit 1; }
    fi

    # Instalar dependencias necesarias si no están presentes
    npm install uuid aws-sdk || { echo "Error al instalar dependencias adicionales en $service"; exit 1; }
  fi

  # Ejecutar deploy para el stage especificado
  echo "Deploying service $service to stage $STAGE"
  npx serverless deploy --stage $STAGE || { echo "Error al desplegar $service en el stage $STAGE"; exit 1; }

  # Volver al directorio base (Deploy/scripts) después de cada despliegue
  cd "$START_DIR" || { echo "Error: No se pudo regresar al directorio base $START_DIR"; exit 1; }

done
