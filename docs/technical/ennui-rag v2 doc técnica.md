# ennui-rag · Documentación Técnica Completa

## 📋 Resumen Ejecutivo

**ennui-rag** es un sistema RAG (Retrieval-Augmented Generation) avanzado diseñado para la indexación, enriquecimiento y búsqueda inteligente de documentos almacenados en Google Drive. El sistema implementa un pipeline completo que va desde la extracción de metadatos hasta la generación de respuestas contextualizadas mediante IA, con persistencia robusta en múltiples bases de datos.

### 🎯 Propósito Principal
- **Indexación Inteligente**: Escaneo recursivo de carpetas de Google Drive con soporte para Shortcuts y Shared Drives
- **Enriquecimiento de Datos**: Extracción de contenido textual, generación de embeddings y metadatos enriquecidos
- **Búsqueda Semántica**: Sistema de búsqueda híbrida que combina búsqueda lexical y semántica
- **Persistencia Idempotente**: Almacenamiento confiable en Supabase y MongoDB con prevención de duplicados

### 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Google Drive  │───▶│   Indexación     │───▶│   Persistencia  │
│   (Fuente)      │    │   & Traversal    │    │   (Supabase/    │
└─────────────────┘    └──────────────────┘    │    MongoDB)      │
                                               └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Interfaz      │◀───│   Búsqueda       │◀───│   Enriquecimiento│
│   Streamlit     │    │   & Reranking    │    │   & Embeddings  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## 🔧 Módulos y Componentes Principales

### 1. **Configuración y Settings** (`src/ennui_rag/settings.py`)

#### Clase `Env`
```python
class Env(BaseSettings):
    OPENAI_API_KEY: str | None = None
    SB_SECRET: str | None = None
    SB_PASSWORD: str | None = None
    SUPABASE_REF: str | None = None
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None
    POSTGRES_DSN: str | None = None
    SUPABASE_CLIENT: object | None = None
    MONGO_URI: str | None = None
    MONGO_CLIENT: object | None = None
```

**Descripción Enriquecida**: La clase `Env` actúa como el centro de configuración del sistema, implementando un patrón de configuración centralizada que gestiona credenciales de múltiples servicios (OpenAI, Supabase, MongoDB) de manera segura. Utiliza Pydantic para validación automática de tipos y carga configuración desde variables de entorno y archivos YAML, garantizando flexibilidad en diferentes entornos de despliegue.

#### Funciones de Configuración

**`get_config(env: str = "dev") -> Tuple[Env, Dict[str, Any]]`**
- **Propósito**: Inicializa la configuración completa del sistema
- **Parámetros**: `env` - Entorno de ejecución (dev/prod)
- **Retorna**: Tupla con variables de entorno validadas y configuración YAML
- **Descripción Enriquecida**: Esta función implementa el patrón Factory para la configuración, cargando automáticamente credenciales, inicializando clientes de base de datos y mezclando configuraciones base con específicas del entorno. Incluye manejo robusto de errores y logging detallado para facilitar el debugging.

**`_init_supabase(env_vars: Env)`**
- **Propósito**: Configura e inicializa el cliente de Supabase
- **Descripción Enriquecida**: Implementa la inicialización lazy del cliente Supabase, construyendo automáticamente URLs y validando credenciales. Incluye fallback graceful si las credenciales no están disponibles.

**`_init_postgres(env_vars: Env)`**
- **Propósito**: Configura la cadena de conexión PostgreSQL
- **Descripción Enriquecida**: Construye dinámicamente el DSN de PostgreSQL usando el ref de Supabase y la contraseña, permitiendo conexión directa a la base de datos subyacente.

**`_init_mongo(env_vars: Env)`**
- **Propósito**: Inicializa el cliente MongoDB opcional
- **Descripción Enriquecida**: Configura MongoDB como almacén secundario, implementando el patrón de persistencia dual para mayor robustez y flexibilidad.

