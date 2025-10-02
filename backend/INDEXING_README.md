# Sistema de Indexación de Google Drive

Este sistema permite indexar y buscar archivos de Google Drive para programas específicos, proporcionando capacidades de búsqueda de texto completo y gestión de contenido.

## Características Principales

- **Indexación Completa**: Escanea recursivamente carpetas de Google Drive
- **Soporte para Google Workspace**: Exporta documentos de Google Docs, Sheets, Slides, etc.
- **Búsqueda de Texto Completo**: Busca en nombres de archivos y contenido
- **Indexación Incremental**: Actualiza solo archivos modificados
- **Gestión de Trabajos**: Monitorea el progreso de indexación
- **Filtros por Tipo**: Filtra archivos por tipo (PDF, DOCX, etc.)
- **Estadísticas**: Proporciona estadísticas detalladas de archivos indexados

## Arquitectura

### Modelos de Base de Datos

#### IndexedFile
Almacena información de archivos indexados:
- `drive_file_id`: ID único del archivo en Google Drive
- `drive_file_name`: Nombre del archivo
- `mime_type`: Tipo MIME del archivo
- `file_type`: Tipo de archivo normalizado
- `content_text`: Contenido de texto extraído
- `content_hash`: Hash del contenido para detección de cambios
- `indexing_status`: Estado de indexación (pending, processing, completed, failed)

#### IndexingJob
Rastrea trabajos de indexación:
- `job_type`: Tipo de trabajo (full_scan, incremental, specific_folder)
- `status`: Estado del trabajo (pending, running, completed, failed, cancelled)
- `progress`: Contadores de progreso (total_files, processed_files, etc.)

### Servicios

#### GoogleDriveScanner
Clase principal para interactuar con Google Drive API:
- `scan_folder_recursive()`: Escanea carpetas recursivamente
- `get_file_content()`: Descarga contenido de archivos
- `export_google_doc()`: Exporta documentos de Google Workspace

#### IndexingService
Maneja la lógica de negocio de indexación:
- `start_indexing_job()`: Inicia un trabajo de indexación
- `search_files()`: Busca archivos indexados
- `get_program_files()`: Obtiene archivos de un programa

## API Endpoints

### Indexación

#### POST `/api/indexing/scan`
Inicia el escaneo e indexación de una carpeta.

**Request:**
```json
{
  "program_id": 1,
  "folder_id": "optional_folder_id",
  "include_trashed": false,
  "job_type": "full_scan"
}
```

**Response:**
```json
{
  "job_id": 123,
  "message": "Indexing job started for program 1",
  "status": "started"
}
```

#### GET `/api/indexing/status/{job_id}`
Obtiene el estado de un trabajo de indexación.

**Response:**
```json
{
  "job_id": 123,
  "status": "running",
  "progress": {
    "total_files": 100,
    "processed_files": 50,
    "successful_files": 45,
    "failed_files": 5
  },
  "error_message": null,
  "started_at": "2023-12-01T10:30:00Z",
  "completed_at": null
}
```

### Búsqueda

#### POST `/api/indexing/search`
Busca archivos indexados.

**Request:**
```json
{
  "program_id": 1,
  "query": "informe",
  "file_types": ["pdf", "google_doc"],
  "limit": 50
}
```

**Response:**
```json
{
  "files": [
    {
      "id": 1,
      "drive_file_id": "1ABC123",
      "drive_file_name": "Informe Final.pdf",
      "file_type": "pdf",
      "content_text": "Contenido del archivo...",
      "indexing_status": "completed"
    }
  ],
  "total_count": 1,
  "query": "informe"
}
```

#### GET `/api/indexing/files/{program_id}`
Obtiene archivos de un programa.

**Query Parameters:**
- `file_types`: Tipos de archivo separados por coma (opcional)
- `limit`: Límite de resultados (default: 100)

### Estadísticas

#### GET `/api/indexing/files/{program_id}/stats`
Obtiene estadísticas de archivos indexados.

**Response:**
```json
{
  "total_files": 100,
  "completed_files": 95,
  "failed_files": 5,
  "total_size_bytes": 1048576,
  "file_types": {
    "pdf": 30,
    "google_doc": 25,
    "docx": 20,
    "xlsx": 15,
    "pptx": 10
  },
  "last_updated": "2023-12-01T10:30:00Z"
}
```

