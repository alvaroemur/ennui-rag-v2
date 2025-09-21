#!/bin/bash
# Script para mover archivos de current/ a legacy/ con fecha append
# Uso: ./move_to_legacy.sh archivo_origen

if [ $# -eq 0 ]; then
    echo "Uso: $0 <archivo_origen>"
    echo "Ejemplo: $0 current/vision-narrativa/Vision.md"
    exit 1
fi

ARCHIVO_ORIGEN="$1"
LEGACY_DIR="legacy"

# Verificar que el archivo existe
if [ ! -f "$ARCHIVO_ORIGEN" ]; then
    echo "Error: El archivo '$ARCHIVO_ORIGEN' no existe"
    exit 1
fi

# Obtener fecha de modificación
FECHA_MOD=$(stat -c %y "$ARCHIVO_ORIGEN" | cut -d' ' -f1)

# Obtener nombre base y extensión
NOMBRE_BASE=$(basename "$ARCHIVO_ORIGEN")
NOMBRE_SIN_EXT="${NOMBRE_BASE%.*}"
EXTENSION="${NOMBRE_BASE##*.}"

# Crear nombre con fecha append
NOMBRE_LEGACY="${NOMBRE_SIN_EXT}_${FECHA_MOD}.${EXTENSION}"

# Crear directorio legacy si no existe
mkdir -p "$LEGACY_DIR"

# Mover archivo
echo "Moviendo: $ARCHIVO_ORIGEN -> $LEGACY_DIR/$NOMBRE_LEGACY"
mv "$ARCHIVO_ORIGEN" "$LEGACY_DIR/$NOMBRE_LEGACY"

echo "✅ Archivo movido a legacy con fecha append: $NOMBRE_LEGACY"
