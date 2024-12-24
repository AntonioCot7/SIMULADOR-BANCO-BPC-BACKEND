#!/bin/bash

# Verificar si se pasa un stage, si no se usa "prod" como valor predeterminado
STAGE="${1:-prod}"

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
  echo "Removing resources for $service from stage $STAGE..."

  # Construir la ruta del directorio del servicio
  SERVICE_DIR="$BASE_DIR$service"
  check_directory "$SERVICE_DIR"  # Verificar si el directorio existe

  # Cambiar al directorio del servicio
  cd "$SERVICE_DIR" || { echo "No se pudo cambiar al directorio $SERVICE_DIR"; exit 1; }

  # Ejecutar el comando para eliminar los recursos del stage especificado
  echo "Ejecutando: npx serverless remove --stage $STAGE"
  npx serverless remove --stage "$STAGE" || { echo "Error al ejecutar 'serverless remove' para $service"; exit 1; }

  # Volver al directorio base (Deploy/scripts) después de cada despliegue
  cd "$START_DIR" || { echo "Error: No se pudo regresar al directorio base $START_DIR"; exit 1; }

done

echo "Todos los recursos han sido eliminados correctamente para el stage $STAGE."