---

### 2. **Pipeline de Indexación** (`src/ennui_rag/pipelines/`)

#### `index_pipeline.py`

**`run_index(env: str = "dev", folder_id: Optional[str] = None, max_items: Optional[int] = None, stores: Optional[List] = None, save_csv: bool = True, always_persist: bool = True) -> pd.DataFrame`**

- **Propósito**: Pipeline principal de indexación de Google Drive
- **Parámetros**:
  - `env`: Entorno de configuración
  - `folder_id`: ID de la carpeta raíz a indexar
  - `max_items`: Límite de elementos a procesar
  - `stores`: Lista de almacenes de persistencia
  - `save_csv`: Si guardar el catálogo en CSV
  - `always_persist`: Si persistir automáticamente en BD
- **Retorna**: DataFrame con metadatos indexados
- **Descripción Enriquecida**: Esta función implementa el patrón Pipeline para el procesamiento de datos, orquestando la indexación completa desde la extracción de metadatos hasta la persistencia. Incluye manejo de errores robusto, logging detallado y soporte para procesamiento por lotes. La función es idempotente, permitiendo re-ejecuciones seguras sin duplicar datos.

#### `project_pipeline.py`

**`select_project(folder_id: str) -> dict`**
- **Propósito**: Selecciona y configura un proyecto activo
- **Parámetros**: `folder_id` - ID de la carpeta del proyecto
- **Retorna**: Diccionario con metadatos del proyecto
- **Descripción Enriquecida**: Implementa el patrón State para la gestión de proyectos, creando y actualizando metadatos de sesión. Mantiene un registro de proyectos recientes y facilita la navegación entre diferentes proyectos.

**`ensure_catalog(project_id: str, force: bool = False, max_items: int | None = None, persist: bool = True) -> str`**
- **Propósito**: Asegura que existe un catálogo para el proyecto
- **Parámetros**:
  - `project_id`: ID del proyecto
  - `force`: Forzar re-indexación
  - `max_items`: Límite de elementos
  - `persist`: Si persistir en BD
- **Retorna**: Ruta al archivo CSV del catálogo
- **Descripción Enriquecida**: Implementa el patrón Lazy Loading para catálogos, reutilizando catálogos existentes cuando es posible y generando nuevos solo cuando es necesario. Incluye validación de integridad y metadatos de sesión.

**`project_status(project_id: str) -> dict`**
- **Propósito**: Obtiene el estado actual del proyecto
- **Retorna**: Diccionario con estadísticas del proyecto
- **Descripción Enriquecida**: Proporciona una vista consolidada del estado del proyecto, incluyendo conteos de archivos, fechas de última modificación y estado de las bases de datos. Implementa el patrón Observer para monitoreo en tiempo real.

**`list_recent_projects(limit: int = 10) -> list[dict]`**
- **Propósito**: Lista proyectos recientes ordenados por fecha
- **Descripción Enriquecida**: Implementa un sistema de historial de proyectos con ordenamiento temporal, facilitando la navegación y el acceso rápido a proyectos frecuentemente utilizados.

---

### 3. **Sistema de Indexación** (`src/ennui_rag/indexing/`)

#### `build.py`

**`build_catalog_dataframe(root_id: str, max_items: Optional[int] = None) -> pd.DataFrame`**
- **Propósito**: Construye el DataFrame principal del catálogo
- **Parámetros**:
  - `root_id`: ID de la carpeta raíz
  - `max_items`: Límite de elementos a procesar
- **Retorna**: DataFrame con metadatos de archivos
- **Descripción Enriquecida**: Implementa el patrón Builder para la construcción de catálogos, orquestando el recorrido del árbol de directorios y la normalización de datos. Incluye optimizaciones de memoria y procesamiento por lotes.

