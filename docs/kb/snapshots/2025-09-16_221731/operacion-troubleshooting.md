---
title: "Operación y Troubleshooting - Snapshot 2025-09-16_221731"
project: "ennui-rag"
doc_type: "kb"
version: "v0.1"
date: "2025-09-16_221731"
source_of_truth: "as-is"
---

# Operación / Cómo correr

Para ejecutar la función `gen_kb` y realizar la comparación de los archivos que describen el sistema, sigue estos pasos:

## Pasos

1. **Selecciona el proyecto**:
   Asegúrate de que el proyecto correcto esté seleccionado en tu entorno de trabajo.

   ```python
   select_project('nombre_del_proyecto')
   ```

2. **Asegura el catálogo**:
   Verifica que el catálogo necesario esté disponible.

   ```python
   ensure_catalog('nombre_del_catalogo')
   ```

3. **Ejecuta la comparación**:
   Llama a la función `gen_kb` con los parámetros adecuados. Puedes utilizar flags temporales para ajustar la ejecución según tus necesidades.

   ```python
   gen_kb(comparar_archivos=True, flags_temporales={'limite': 100})
   ```

   - **Flags temporales**: Puedes ajustar el límite de comparación mediante el parámetro `limite`. El valor predeterminado es 100, pero puedes modificarlo según el tamaño de los archivos.

4. **Revisa los resultados**:
   Después de ejecutar la función, verifica los resultados de la comparación para asegurarte de que se haya realizado correctamente.

## Notas

- Asegúrate de que los archivos que describen el sistema estén en el formato correcto para evitar errores durante la comparación.
- Si encuentras problemas, revisa los logs generados para identificar posibles inconsistencias.

## 🛠️ Troubleshooting
- Revisa claves/entorno (`SB_SECRET`, `MONGO_URI`, `OPENAI_API_KEY`).
- Si falla Drive: re-montar y reintentar.
- Si hay columnas faltantes en DF: valida `normalize` y utilidades.
- Conflictos `ON CONFLICT`: alinea índices únicos.
- UI: si Streamlit no carga, valida versión de `streamlit` y puertos.