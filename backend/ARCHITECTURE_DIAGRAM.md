# Arquitectura del Sistema de Indexación

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Streamlit)                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Program UI    │  │  Search UI      │  │  Stats UI       │ │
│  │                 │  │                 │  │                 │ │
│  │ - Create Program│  │ - Search Files  │  │ - View Stats    │ │
│  │ - Start Indexing│  │ - Filter by Type│  │ - Monitor Jobs  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/API Calls
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Backend API (FastAPI)                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Program Router │  │ Indexing Router │  │   Auth Router   │ │
│  │                 │  │                 │  │                 │ │
│  │ - CRUD Programs │  │ - Start Scan    │  │ - JWT Auth      │ │
│  │ - Manage Access │  │ - Monitor Jobs  │  │ - Google OAuth  │ │
│  │ - Check Drive   │  │ - Search Files  │  │ - Session Mgmt  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Service Calls
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ IndexingService │  │ GoogleDriveAPI  │  │   AuthService   │ │
│  │                 │  │                 │  │                 │ │
│  │ - Manage Jobs   │  │ - Scan Folders  │  │ - Validate JWT  │ │
│  │ - Process Files │  │ - Download Files│  │ - Google OAuth  │ │
│  │ - Search Content│  │ - Export Docs   │  │ - Check Perms   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Database Operations
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Database Layer                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Programs      │  │  IndexedFiles   │  │  IndexingJobs   │ │
│  │                 │  │                 │  │                 │ │
│  │ - Program Info  │  │ - File Metadata │  │ - Job Status    │ │
│  │ - Drive Folder  │  │ - Content Text  │  │ - Progress      │ │
│  │ - Access Control│  │ - File Hash     │  │ - Error Logs    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │     Users       │  │  ProgramAccess  │  │  UserSessions   │ │
│  │                 │  │                 │  │                 │ │
│  │ - User Info     │  │ - Permissions   │  │ - JWT Tokens    │ │
│  │ - Google Tokens │  │ - Roles         │  │ - Session Data  │ │
│  │ - Auth Data     │  │ - Active Status │  │ - Expiration    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ OAuth2 API Calls
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Google Drive   │  │  Google OAuth   │  │  Google APIs    │ │
│  │     API         │  │     Service     │  │                 │ │
│  │                 │  │                 │  │                 │ │
│  │ - List Files    │  │ - Get Tokens    │  │ - Drive v3      │ │
│  │ - Download      │  │ - Refresh Tokens│  │ - OAuth2        │ │
│  │ - Export Docs   │  │ - Validate      │  │ - Discovery     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Indexación

```
1. Usuario inicia indexación
   │
   ▼
2. Frontend → API: POST /indexing/scan
   │
   ▼
3. API valida permisos y crea IndexingJob
   │
   ▼
4. IndexingService inicia trabajo en background
   │
   ▼
5. GoogleDriveScanner escanea carpeta recursivamente
   │
   ▼
6. Para cada archivo:
   ├─ Descargar/Exportar contenido
   ├─ Extraer texto
   ├─ Calcular hash
   └─ Guardar en IndexedFile
   │
   ▼
7. Actualizar progreso en IndexingJob
   │
   ▼
8. Marcar trabajo como completado
```

## Flujo de Búsqueda

```
1. Usuario busca archivos
   │
   ▼
2. Frontend → API: POST /indexing/search
   │
   ▼
3. API valida permisos
   │
   ▼
4. IndexingService busca en IndexedFile
   ├─ Filtrar por programa
   ├─ Buscar en nombre y contenido
   ├─ Aplicar filtros de tipo
   └─ Paginar resultados
   │
   ▼
5. Retornar resultados al frontend
```

## Modelos de Datos

### IndexedFile
```sql
CREATE TABLE indexed_files (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    drive_file_id VARCHAR UNIQUE NOT NULL,
    drive_file_name VARCHAR NOT NULL,
    drive_file_path VARCHAR,
    mime_type VARCHAR NOT NULL,
    file_type VARCHAR NOT NULL,
    file_size INTEGER DEFAULT 0,
    web_view_link VARCHAR,
    content_text TEXT,
    content_hash VARCHAR,
    is_google_doc BOOLEAN DEFAULT FALSE,
    is_downloadable BOOLEAN DEFAULT TRUE,
    indexing_status VARCHAR DEFAULT 'pending',
    indexing_error VARCHAR,
    last_indexed_at TIMESTAMP,
    drive_created_time TIMESTAMP,
    drive_modified_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### IndexingJob
```sql
CREATE TABLE indexing_jobs (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    user_id INTEGER REFERENCES users(id),
    job_type VARCHAR NOT NULL,
    folder_id VARCHAR,
    status VARCHAR DEFAULT 'pending',
    total_files INTEGER DEFAULT 0,
    processed_files INTEGER DEFAULT 0,
    successful_files INTEGER DEFAULT 0,
    failed_files INTEGER DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

## Seguridad

1. **Autenticación JWT**: Todos los endpoints requieren token válido
2. **Autorización**: Verificación de permisos por programa
3. **Google OAuth**: Tokens seguros para acceso a Drive
4. **Validación de Entrada**: Sanitización de queries de búsqueda
5. **Rate Limiting**: Protección contra abuso de API
6. **Logging**: Auditoría de todas las operaciones

## Escalabilidad

1. **Procesamiento Asíncrono**: Indexación en background
2. **Paginación**: Resultados limitados para evitar timeouts
3. **Caché**: Hash de contenido para evitar re-procesamiento
4. **Índices de BD**: Optimización de consultas de búsqueda
5. **Monitoreo**: Seguimiento de progreso y errores
