---
title: "Arquitectura y Flujo - Snapshot 2025-09-16_174208"
project: "ennui-rag"
doc_type: "kb"
version: "v0.1"
date: "2025-09-16_174208"
source_of_truth: "as-is"
---

# Arquitectura y Flujo

La arquitectura del sistema Ennui-RAG se organiza en varias capas que facilitan la modularidad y la escalabilidad:

1. **Indexing**: Esta capa se encarga de la organización y búsqueda eficiente de datos. Utiliza índices para optimizar el acceso a la información.

2. **Pipelines**: Los pipelines procesan los datos desde su origen hasta su destino. Incluyen transformaciones y validaciones necesarias para asegurar la calidad de los datos.

3. **I/O**: La capa de entrada/salida maneja la interacción con fuentes externas, como Google Drive, y la lectura/escritura de archivos CSV. 

4. **Persistence**: Aquí se gestionan las bases de datos, utilizando SQLAlchemy para la conexión y manipulación de datos en MariaDB. La configuración de la base de datos se encuentra en `database/config.py`, donde se definen los parámetros de conexión.

5. **Settings**: Esta capa incluye configuraciones globales y específicas del entorno, permitiendo la personalización del comportamiento del sistema.

6. **App/UI**: La interfaz de usuario se implementa con Streamlit, proporcionando una forma interactiva de visualizar y manipular datos. La UI se integra con los modelos de datos y permite a los usuarios realizar consultas y visualizar resultados en tiempo real.

El flujo de datos sigue el siguiente camino: **Drive → DataFrame (DF) → CSV → Records → Stores**. Los datos se extraen de Google Drive, se transforman en DataFrames, se guardan como archivos CSV y, finalmente, se almacenan en la base de datos.

Recientemente, se ha automatizado el sistema de legacy, permitiendo una gestión más eficiente de las versiones de conocimiento (KB) y facilitando la actualización de la documentación. Esto se refleja en el README actualizado, que ahora incluye timestamps y archivos especializados, mejorando la trazabilidad y el acceso a la información.