---
title: "Arquitectura y Flujo - Snapshot 2025-09-16_221731"
project: "ennui-rag"
doc_type: "kb"
version: "v0.1"
date: "2025-09-16_221731"
source_of_truth: "as-is"
---

## Arquitectura y flujo

La arquitectura del sistema Ennui-RAG se organiza en varias capas que facilitan la modularidad y el mantenimiento:

1. **Indexing**: Esta capa se encarga de la creación y gestión de índices para optimizar la búsqueda y recuperación de datos. Utiliza modelos y utilidades específicas para transformar datos en estructuras indexadas.

2. **Pipelines**: Los pipelines son responsables de orquestar el flujo de datos a través de diferentes etapas de procesamiento, desde la ingesta hasta la persistencia. Incluyen procesos como enriquecimiento y almacenamiento en bases de datos.

3. **IO (Input/Output)**: Esta capa maneja la interacción con fuentes externas, como Google Drive y bases de datos. Facilita la lectura y escritura de archivos, así como la comunicación con APIs.

4. **Persistence**: Aquí se gestionan las operaciones de almacenamiento de datos, utilizando SQLAlchemy para interactuar con la base de datos MariaDB. La configuración y conexión se manejan a través del módulo `config.py`.

5. **Settings**: Contiene configuraciones generales del sistema, como variables de entorno y parámetros de conexión a la base de datos.

6. **App/UI**: La interfaz de usuario se implementa con Streamlit, permitiendo a los usuarios interactuar con el sistema de manera intuitiva. La UI se conecta a las capas anteriores para mostrar datos y resultados procesados.

### Flujo de Datos

El flujo de datos sigue el siguiente recorrido: **Drive → DataFrame (DF) → CSV → Records → Stores**. Los archivos se extraen de Google Drive, se convierten en DataFrames para su procesamiento, se exportan a CSV y, finalmente, se almacenan en la base de datos.

### Configuración y Clientes

La configuración del sistema reside en el módulo `config.py`, donde se definen las credenciales y parámetros de conexión. Los clientes, como los modelos de SQLAlchemy, se importan desde el paquete `database`, permitiendo una fácil integración y uso en diferentes partes del sistema.

Este diseño modular y el flujo de datos optimizado permiten una fácil escalabilidad y mantenimiento, alineándose con las actualizaciones recientes en el sistema.