---
title: "Design Documentation - Legacy"
project: "ennui-rag"
doc_type: "design"
version: "v0.2"
date: "2025-09-16"
source_of_truth: "historical"
---

# Design Documentation - Legacy

## Propósito

Esta carpeta contiene la **documentación de diseño histórica** del proyecto ennui-rag. Aquí encontrarás:

- Archivos de diseño anteriores con fecha de modificación append
- Diseños obsoletos o versiones anteriores
- Decisiones arquitectónicas históricas
- Contexto de evolución del diseño

## Cuándo usar esta documentación

- **Contexto histórico** - Para entender cómo evolucionó el diseño
- **Migración** - Para comparar cambios entre versiones
- **Troubleshooting** - Para entender decisiones de diseño pasadas
- **Arqueología de diseño** - Para entender la evolución del sistema

## Convención de Nombres

Los archivos en legacy siguen la convención:
```
nombre-original_YYYY-MM-DD.ext
```

Donde:
- `nombre-original` - Nombre original del archivo
- `YYYY-MM-DD` - Fecha de última modificación
- `.ext` - Extensión original

## Estructura

```
legacy/
├── README.md                    # Este archivo
└── [archivos con fecha append]  # Archivos históricos
```

## Política de Mantenimiento

- **Solo lectura** - Esta documentación no se actualiza activamente
- **Preservar contexto** - Mantener metadatos de cuándo y por qué se movió aquí
- **Archivo** - Considerar comprimir o archivar documentación muy antigua
- **Referencias** - Mantener referencias cruzadas con documentación actual cuando sea relevante

## Migración desde Current

Cuando la documentación en `../current/` se vuelve obsoleta:

1. **Mover archivos** - Mover a la carpeta `legacy/`
2. **Append fecha** - Agregar fecha de modificación al nombre
3. **Preservar metadatos** - Mantener timestamps y versiones
4. **Actualizar referencias** - Actualizar enlaces en documentación actual
5. **Documentar razón** - Explicar por qué se movió a legacy

---
*Documentación de diseño histórica preservada para contexto y referencia*