**`save_catalog_csv(df: pd.DataFrame, path: str = CSV_PATH) -> None`**
- **Propósito**: Guarda el catálogo en formato CSV
- **Descripción Enriquecida**: Implementa persistencia local eficiente con manejo de directorios y codificación UTF-8, asegurando compatibilidad con herramientas externas.

#### `traversal.py`

**`walk_drive_tree(svc, root_id: str, max_items: Optional[int] = None) -> List[Dict]`**
- **Propósito**: Recorre recursivamente el árbol de Google Drive
- **Parámetros**:
  - `svc`: Servicio de Google Drive
  - `root_id`: ID de la carpeta raíz
  - `max_items`: Límite de elementos
- **Retorna**: Lista de diccionarios con metadatos de archivos
- **Descripción Enriquecida**: Implementa un algoritmo DFS (Depth-First Search) optimizado para Google Drive, con soporte completo para Shortcuts y Shared Drives. Incluye manejo de paginación, logging de progreso y control de límites. El algoritmo es resiliente a errores de red y implementa retry automático.

#### `normalize.py`

**`normalize_df_to_records(df: pd.DataFrame, project_id: Optional[str] = None, session_id: Optional[str] = None, root_folder_id: Optional[str] = None) -> List[Dict]`**
- **Propósito**: Normaliza el DataFrame a registros para persistencia
- **Descripción Enriquecida**: Implementa el patrón Adapter para la normalización de datos, convirtiendo el formato interno del DataFrame a un formato estándar para persistencia. Incluye validación de tipos, limpieza de datos y enriquecimiento de metadatos.

---

### 4. **Sistema de Persistencia** (`src/ennui_rag/persistence/`)

#### `base.py`

**Clase `CatalogStore` (ABC)**
```python
class CatalogStore(ABC):
    @abstractmethod
    def prepare(self) -> None: ...
    @abstractmethod
    def upsert(self, records: Iterable[Dict[str, Any]], batch_size: int = 500) -> int: ...
```

**Descripción Enriquecida**: Implementa el patrón Strategy para la persistencia, definiendo una interfaz común para diferentes tipos de almacenes. Permite la extensión fácil del sistema con nuevos tipos de bases de datos sin modificar el código cliente.

**`persist_catalog_df(df: pd.DataFrame, stores: List[CatalogStore], batch_size: int = 500, deduplicate: bool = True, project_id: Optional[str] = None, session_id: Optional[str] = None, root_folder_id: Optional[str] = None) -> Dict[str, int]`**

- **Propósito**: Persiste el catálogo en múltiples almacenes
- **Parámetros**:
  - `df`: DataFrame a persistir
  - `stores`: Lista de almacenes de destino
  - `batch_size`: Tamaño de lote para procesamiento
  - `deduplicate`: Si eliminar duplicados
  - `project_id`, `session_id`, `root_folder_id`: Metadatos contextuales
- **Retorna**: Diccionario con conteos de registros procesados por almacén
- **Descripción Enriquecida**: Implementa el patrón Command para operaciones de persistencia, permitiendo la ejecución de operaciones complejas de manera atómica. Incluye deduplicación inteligente, sanitización de datos y manejo de errores robusto.

#### `supabase.py`

**Clase `SupabaseStore`**
```python
class SupabaseStore(CatalogStore):
    def __init__(self, client: Client, table: str = "catalog_drive", on_conflict: str = "project_id,file_id,drive_id")
    def prepare(self) -> None
    def upsert(self, records: Iterable[Dict[str, Any]], batch_size: int = 500) -> int
    def select_all(self, limit: Optional[int] = None) -> List[Dict[str, Any]]
    def select_by_project(self, project_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]
    def select_by_ids(self, file_ids: List[str], drive_id: Optional[str] = None) -> List[Dict[str, Any]]
    def count(self) -> int
    def count_by_project(self, project_id: str) -> int
```

