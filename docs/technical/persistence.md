# Actualización de Persistencia: Supabase como Fuente Principal

## Resumen de Cambios

Esta actualización modifica el sistema para que **siempre se haga persistencia** y **siempre se lean los datos desde Supabase** en lugar de archivos CSV locales (`catalog_base.csv`), incluyendo **datos enriquecidos** (`enriched_files` y `enriched_folders`).

## Cambios Implementados

### 1. Nuevo Módulo de Lectura (`src/ennui_rag/persistence/reader.py`)

- **`read_catalog_from_supabase()`**: Lee el catálogo completo desde Supabase
- **`read_enriched_data_from_supabase()`**: Lee datos enriquecidos (archivos y carpetas) desde Supabase
- **`read_catalog_with_fallback()`**: Lee desde Supabase con fallback opcional a CSV
- **`get_supabase_status()`**: Obtiene el estado de los datos en Supabase

### 2. SupabaseStore Mejorado (`src/ennui_rag/persistence/supabase.py`)

Se agregaron nuevos métodos de lectura:
- **`select_all()`**: Lee todos los registros
- **`select_by_project()`**: Lee registros filtrados por project_id
- **`select_by_ids()`**: Lee registros filtrados por file_ids
- **`count()`**: Cuenta el total de registros
- **`count_by_project()`**: Cuenta registros por project_id

### 3. Pipeline de Indexación (`src/ennui_rag/pipelines/index_pipeline.py`)

- **`always_persist=True`** por defecto
- **Siempre** se hace persistencia en Supabase si hay credenciales disponibles
- Se eliminó la lógica condicional de persistencia

### 4. Pipeline de Enriquecimiento (`src/ennui_rag/pipelines/enrich_pipeline.py`)

- **`persist_supabase=True`** por defecto
- **`use_supabase=True`** por defecto
- Lee datos desde Supabase en lugar de CSV
- **Siempre** hace persistencia en Supabase

### 5. Pipeline de Proyecto (`src/ennui_rag/pipelines/project_pipeline.py`)

- **`persist=True`** por defecto
- **Siempre** usa persistencia automática

### 6. Loader de Búsqueda (`src/ennui_rag/search/loader.py`)

- **`use_supabase=True`** por defecto
- Nueva función **`load_corpus_from_supabase()`**
- Prioriza datos desde Supabase, con fallback a CSV

### 7. 🆕 Nuevos Pipelines de Supabase

#### Pipeline de Enriquecimiento con Supabase (`src/ennui_rag/pipelines/enrich_supabase_pipeline.py`)

- **`run_enrich_supabase()`**: Pipeline que SIEMPRE usa Supabase para lectura y persistencia
- **`enrich_existing_project()`**: Función de conveniencia para enriquecer proyectos existentes
- **SIEMPRE** lee desde Supabase y **SIEMPRE** persiste en Supabase
- No depende de archivos CSV locales

#### Pipeline de Proyecto con Supabase (`src/ennui_rag/pipelines/project_supabase_pipeline.py`)

- **`ensure_catalog_and_enrich_supabase()`**: Asegura catálogo e indexación, y SIEMPRE enriquece
- **`project_status_supabase()`**: Estado completo incluyendo datos enriquecidos desde Supabase
- **`reprocess_project_supabase()`**: Reprocesa proyecto completo usando Supabase
- **SIEMPRE** usa persistencia automática y enriquecimiento

## Cómo Funciona Ahora

### Antes (Comportamiento Anterior)
```python
# Los pipelines leían desde CSV local
df = pd.read_csv("catalog_base.csv")

# La persistencia era opcional
if stores:
    persist_catalog_df(df, stores, ...)

# Los datos enriquecidos se guardaban en CSV local
pd.DataFrame(files).to_csv("catalog_enriched_files.csv")
```

### Ahora (Nuevo Comportamiento)
```python
# Los pipelines leen desde Supabase por defecto
df = read_catalog_from_supabase(project_id)

# La persistencia SIEMPRE se hace
persist_catalog_df(df, stores, ...)  # stores se inicializa automáticamente

# Los datos enriquecidos SIEMPRE se persisten en Supabase
files_store.upsert(files, batch_size=500)  # Tabla enriched_files
folders_store.upsert(folders, batch_size=500)  # Tabla enriched_folders
```

## Uso de la Nueva Funcionalidad

### 1. Indexación Automática con Persistencia
```python
from ennui_rag.pipelines.index_pipeline import run_index

# Siempre hace persistencia automáticamente
df = run_index(
    env="dev",
    folder_id="your_folder_id",
    always_persist=True  # Por defecto
)
```

### 2. Enriquecimiento con Lectura desde Supabase
```python
from ennui_rag.pipelines.enrich_pipeline import run_enrich

# Lee desde Supabase y siempre persiste
result = run_enrich(
    env="dev",
    project_id="your_project_id",
    use_supabase=True,      # Por defecto
    persist_supabase=True,  # Por defecto
)
```

