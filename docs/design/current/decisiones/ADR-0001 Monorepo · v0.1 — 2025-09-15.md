---
title: "ADR-0001 Monorepo"
project: "ennui-rag"
doc_type: "design"
version: "v0.1"
date: "2025-09-15"
source_of_truth: "to-be"
---

# ADR-0001: Estructura Monorepo

## Contexto

El proyecto ennui-rag necesita una estructura que permita:
- Desarrollo modular de componentes
- Gestión centralizada de dependencias
- Documentación unificada
- Scripts de automatización compartidos

## Decisión

Adoptar estructura de monorepo con:

```
ennui-rag/
├── src/ennui_rag/          # Código fuente principal
├── docs/                   # Documentación centralizada
├── scripts/                # Scripts de automatización
├── notebooks/              # Jupyter notebooks
├── configs/                # Configuraciones
└── data/                   # Datos del proyecto
```

## Alternativas Consideradas

1. **Multi-repo** - Repositorios separados por módulo
2. **Microservicios** - Servicios independientes
3. **Monolito** - Todo en un solo archivo

## Consecuencias

### Positivas
- ✅ Gestión centralizada de dependencias
- ✅ Documentación unificada
- ✅ Scripts compartidos
- ✅ Desarrollo más simple

### Negativas
- ❌ Acoplamiento entre módulos
- ❌ Tamaño del repositorio
- ❌ Dependencias compartidas