**Descripción Enriquecida**: Implementa un almacén de datos robusto para Supabase, con soporte completo para operaciones CRUD y consultas complejas. Incluye manejo de conflictos de clave primaria, deduplicación intra-lote y logging detallado. La implementación es altamente optimizada para grandes volúmenes de datos.

---

### 5. **Sistema de Enriquecimiento** (`src/ennui_rag/enrichment/`)

#### `extractors.py`

**Clase `SnippetExtractor` (ABC)**
```python
class SnippetExtractor(ABC):
    name: str = "base"
    def matches(self, row: FileRow) -> bool
    def extract(self, drive: Any, row: FileRow, *, max_chars: int, head_max_lines: int, head_max_bytes: int, bytes_chunk: int) -> SnippetResult
```

**Descripción Enriquecida**: Implementa el patrón Strategy para la extracción de contenido, permitiendo diferentes estrategias según el tipo de archivo. Cada extractor está optimizado para tipos específicos de archivos y utiliza las APIs más apropiadas para cada caso.

**Extractores Especializados**:

- **`GDocExtractor`**: Extrae contenido completo de Google Docs usando la API de exportación
- **`SheetCsvExtractor`**: Procesa Google Sheets y archivos CSV con muestreo inteligente
- **`ExcelExtractor`**: Maneja archivos Excel con análisis de estructura y contenido
- **`TextLikeExtractor`**: Procesa archivos de texto plano con múltiples formatos

**`get_snippet(drive: Any, row: FileRow, *, max_chars: int = 1200, head_max_lines: int = HEAD_MAX_LINES_DEFAULT, head_max_bytes: int = HEAD_MAX_BYTES_DEFAULT, bytes_chunk: int = BYTES_CHUNK_DEFAULT, extractors: Optional[List[SnippetExtractor]] = None) -> SnippetResult`**

- **Propósito**: Orquesta la extracción de contenido usando múltiples extractores
- **Descripción Enriquecida**: Implementa el patrón Chain of Responsibility para la extracción de contenido, probando extractores en orden de prioridad hasta encontrar uno que funcione. Incluye manejo de errores graceful y fallback automático.

---

### 6. **Sistema de Búsqueda** (`src/ennui_rag/search/`)

#### `search.py`

**`search_llm(query: str, project_id: str, *, data_dir: Path | None = None, k: int = 40, n: int = 12, kind: Optional[str] = None, use_embeddings: bool = False, q_vec = None, by_path: str | None = None, by_mime: str | None = None, modified_from: str | None = None, modified_to: str | None = None, as_answer: bool = False, answer_k: int = 5, debug: bool = False, return_candidates: bool = False) -> pd.DataFrame | dict`**

- **Propósito**: Sistema de búsqueda híbrida con reranking por LLM
- **Parámetros**:
  - `query`: Consulta de búsqueda
  - `project_id`: ID del proyecto a buscar
  - `k`: Número de candidatos a recuperar
  - `n`: Número de resultados finales
  - `use_embeddings`: Si usar búsqueda semántica
  - `as_answer`: Si devolver respuesta generada
- **Retorna**: DataFrame con resultados o diccionario con respuesta
- **Descripción Enriquecida**: Implementa un sistema de búsqueda híbrida que combina búsqueda lexical tradicional con búsqueda semántica basada en embeddings. Incluye reranking inteligente usando LLM, filtros avanzados y generación de respuestas contextualizadas. El sistema es altamente configurable y optimizado para diferentes casos de uso.

---

### 7. **Interfaz de Usuario** (`src/ennui_rag/app/`)

#### `ui_streamlit.py`

**Funciones Principales**:
- **`main()`**: Función principal de la aplicación Streamlit
- **`render_sidebar()`**: Renderiza la barra lateral con navegación
- **`render_main_content()`**: Renderiza el contenido principal según la sección activa

