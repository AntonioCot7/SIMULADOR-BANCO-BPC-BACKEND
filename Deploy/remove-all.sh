#!/bin/bash

# Directorio donde se encuentran los scripts
SCRIPT_DIR="$(pwd)/scripts"

# Lista de los scripts de eliminación
scripts=("remove-dev.sh" "remove-prod.sh" "remove-test.sh")

# Función para verificar y aplicar chmod
check_and_chmod() {
  for script in "${scripts[@]}"
  do
    script_path="$SCRIPT_DIR/$script"
    if [ -f "$script_path" ]; then
      if [ ! -x "$script_path" ]; then
        echo "$script_path no tiene permisos de ejecución, aplicando chmod..."
        chmod +x "$script_path"
      else
        echo "$script_path ya tiene permisos de ejecución."
      fi
    else
      echo "$script_path no encontrado."
    fi
  done
}

# Llamar a la función para verificar los permisos
check_and_chmod


# Ejecutar los tres scripts de eliminación
echo "Ingresando al directorio de scripts..."
cd "$SCRIPT_DIR"

echo "----------------------------"
echo "Ejecutando $SCRIPT_DIR/remove-dev.sh..."
./remove-dev.sh
echo "REMOVE STAGE DEV COMPLETADO"

echo "----------------------------"
echo "Ejecutando $SCRIPT_DIR/remove-prod.sh..."
./remove-prod.sh
echo "REMOVE STAGE PROD COMPLETADO"

echo "----------------------------"
echo "Ejecutando $SCRIPT_DIR/remove-test.sh..."
./remove-test.sh
echo "REMOVE STAGE TEST COMPLETADO"

echo "----------------------------"
echo "Todos los recursos han sido eliminados."

echo "----------------------------"
cd "../"
echo "Regresando  al directorio principal..."