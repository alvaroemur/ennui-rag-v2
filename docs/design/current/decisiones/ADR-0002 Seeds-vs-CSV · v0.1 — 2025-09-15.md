---
title: "ADR-0002 Seeds vs CSV"
project: "ennui-rag"
doc_type: "design"
version: "v0.1"
date: "2025-09-15"
source_of_truth: "to-be"
---

# ADR-0002: Seeds vs CSV para Datos Iniciales

## Contexto

El sistema necesita cargar datos iniciales para:
- Catálogos de archivos
- Configuraciones de programas
- Metadatos de sesiones
- Plantillas de cumplimiento

## Decisión

Usar **CSV como formato principal** con seeds como respaldo:

1. **CSV** - Para datos masivos y exportables
2. **Seeds** - Para datos de configuración crítica
3. **JSON** - Para metadatos complejos

## Alternativas Consideradas

1. **Solo Seeds** - Scripts de Python para datos iniciales
2. **Solo CSV** - Archivos CSV únicamente
3. **Base de datos** - Datos pre-cargados en DB
4. **API externa** - Datos desde servicio externo

## Consecuencias

### Positivas
- ✅ CSV es fácil de editar y versionar
- ✅ Seeds permiten lógica compleja
- ✅ Flexibilidad en formatos
- ✅ Fácil migración de datos

### Negativas
- ❌ Múltiples formatos a mantener
- ❌ Complejidad en la carga
- ❌ Validación de consistencia
