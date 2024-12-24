#!/bin/bash

# Verificar si se pasa un stage, si no se usa "dev" como valor predeterminado
STAGE="${1:-dev}"

# Lista de servicios
services=(TABLA-CUENTA TABLA-PAGOS TABLA-PRESTAMOS TABLA-SOLICITUD-PRESTAMO TABLA-SOPORTE TABLA-TARJETAS TABLA-TOKENS_ACCESO TABLA-TRANSACCION TABLA-USUARIOS)

# Directorio base donde están las carpetas de las tablas
BASE_DIR="../../"  # Ajusta este valor si la estructura es diferente

# Guardar el directorio de inicio (Deploy/scripts) para regresar allí después de cada despliegue
START_DIR="$(pwd)"

for service in "${services[@]}"
do
  echo "Deploying $service to stage $STAGE..."

  # Comprobar si el directorio del servicio existe
  if [ ! -d "$BASE_DIR$service" ]; then
    echo "Error: El directorio $BASE_DIR$service no existe. Saliendo del script."
    exit 1  # Termina el script si el directorio no existe
  fi

  # Cambiar al directorio del servicio
  cd "$BASE_DIR$service" || { echo "Error: No se pudo acceder al directorio $BASE_DIR$service"; exit 1; }

  # Para ciertos servicios, instalar dependencias si no existen
  if [[ "$service" == "TABLA-PRESTAMOS" || "$service" == "TABLA-SOLICITUD-PRESTAMO" || "$service" == "TABLA-SOPORTE" ]]; then
    if [ ! -f package.json ]; then
      echo "package.json no encontrado. Creando uno nuevo..."
      npm init -y
    fi

    # Verificar si las dependencias ya están instaladas
    if [ ! -d "node_modules" ]; then
      echo "Running npm install in $service..."
      npm install
    fi

    # Instalar dependencias específicas
    npm install uuid aws-sdk
  fi

  # Ejecutar deploy para el stage especificado
  npx serverless deploy --stage $STAGE || { echo "Error: El despliegue de $service falló."; exit 1; }

  # Volver al directorio base (Deploy/scripts) después de cada despliegue
  cd "$START_DIR" || { echo "Error: No se pudo regresar al directorio base $START_DIR"; exit 1; }

done
