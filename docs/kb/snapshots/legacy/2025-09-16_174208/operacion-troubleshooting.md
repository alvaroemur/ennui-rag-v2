---
title: "Operación y Troubleshooting - Snapshot 2025-09-16_174208"
project: "ennui-rag"
doc_type: "kb"
version: "v0.1"
date: "2025-09-16_174208"
source_of_truth: "as-is"
---

# Operación / Cómo correr

Sigue estos pasos para ejecutar el flujo actualizado en el entorno Colab:

## 1. Configuración del Entorno

Asegúrate de tener todos los archivos especializados y el sistema de legacy automatizado configurados. Carga los archivos necesarios en tu entorno Colab.

```python
# Cargar archivos necesarios
from google.colab import files
uploaded = files.upload()
```

## 2. Seleccionar Proyecto

Utiliza el snippet `select_project` para elegir el proyecto adecuado. Asegúrate de que el proyecto esté actualizado con los timestamps correctos.

```python
select_project('nombre_del_proyecto')
```

## 3. Asegurar Catálogo

Ejecuta `ensure_catalog` para verificar que todos los archivos y datos requeridos estén presentes y en el formato correcto.

```python
ensure_catalog()
```

## 4. Ejecutar Índice

Corre el snippet `run_index` para iniciar el proceso de indexación. Este paso es crucial para el funcionamiento del sistema automatizado.

```python
run_index()
```

## Aclaraciones

- **Flags Temporales**: Asegúrate de establecer los flags temporales según sea necesario para evitar conflictos en la ejecución.
- **Límites Actuales**: Ten en cuenta que el sistema tiene límites en la cantidad de datos procesados por ejecución. Revisa la documentación para más detalles.

## 5. Verificación de Resultados

Después de ejecutar el índice, verifica los resultados generados para asegurarte de que todo esté funcionando correctamente.

```python
# Comprobar resultados
check_results()
```

Sigue estos pasos para garantizar una ejecución fluida y efectiva del flujo actualizado.

## 🛠️ Troubleshooting
- Revisa claves/entorno (`SB_SECRET`, `MONGO_URI`, `OPENAI_API_KEY`).
- Si falla Drive: re-montar y reintentar.
- Si hay columnas faltantes en DF: valida `normalize` y utilidades.
- Conflictos `ON CONFLICT`: alinea índices únicos.
- UI: si Streamlit no carga, valida versión de `streamlit` y puertos.