### 3. 🆕 Enriquecimiento SIEMPRE con Supabase
```python
from ennui_rag.pipelines import run_enrich_supabase

# SIEMPRE lee desde Supabase y SIEMPRE persiste en Supabase
result = run_enrich_supabase(
    env="dev",
    project_id="your_project_id",
    persist_supabase=True,  # Por defecto
)
```

### 4. 🆕 Pipeline Completo con Enriquecimiento Automático
```python
from ennui_rag.pipelines import ensure_catalog_and_enrich_supabase

# Asegura catálogo, indexación y SIEMPRE enriquece usando Supabase
result = ensure_catalog_and_enrich_supabase(
    project_id="your_project_id",
    persist=True,   # Siempre persistir
    enrich=True     # Siempre enriquecer
)
```

### 5. Lectura Directa desde Supabase
```python
from ennui_rag.persistence import read_catalog_from_supabase, read_enriched_data_from_supabase

# Leer catálogo desde Supabase
df = read_catalog_from_supabase("your_project_id")

# Leer datos enriquecidos desde Supabase
files_df, folders_df = read_enriched_data_from_supabase("your_project_id")
```

### 6. Carga de Corpus desde Supabase
```python
from ennui_rag.search.loader import load_corpus

# Carga desde Supabase por defecto
df = load_corpus("your_project_id", use_supabase=True)  # Por defecto
```

## Configuración Requerida

### Variables de Entorno
```bash
# Supabase (requerido para la nueva funcionalidad)
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"

# MongoDB (opcional)
export MONGO_URI="your_mongo_uri"
```

### Tablas de Supabase
- **`catalog_drive`**: Catálogo base de archivos y carpetas
- **`enriched_files`**: Archivos enriquecidos (SIEMPRE se persiste aquí)
- **`enriched_folders`**: Carpetas enriquecidas (SIEMPRE se persiste aquí)

## Scripts de Prueba

### Script Principal de Persistencia
`scripts/test_supabase_persistence.py` - Demuestra:
1. ✅ Persistencia automática en todos los pipelines
2. ✅ Lectura desde Supabase en lugar de CSV
3. ✅ Funcionamiento para index, enrich, y project pipelines

### 🆕 Script de Datos Enriquecidos
`scripts/test_enriched_supabase.py` - Demuestra:
1. ✅ Persistencia automática de datos enriquecidos en Supabase
2. ✅ Lectura de datos enriquecidos desde Supabase
3. ✅ Funcionamiento para archivos y carpetas enriquecidas
4. ✅ Pipeline completo con enriquecimiento automático

### Ejecutar Pruebas
```bash
# Prueba general de persistencia
cd scripts
python test_supabase_persistence.py

# Prueba específica de datos enriquecidos
python test_enriched_supabase.py
```

## Beneficios de la Actualización

1. **Persistencia Garantizada**: Los datos siempre se guardan en Supabase
2. **Fuente Única de Verdad**: Supabase es la fuente principal de datos
3. **Consistencia**: Todos los pipelines usan la misma fuente de datos
4. **Escalabilidad**: No hay dependencia de archivos CSV locales
5. **Colaboración**: Múltiples usuarios pueden acceder a los mismos datos
6. **Backup Automático**: Los datos están respaldados en la nube
7. **🆕 Datos Enriquecidos Centralizados**: Archivos y carpetas enriquecidas siempre en Supabase
8. **🆕 Enriquecimiento Automático**: Se puede configurar para que siempre enriquezca

## Migración

### Para Usuarios Existentes
- Los cambios son **retrocompatibles**
- Se puede deshabilitar Supabase con `use_supabase=False`
- Se puede deshabilitar persistencia con `persist_supabase=False`
- Los pipelines originales siguen funcionando

### Para Nuevos Usuarios
- La funcionalidad está habilitada por defecto
- Solo requiere configurar credenciales de Supabase
- No es necesario crear archivos CSV locales
- Los datos enriquecidos se persisten automáticamente

## Troubleshooting

### Error: "Supabase no está accesible"
- Verificar variables de entorno `SUPABASE_URL` y `SUPABASE_KEY`
- Verificar conectividad a internet
- Verificar que la tabla existe en Supabase

### Error: "No se encontraron datos en Supabase"
- Ejecutar primero el pipeline de indexación
- Verificar que el `project_id` sea correcto
- Verificar que la tabla tenga datos

### Error: "No se encontraron datos enriquecidos"
- Ejecutar primero el pipeline de enriquecimiento
- Verificar que las tablas `enriched_files` y `enriched_folders` existan
- Verificar que el enriquecimiento se haya completado exitosamente

### Fallback a CSV
- Si Supabase falla, el sistema puede caer a CSV local
- Esto se puede controlar con el parámetro `fallback_to_csv`

## Próximos Pasos

1. **Testing**: Probar la nueva funcionalidad en entorno de desarrollo
2. **Documentación**: Actualizar documentación de usuario
3. **Monitoreo**: Implementar métricas de uso de Supabase
4. **Optimización**: Mejorar rendimiento de consultas a Supabase
5. **🆕 Datos Enriquecidos**: Implementar monitoreo de calidad de enriquecimiento
6. **🆕 Pipeline Automático**: Configurar enriquecimiento automático en producción
