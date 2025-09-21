---
title: "Generar árbol de funciones"
project: "ennui-rag"
doc_type: "playbook"
version: "v0.1"
date: "2025-09-15"
source_of_truth: "as-is"
---

# Generar árbol de funciones

## Propósito

Generar documentación automática de la estructura de funciones del proyecto ennui-rag.

## Procedimiento

### 1. Ejecutar script de generación
```bash
cd /home/alvaro_e_mur/ennui-rag
python scripts/gen_kb.py
```

### 2. Verificar salida
El script genera:
- `docs/kb/snapshots/YYYY-MM-DD/funciones-resumen.md`
- Actualiza `docs/kb/snapshots/YYYY-MM-DD/arbol-modulos.md`

### 3. Revisar contenido
- Verificar que todas las funciones estén documentadas
- Comprobar firmas de funciones
- Validar estructura de módulos

### 4. Commit cambios
```bash
git add docs/kb/snapshots/
git commit -m "docs: actualizar snapshot KB $(date +%Y-%m-%d)"
```

## Configuración

El script `gen_kb.py` debe estar configurado para:
- Escanear `src/ennui_rag/`
- Extraer docstrings
- Generar firmas de funciones
- Crear estructura jerárquica

## Troubleshooting

- **Error de importación**: Verificar PYTHONPATH
- **Módulos no encontrados**: Revisar estructura de directorios
- **Permisos**: Verificar acceso de escritura a docs/