## Configuración

### 1. Migración de Base de Datos

Ejecuta el script de migración para crear las nuevas tablas:

```bash
cd backend
python migrate_indexing.py
```

### 2. Autenticación con Google Drive

Los usuarios necesitan autenticarse con Google Drive para acceder a sus archivos. El sistema utiliza OAuth2 y almacena los tokens en la tabla `users`:

- `google_access_token`: Token de acceso OAuth2
- `google_refresh_token`: Token de actualización
- `google_token_expiry`: Fecha de expiración del token

### 3. Permisos de Programa

Los usuarios deben tener acceso al programa para poder indexar archivos. Los roles disponibles son:
- `owner`: Puede indexar y eliminar archivos
- `editor`: Puede indexar archivos
- `viewer`: Solo puede buscar archivos

## Uso

### 1. Indexación Completa

```python
# Iniciar indexación completa de un programa
scan_request = {
    "program_id": 1,
    "include_trashed": False,
    "job_type": "full_scan"
}

response = requests.post(
    f"{API_BASE}/indexing/scan",
    headers=headers,
    json=scan_request
)
```

### 2. Indexación Incremental

```python
# Indexar solo archivos modificados
scan_request = {
    "program_id": 1,
    "job_type": "incremental"
}
```

### 3. Búsqueda de Archivos

```python
# Buscar archivos por contenido
search_request = {
    "program_id": 1,
    "query": "informe anual",
    "file_types": ["pdf", "google_doc"],
    "limit": 20
}

response = requests.post(
    f"{API_BASE}/indexing/search",
    headers=headers,
    json=search_request
)
```

### 4. Monitoreo de Progreso

```python
# Verificar estado de indexación
response = requests.get(
    f"{API_BASE}/indexing/status/{job_id}",
    headers=headers
)

status = response.json()
print(f"Progreso: {status['progress']['processed_files']}/{status['progress']['total_files']}")
```

## Tipos de Archivo Soportados

### Google Workspace
- Google Docs (exportados como texto plano)
- Google Sheets (exportados como texto plano)
- Google Slides (exportados como texto plano)
- Google Forms
- Google Drawings

### Archivos Regulares
- PDF
- Microsoft Office (DOCX, XLSX, PPTX)
- Texto plano (TXT)
- CSV
- JSON
- HTML
- Imágenes (JPEG, PNG, GIF)
- ZIP

## Limitaciones

1. **Tamaño de Archivos**: Archivos muy grandes pueden causar timeouts
2. **Rate Limits**: Google Drive API tiene límites de velocidad
3. **Contenido**: Solo se indexa contenido de texto (no imágenes o videos)
4. **Permisos**: Requiere permisos de lectura en Google Drive

## Monitoreo y Debugging

### Logs
El sistema registra información detallada en los logs:
- Inicio y finalización de trabajos
- Errores de procesamiento de archivos
- Estadísticas de progreso

### Estados de Indexación
- `pending`: Archivo en cola para procesar
- `processing`: Archivo siendo procesado
- `completed`: Archivo indexado exitosamente
- `failed`: Error al procesar archivo

### Estados de Trabajo
- `pending`: Trabajo en cola
- `running`: Trabajo en ejecución
- `completed`: Trabajo completado
- `failed`: Trabajo fallido
- `cancelled`: Trabajo cancelado

## Ejemplos

Ver `backend/apps/indexing_example.py` para ejemplos completos de uso del sistema.

## Troubleshooting

### Error: "Google Drive access token required"
- El usuario necesita autenticarse con Google Drive
- Verificar que el token no haya expirado

### Error: "No access to this program"
- El usuario no tiene permisos para acceder al programa
- Verificar roles de acceso en la tabla `program_access`

### Error: "Invalid or expired access token"
- El token de Google Drive ha expirado
- El usuario necesita reautenticarse

### Archivos no se indexan
- Verificar permisos en Google Drive
- Revisar logs para errores específicos
- Verificar que el archivo no esté en papelera (si `include_trashed=False`)
