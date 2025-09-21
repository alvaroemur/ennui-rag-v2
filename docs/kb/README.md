---
title: "Knowledge Base - Sistema de Snapshots Automatizado"
project: "ennui-rag"
doc_type: "kb"
version: "v0.2"
date: "2025-09-16"
source_of_truth: "as-is"
---

# Knowledge Base - Sistema de Snapshots Automatizado

## ¿Qué es un snapshot?

Un snapshot es una captura temporal completa de la documentación del proyecto ennui-rag en un momento específico. Contiene:

- **Estructura actual** - Estado real del código y archivos
- **Documentación técnica** - Funciones, módulos, arquitectura, pipelines
- **Metadatos** - Versión, fecha, contexto editorial
- **Front-matter YAML** - Metadatos estructurados para cada archivo

## ¿Cómo se genera?

Los snapshots se generan automáticamente mediante `scripts/gen_kb.py` que:

1. **Escanea el código fuente** - Analiza módulos Python, notebooks, YAML/JSON
2. **Extrae documentación técnica** - Funciones, clases, imports, UI heuristics
3. **Genera contenido con LLM** - Usa OpenAI para enriquecer secciones específicas
4. **Integra contexto editorial** - Incluye notas del autor sobre cambios recientes
5. **Crea archivos especializados** - Genera múltiples archivos MD con front-matter
6. **Maneja versionado** - Mueve snapshots anteriores a legacy automáticamente

## Flujo de Generación

```bash
# Generar snapshot con contexto editorial
python scripts/gen_kb.py --context-file contexto.md --verbose

# Generar snapshot con contexto directo
python scripts/gen_kb.py --context "Cambios recientes..." --verbose

# Generar snapshot básico
python scripts/gen_kb.py --verbose
```

## ¿Cómo usarlo en prompts?

Para usar un snapshot en prompts de IA:

1. **Referencia el snapshot más reciente** en `docs/kb/snapshots/[timestamp]`
2. **Cita archivo y sección** específica con front-matter
3. **Usa el contexto editorial** para entender cambios recientes
4. **Formato recomendado**: `[archivo:sección]` o `[snapshot:archivo:sección]`

## Estructura de un snapshot

```
snapshots/YYYY-MM-DD_HHMMSS/          # Timestamp GMT-5 (Lima)
├── resumen-ejecutivo.md              # Resumen del proyecto y estado actual
├── arquitectura-flujo.md             # Arquitectura y flujo de datos
├── arbol-modulos.md                  # Estructura completa + APIs + pipelines
├── operacion-troubleshooting.md      # Cómo usar + troubleshooting
└── notas-cambio.md                   # Cambios + contexto editorial
```

## Sistema de Legacy

- **Snapshots anteriores** se mueven automáticamente a `legacy/[timestamp]`
- **Solo se mantiene** el snapshot más reciente en `/snapshots/`
- **Estructura limpia** sin carpetas duplicadas o vacías

## Contexto Editorial

El sistema integra contexto editorial del autor para:
- **Priorizar roadmap** basado en trabajo reciente
- **Enriquecer secciones** con información específica del proyecto
- **Documentar cambios** y decisiones técnicas
- **Mantener coherencia** entre snapshots

## Timestamps y Zona Horaria

- **Formato**: `YYYY-MM-DD_HHMMSS` (ej: `2025-09-16_173856`)
- **Zona horaria**: GMT-5 (Lima/Perú) - consistente todo el año
- **Precisión**: Incluye hora exacta de generación