**Descripción Enriquecida**: Implementa una interfaz de usuario moderna y responsiva usando Streamlit, con navegación por pestañas y componentes modulares. La interfaz incluye paneles especializados para indexación, enriquecimiento, búsqueda y gestión de estado. Implementa el patrón MVC (Model-View-Controller) para separación clara de responsabilidades.

---

### 8. **Entrada/Salida** (`src/ennui_rag/io/`)

#### `drive_io.py`

**`get_drive_service()`**
- **Propósito**: Inicializa el servicio de Google Drive
- **Descripción Enriquecida**: Configura la autenticación OAuth2 con Google Drive usando credenciales de service account, implementando el patrón Singleton para reutilización eficiente de conexiones.

**`get_file_meta(service, file_id: str) -> Dict`**
- **Propósito**: Obtiene metadatos de un archivo específico
- **Descripción Enriquecida**: Implementa retry automático con backoff exponencial para manejar limitaciones de rate de la API de Google Drive.

**`list_children(service, folder_id: str, page_token: Optional[str] = None) -> Tuple[List[Dict], Optional[str]]`**
- **Propósito**: Lista archivos hijos de una carpeta con paginación
- **Descripción Enriquecida**: Implementa paginación eficiente para manejar carpetas con muchos archivos, incluyendo soporte para Shared Drives y filtros de trashed files.

---

## 🔄 Flujos de Trabajo Principales

### 1. **Flujo de Indexación**
```
Google Drive → Traversal → Normalización → Persistencia → CSV Local
     ↓              ↓            ↓             ↓
  Metadatos    Estructura    Validación    Múltiples BD
```

### 2. **Flujo de Enriquecimiento**
```
CSV Local → Extracción → LLM Processing → Embeddings → Persistencia
    ↓           ↓             ↓              ↓
  Archivos   Contenido    Descripciones   Vectores
```

### 3. **Flujo de Búsqueda**
```
Query → Retrieval → Reranking → Answer Generation
  ↓        ↓           ↓              ↓
Usuario  Candidatos  LLM Score    Respuesta
```

---

## 🛠️ Patrones de Diseño Implementados

1. **Factory Pattern**: Configuración y creación de clientes de BD
2. **Strategy Pattern**: Extractores de contenido y almacenes de persistencia
3. **Observer Pattern**: Monitoreo de estado de proyectos
4. **Command Pattern**: Operaciones de persistencia
5. **Chain of Responsibility**: Extracción de contenido
6. **Singleton Pattern**: Servicios de Google Drive
7. **Builder Pattern**: Construcción de catálogos
8. **Adapter Pattern**: Normalización de datos

---

## 📊 Métricas y Monitoreo

El sistema incluye métricas detalladas para:
- **Indexación**: Elementos procesados, tiempo de ejecución, errores
- **Persistencia**: Registros insertados/actualizados por almacén
- **Búsqueda**: Tiempo de respuesta, precisión de resultados
- **Enriquecimiento**: Archivos procesados, calidad de extracción

---

## 🚀 Características Avanzadas

1. **Idempotencia**: Operaciones seguras para re-ejecución
2. **Deduplicación**: Prevención de registros duplicados
3. **Retry Automático**: Manejo robusto de errores de red
4. **Procesamiento por Lotes**: Optimización de memoria y rendimiento
5. **Filtros Avanzados**: Búsqueda por tipo, fecha, ruta, MIME
6. **Búsqueda Híbrida**: Combinación de lexical y semántica
7. **Interfaz Modular**: Componentes reutilizables y extensibles

---

## 📈 Escalabilidad y Rendimiento

- **Procesamiento Asíncrono**: Para operaciones de I/O intensivas
- **Caché Inteligente**: Reutilización de catálogos existentes
- **Paginación Eficiente**: Manejo de grandes volúmenes de datos
- **Compresión**: Optimización de almacenamiento
- **Índices Optimizados**: Consultas rápidas en bases de datos

---

*Documento generado automáticamente con enriquecimiento de IA - ennui-rag v0.1.0*
