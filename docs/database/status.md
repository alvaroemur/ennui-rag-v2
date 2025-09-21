    # DB_STATUS · Auto-generado

- Tablas: **62**
- Filas aproximadas: **9,936**

## public.application

- Filas: **-1**

> La tabla 'application' almacena las solicitudes de los usuarios, vinculándose con las tablas 'cohort' y 'organization' a través de las claves foráneas 'cohort_id' y 'organization_id'. Cada solicitud tiene un estado y una marca de tiempo de envío.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único de la solicitud. |
| 2 | `cohort_id` | uuid | NO |  | Identificador del grupo al que pertenece la solicitud (FK a 'cohort'). |
| 3 | `organization_id` | uuid | NO |  | Identificador de la organización que realiza la solicitud (FK a 'organization'). |
| 4 | `status` | text | YES | 'submitted'::text | Estado actual de la solicitud, por defecto 'submitted'. |
| 5 | `submitted_at` | timestamp with time zone | YES | now() | Fecha y hora en que se envió la solicitud. |
| 6 | `payload_json` | jsonb | YES | '{}'::jsonb | Datos adicionales de la solicitud en formato JSON. |

## public.assignment

- Filas: **-1**

> La tabla 'assignment' almacena asignaciones relacionadas con requisitos, personas y organizaciones. Contiene claves foráneas que referencian a las tablas 'requirement', 'person' y 'organization'.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único de la asignación. |
| 2 | `requirement_id` | uuid | NO |  | Identificador del requisito asociado a la asignación. |
| 3 | `subject_person_id` | uuid | YES |  | Identificador de la persona sujeta a la asignación (opcional). |
| 4 | `subject_org_id` | uuid | YES |  | Identificador de la organización sujeta a la asignación (opcional). |
| 5 | `status` | text | YES | 'assigned'::text | Estado actual de la asignación, por defecto 'assigned'. |
| 6 | `created_at` | timestamp with time zone | NO | now() | Fecha y hora de creación de la asignación. |

## public.attendance

- Filas: **-1**

> La tabla 'attendance' registra la asistencia de personas a sesiones, vinculando cada entrada a un 'person_id' y un 'session_id'. Esto permite rastrear la participación de individuos en eventos específicos.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único de la asistencia. |
| 2 | `session_id` | uuid | NO |  | Identificador de la sesión a la que se asiste, referencia a la tabla 'session'. |
| 3 | `person_id` | uuid | NO |  | Identificador de la persona que asiste, referencia a la tabla 'person'. |
| 4 | `status` | text | NO | 'present'::text | Estado de la asistencia, por defecto es 'present'. |
| 5 | `check_in_at` | timestamp with time zone | YES |  | Marca de tiempo opcional que indica cuándo se registró la asistencia. |
| 6 | `created_at` | timestamp with time zone | NO | now() | Marca de tiempo que indica cuándo se creó el registro de asistencia. |

## public.california

- Filas: **3,000**

> La tabla 'california' almacena información sobre propiedades en California, incluyendo el número total de habitaciones. No tiene claves foráneas, lo que indica que no se relaciona directamente con otras tablas.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | bigint | NO |  | Identificador único de la propiedad. |
| 2 | `total_rooms` | real | NO |  | Número total de habitaciones en la propiedad. |

## public.catalog_drive

- Filas: **3,832**

> La tabla 'catalog_drive' almacena información sobre archivos en un sistema de almacenamiento, incluyendo detalles como el identificador del archivo, su nombre y ruta relativa. Esta tabla puede relacionarse con otras a través de campos como 'project_id' y 'session_id'.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `file_id` | text | NO |  | Identificador único del archivo. |
| 2 | `drive_id` | text | NO |  | Identificador del disco o unidad donde se encuentra el archivo. |
| 3 | `name` | text | YES |  | Nombre del archivo. |
| 4 | `relative_path` | text | YES |  | Ruta relativa del archivo dentro del sistema. |
| 5 | `type` | text | YES |  | Tipo de archivo (por ejemplo, documento, imagen). |
| 6 | `mime_type` | text | YES |  | Tipo MIME del archivo. |
| 7 | `size_bytes` | bigint | YES |  | Tamaño del archivo en bytes. |
| 8 | `modified` | timestamp with time zone | YES |  | Fecha y hora de la última modificación del archivo. |
| 9 | `owner` | text | YES |  | Propietario del archivo. |
| 10 | `web_url` | text | YES |  | URL para acceder al archivo en la web. |
| 11 | `extension` | text | YES |  | Extensión del archivo (por ejemplo, .txt, .jpg). |
| 12 | `indexed_at` | timestamp with time zone | YES | now() | Fecha y hora en que se indexó el archivo. |
| 13 | `project_id` | text | YES |  | Identificador del proyecto asociado al archivo. |
| 14 | `session_id` | text | YES |  | Identificador de la sesión relacionada con el archivo. |
| 15 | `root_folder_id` | text | YES |  | Identificador de la carpeta raíz donde se encuentra el archivo. |

## public.cohort

- Filas: **-1**

> La tabla 'cohort' almacena información sobre cohortes asociadas a programas específicos, identificadas por un ID único. Tiene una relación de clave foránea con la tabla 'program', referenciando el 'program_id'.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único de la cohorte. |
| 2 | `program_id` | uuid | NO |  | Identificador del programa al que pertenece la cohorte. |
| 3 | `name` | text | NO |  | Nombre de la cohorte. |
| 4 | `start_date` | date | YES |  | Fecha de inicio de la cohorte. |
| 5 | `end_date` | date | YES |  | Fecha de finalización de la cohorte. |
| 6 | `status` | text | YES | 'planned'::text | Estado actual de la cohorte, por defecto 'planned'. |
| 7 | `created_at` | timestamp with time zone | NO | now() | Fecha y hora de creación del registro. |
| 8 | `updated_at` | timestamp with time zone | NO | now() | Fecha y hora de la última actualización del registro. |

## public.compliance_status

- Filas: **-1**

> La tabla 'compliance_status' almacena el estado de cumplimiento de requisitos específicos, relacionándose con la tabla 'requirement' a través de la clave foránea 'requirement_id'. Cada registro representa un estado asociado a un sujeto determinado y su cumplimiento en un momento específico.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único del estado de cumplimiento. |
| 2 | `requirement_id` | uuid | NO |  | Identificador del requisito relacionado, referencia a la tabla 'requirement'. |
| 3 | `subject_type` | text | NO |  | Tipo de sujeto al que se aplica el estado de cumplimiento. |
| 4 | `subject_id` | uuid | NO |  | Identificador del sujeto específico al que se aplica el estado. |
| 5 | `status` | text | NO |  | Estado de cumplimiento (ej. cumplido, no cumplido). |
| 6 | `confidence` | numeric | YES |  | Nivel de confianza en la evaluación del estado (opcional). |
| 7 | `explanation` | text | YES |  | Explicación adicional sobre el estado de cumplimiento (opcional). |
| 8 | `as_of` | timestamp with time zone | NO | now() | Fecha y hora en que se registró el estado de cumplimiento. |

## public.document

- Filas: **-1**

> La tabla 'document' almacena información sobre documentos, incluyendo su identificación, metadatos y tiempos de creación y modificación. No tiene claves foráneas, lo que indica que no está directamente relacionada con otras tablas.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único del documento, generado automáticamente. |
| 2 | `drive_file_id` | text | YES |  | Identificador del archivo en el sistema de almacenamiento en la nube. |
| 3 | `sha1` | text | YES |  | Hash SHA-1 del contenido del documento para verificación de integridad. |
| 4 | `path` | text | YES |  | Ruta de acceso al documento en el sistema de archivos. |
| 5 | `mime` | text | YES |  | Tipo MIME del documento, que indica su formato. |
| 6 | `created_time` | timestamp with time zone | YES |  | Fecha y hora en que se creó el documento. |
| 7 | `modified_time` | timestamp with time zone | YES |  | Fecha y hora de la última modificación del documento. |
| 8 | `project_id` | text | YES |  | Identificador del proyecto asociado al documento. |
| 9 | `created_at` | timestamp with time zone | NO | now() | Fecha y hora en que se registró el documento en la base de datos. |

## public.enrichments_files

- Filas: **2,628**

> La tabla 'enrichments_files' almacena información sobre archivos enriquecidos, incluyendo detalles como el título, resumen, etiquetas y entidades asociadas. Cada archivo está vinculado a un 'drive_id' y puede estar asociado a un 'project_id'.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `drive_id` | text | NO |  | Identificador del drive donde se encuentra el archivo. |
| 2 | `file_id` | text | NO |  | Identificador único del archivo. |
| 3 | `title_canonical` | text | NO |  | Título canónico del archivo. |
| 4 | `summary_80w` | text | NO |  | Resumen del archivo en 80 palabras. |
| 5 | `tags` | ARRAY | NO | '{}'::text[] | Etiquetas asociadas al archivo. |
| 6 | `topic_label` | text | NO | 'otro'::text | Etiqueta de tema del archivo. |
| 7 | `entities` | ARRAY | NO | '{}'::text[] | Entidades mencionadas en el archivo. |
| 8 | `confidence` | double precision | NO |  | Nivel de confianza en la información del archivo. |
| 9 | `notes_short` | text | NO | ''::text | Notas breves sobre el archivo. |
| 10 | `fingerprint` | text | NO |  | Huella digital del archivo. |
| 11 | `llm_recipe` | text | NO |  | Receta utilizada para el modelo de lenguaje asociado al archivo. |
| 12 | `indexed_at` | timestamp with time zone | NO |  | Fecha y hora en que se indexó el archivo. |
| 13 | `project_id` | text | YES |  | Identificador del proyecto asociado al archivo (opcional). |

## public.enrichments_folders

- Filas: **404**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `drive_id` | text | NO |  |  |
| 2 | `folder_id` | text | NO |  |  |
| 3 | `title_canonical` | text | NO |  |  |
| 4 | `summary_120w` | text | NO |  |  |
| 5 | `tags` | ARRAY | NO | '{}'::text[] |  |
| 6 | `topic_label` | text | NO | 'otro'::text |  |
| 7 | `entities` | ARRAY | NO | '{}'::text[] |  |
| 8 | `confidence` | double precision | NO |  |  |
| 9 | `notes_short` | text | NO | ''::text |  |
| 10 | `fingerprint` | text | NO |  |  |
| 11 | `llm_recipe` | text | NO |  |  |
| 12 | `indexed_at` | timestamp with time zone | NO |  |  |
| 13 | `relative_path` | text | NO |  |  |
| 14 | `name` | text | NO |  |  |
| 15 | `children_count_total` | integer | NO |  |  |
| 16 | `children_count_used` | integer | NO |  |  |
| 17 | `project_id` | text | YES |  |  |

## public.evaluation

- Filas: **-1**

> La tabla 'evaluation' almacena evaluaciones relacionadas con evidencias y requisitos, referenciando las tablas 'evidence' y 'requirement' a través de claves foráneas. Su propósito es registrar los resultados de las evaluaciones, incluyendo detalles y puntuaciones.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único de la evaluación. |
| 2 | `evidence_id` | uuid | NO |  | Identificador de la evidencia asociada a la evaluación (FK a 'evidence'). |
| 3 | `requirement_id` | uuid | NO |  | Identificador del requisito evaluado (FK a 'requirement'). |
| 4 | `instrument` | text | YES |  | Instrumento utilizado para la evaluación. |
| 5 | `method` | text | YES |  | Método aplicado en la evaluación. |
| 6 | `score` | numeric | YES |  | Puntuación obtenida en la evaluación. |
| 7 | `passed` | boolean | YES |  | Indica si la evaluación fue aprobada. |
| 8 | `details_json` | jsonb | NO | '{}'::jsonb | Detalles adicionales de la evaluación en formato JSON. |
| 9 | `evaluated_at` | timestamp with time zone | NO | now() | Fecha y hora en que se realizó la evaluación. |

## public.event

- Filas: **-1**

> La tabla 'event' almacena información sobre eventos registrados en el sistema, incluyendo el tipo de evento y el momento en que ocurrió. Esta tabla permite relacionar actores y sujetos a través de sus identificadores, aunque no tiene claves foráneas definidas.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único del evento, generado automáticamente. |
| 2 | `event_type` | text | NO |  | Tipo de evento que se está registrando. |
| 3 | `occurred_at` | timestamp with time zone | NO | now() | Fecha y hora en que ocurrió el evento, con zona horaria. |
| 4 | `actor_id` | uuid | YES |  | Identificador del actor que realizó la acción, puede ser nulo. |
| 5 | `subject_type` | text | YES |  | Tipo de sujeto relacionado con el evento, puede ser nulo. |
| 6 | `subject_id` | uuid | YES |  | Identificador del sujeto relacionado con el evento, puede ser nulo. |
| 7 | `payload_json` | jsonb | NO | '{}'::jsonb | Datos adicionales del evento en formato JSON. |
| 8 | `source` | text | YES |  | Origen del evento, puede ser nulo. |

## public.evidence

- Filas: **-1**

> La tabla 'evidence' almacena evidencias relacionadas con asignaciones y documentos, vinculándose a la tabla 'assignment' a través de 'assignment_id' y a la tabla 'document' mediante 'document_id'. Su propósito es gestionar y registrar información sobre evidencias en formato JSON.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único de la evidencia. |
| 2 | `assignment_id` | uuid | NO |  | Identificador de la asignación a la que pertenece la evidencia. |
| 3 | `type_id` | text | NO |  | Tipo de evidencia, representado como texto. |
| 4 | `document_id` | uuid | YES |  | Identificador del documento asociado, puede ser nulo. |
| 5 | `source` | text | YES |  | Fuente de la evidencia, puede ser nulo. |
| 6 | `payload_json` | jsonb | NO | '{}'::jsonb | Datos de la evidencia en formato JSON. |
| 7 | `ingested_at` | timestamp with time zone | NO | now() | Fecha y hora en que se registró la evidencia. |

## public.evidence_context

- Filas: **-1**

> La tabla 'evidence_context' almacena información sobre el contexto de las evidencias, relacionándose con las tablas 'evidence', 'organization', 'person' y 'session' a través de claves foráneas. Cada registro vincula una evidencia con su respectivo contexto organizacional, personal y de sesión.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `evidence_id` | uuid | NO |  | Identificador único de la evidencia, clave foránea de la tabla 'evidence'. |
| 2 | `session_id` | uuid | YES |  | Identificador de la sesión asociada, clave foránea de la tabla 'session'. |
| 3 | `person_id` | uuid | YES |  | Identificador de la persona asociada, clave foránea de la tabla 'person'. |
| 4 | `organization_id` | uuid | YES |  | Identificador de la organización asociada, clave foránea de la tabla 'organization'. |

## public.extraction

- Filas: **-1**

> La tabla 'extraction' almacena información sobre las extracciones de documentos, incluyendo detalles como el parser utilizado y la calidad de la extracción. Está relacionada con la tabla 'document' a través de la clave foránea 'document_id'.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único de la extracción. |
| 2 | `document_id` | uuid | NO |  | Identificador del documento asociado a la extracción. |
| 3 | `parser` | text | YES |  | Nombre del parser utilizado para la extracción. |
| 4 | `version` | text | YES |  | Versión del documento extraído. |
| 5 | `schema_version` | text | YES |  | Versión del esquema del documento extraído. |
| 6 | `quality` | numeric | YES |  | Calidad de la extracción, medida numéricamente. |
| 7 | `created_at` | timestamp with time zone | NO | now() | Fecha y hora en que se creó el registro de extracción. |

## public.flow_steps

- Filas: **-1**

> La tabla 'flow_steps' almacena los pasos de un flujo de trabajo, cada uno identificado por un UUID único. Está relacionada con la tabla 'program_flows' a través de la clave foránea 'flow_id', que indica a qué flujo pertenece cada paso.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único del paso del flujo. |
| 2 | `flow_id` | uuid | NO |  | Identificador del flujo al que pertenece este paso (FK a program_flows). |
| 3 | `step_order` | integer | NO |  | Orden secuencial del paso dentro del flujo. |
| 4 | `name` | text | NO |  | Nombre descriptivo del paso. |
| 5 | `created_at` | timestamp with time zone | YES | now() | Fecha y hora de creación del registro. |
| 6 | `updated_at` | timestamp with time zone | YES | now() | Fecha y hora de la última actualización del registro. |

## public.form_runs

- Filas: **-1**

> La tabla 'form_runs' almacena información sobre las ejecuciones de formularios, vinculándose con las tablas 'program_flows', 'program_form_versions', 'programs' y 'flow_steps' a través de claves foráneas. Cada registro representa una instancia de un formulario en un flujo específico de un proyecto.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único de la ejecución del formulario. |
| 2 | `project_id` | text | NO |  | Identificador del proyecto al que pertenece la ejecución. |
| 3 | `flow_id` | uuid | NO |  | Identificador del flujo asociado a la ejecución del formulario. |
| 4 | `step_id` | uuid | NO |  | Identificador del paso en el flujo correspondiente a la ejecución. |
| 5 | `form_version_id` | uuid | NO |  | Identificador de la versión del formulario utilizado en la ejecución. |
| 6 | `cohort` | text | YES |  | Cohorte asociada a la ejecución, si aplica. |
| 7 | `flow_mode` | text | YES |  | Modo del flujo en el que se ejecuta el formulario. |
| 8 | `opens_at` | timestamp with time zone | YES |  | Fecha y hora en que se abre el formulario para la ejecución. |
| 9 | `closes_at` | timestamp with time zone | YES |  | Fecha y hora en que se cierra el formulario para la ejecución. |
| 10 | `created_at` | timestamp with time zone | YES | now() | Fecha y hora en que se creó el registro de la ejecución. |

## public.identity_candidate

- Filas: **-1**

> La tabla 'identity_candidate' almacena información sobre candidatos de identidad, incluyendo un puntaje base y señales en formato JSON. Se relaciona con las tablas 'person' y 'staging_attendance_row' a través de las claves foráneas 'person_id' y 'staging_row_id'.

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() | Identificador único del candidato, generado automáticamente. |
| 2 | `staging_row_id` | uuid | NO |  | Identificador de la fila de asistencia en estado provisional, no nulo. |
| 3 | `person_id` | uuid | NO |  | Identificador de la persona asociada, no nulo. |
| 4 | `signals_json` | jsonb | NO | '{}'::jsonb | Datos en formato JSONB que representan señales relacionadas con el candidato, no nulo. |
| 5 | `base_score` | numeric | YES |  | Puntaje base del candidato, puede ser nulo. |

## public.identity_resolution

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `staging_row_id` | uuid | NO |  |  |
| 3 | `person_id_selected` | uuid | YES |  |  |
| 4 | `method` | text | YES |  |  |
| 5 | `confidence` | numeric | YES |  |  |
| 6 | `explanation_text` | text | YES |  |  |
| 7 | `decided_at` | timestamp with time zone | YES | now() |  |
| 8 | `decided_by` | uuid | YES |  |  |

## public.load_batch

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `document_id` | uuid | YES |  |  |
| 3 | `started_at` | timestamp with time zone | NO | now() |  |
| 4 | `ended_at` | timestamp with time zone | YES |  |  |
| 5 | `status` | text | YES | 'running'::text |  |
| 6 | `inserted` | integer | YES | 0 |  |
| 7 | `updated` | integer | YES | 0 |  |
| 8 | `skipped` | integer | YES | 0 |  |
| 9 | `errors` | integer | YES | 0 |  |

## public.mentor

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `person_id` | uuid | NO |  |  |
| 2 | `expertise` | text | YES |  |  |
| 3 | `notes` | text | YES |  |  |

## public.module

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `cohort_id` | uuid | NO |  |  |
| 3 | `title` | text | NO |  |  |
| 4 | `description` | text | YES |  |  |
| 5 | `created_at` | timestamp with time zone | NO | now() |  |

## public.organization

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `legal_name` | text | NO |  |  |
| 3 | `country` | text | YES |  |  |
| 4 | `sector` | text | YES |  |  |
| 5 | `contact_id` | uuid | YES |  |  |
| 6 | `created_at` | timestamp with time zone | NO | now() |  |
| 7 | `updated_at` | timestamp with time zone | NO | now() |  |

## public.participation

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `cohort_id` | uuid | NO |  |  |
| 3 | `person_id` | uuid | NO |  |  |
| 4 | `role_in_cohort` | text | YES |  |  |
| 5 | `status` | text | YES | 'active'::text |  |
| 6 | `created_at` | timestamp with time zone | NO | now() |  |

## public.person

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `full_name` | text | NO |  |  |
| 3 | `email` | text | YES |  |  |
| 4 | `role` | text | YES |  |  |
| 5 | `org_id` | uuid | YES |  |  |
| 6 | `created_at` | timestamp with time zone | NO | now() |  |
| 7 | `updated_at` | timestamp with time zone | NO | now() |  |

## public.program

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `name` | text | NO |  |  |
| 3 | `goals` | jsonb | YES | '{}'::jsonb |  |
| 4 | `created_at` | timestamp with time zone | NO | now() |  |
| 5 | `updated_at` | timestamp with time zone | NO | now() |  |

## public.program_flows

- Filas: **1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `project_id` | text | NO |  |  |
| 3 | `name` | text | NO |  |  |
| 4 | `audience` | text | YES |  |  |
| 5 | `stage` | text | NO | 'convocatoria_seleccion'::text |  |
| 6 | `created_at` | timestamp with time zone | YES | now() |  |
| 7 | `deleted_at` | timestamp with time zone | YES |  |  |
| 8 | `updated_at` | timestamp with time zone | YES | now() |  |

## public.program_form_questions

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `form_version_id` | uuid | NO |  |  |
| 3 | `q_order` | integer | NO |  |  |
| 4 | `q_code` | text | NO |  |  |
| 5 | `q_label` | text | NO |  |  |
| 6 | `q_type` | text | NO |  |  |
| 7 | `q_options` | jsonb | YES |  |  |
| 8 | `required` | boolean | YES | false |  |
| 9 | `created_at` | timestamp with time zone | YES | now() |  |

## public.program_form_versions

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `form_id` | uuid | NO |  |  |
| 3 | `version` | integer | NO |  |  |
| 4 | `status` | text | NO | 'draft'::text |  |
| 5 | `created_at` | timestamp with time zone | YES | now() |  |
| 6 | `published_at` | timestamp with time zone | YES |  |  |

## public.program_forms

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `project_id` | text | NO |  |  |
| 3 | `name` | text | NO |  |  |
| 4 | `stage` | text | NO | 'convocatoria_seleccion'::text |  |
| 5 | `audience` | text | YES |  |  |
| 6 | `created_at` | timestamp with time zone | YES | now() |  |
| 7 | `updated_at` | timestamp with time zone | YES | now() |  |

## public.program_stages

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `project_id` | text | NO |  |  |
| 3 | `stage` | text | NO |  |  |
| 4 | `data` | jsonb | YES |  |  |
| 5 | `updated_at` | timestamp with time zone | YES | now() |  |

## public.programs

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `project_id` | text | NO |  |  |
| 2 | `code` | text | YES |  |  |
| 3 | `title` | text | YES |  |  |
| 4 | `scope` | text | YES |  |  |
| 5 | `actors` | ARRAY | YES |  |  |
| 6 | `folders` | jsonb | YES |  |  |
| 7 | `training_design` | jsonb | YES |  |  |
| 8 | `forms` | jsonb | YES |  |  |
| 9 | `config` | jsonb | YES |  |  |
| 10 | `updated_at` | timestamp with time zone | YES | now() |  |

## public.rag_node

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `document_id` | uuid | YES |  |  |
| 3 | `chunk` | text | NO |  |  |
| 4 | `embedding` | USER-DEFINED | YES |  |  |
| 5 | `metadata_json` | jsonb | NO | '{}'::jsonb |  |
| 6 | `created_at` | timestamp with time zone | NO | now() |  |

## public.requirement

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `cohort_id` | uuid | NO |  |  |
| 3 | `type_id` | text | NO |  |  |
| 4 | `title` | text | NO |  |  |
| 5 | `window_start` | timestamp with time zone | YES |  |  |
| 6 | `window_end` | timestamp with time zone | YES |  |  |
| 7 | `policy_json` | jsonb | NO | '{}'::jsonb |  |
| 8 | `created_at` | timestamp with time zone | NO | now() |  |

## public.session

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `cohort_id` | uuid | NO |  |  |
| 3 | `module_id` | uuid | YES |  |  |
| 4 | `type` | text | YES |  |  |
| 5 | `title` | text | NO |  |  |
| 6 | `scheduled_at` | timestamp with time zone | YES |  |  |
| 7 | `facilitator_id` | uuid | YES |  |  |
| 8 | `created_at` | timestamp with time zone | NO | now() |  |

## public.staging_attendance_row

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `document_id` | uuid | NO |  |  |
| 3 | `session_id` | uuid | YES |  |  |
| 4 | `raw_name` | text | YES |  |  |
| 5 | `norm_name` | text | YES |  |  |
| 6 | `row_hash` | text | YES |  |  |
| 7 | `status` | text | YES | 'new'::text |  |
| 8 | `load_batch_id` | uuid | YES |  |  |
| 9 | `created_at` | timestamp with time zone | NO | now() |  |

## auth.audit_log_entries

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `instance_id` | uuid | YES |  |  |
| 2 | `id` | uuid | NO |  |  |
| 3 | `payload` | json | YES |  |  |
| 4 | `created_at` | timestamp with time zone | YES |  |  |
| 5 | `ip_address` | character varying | NO | ''::character varying |  |

## auth.flow_state

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `user_id` | uuid | YES |  |  |
| 3 | `auth_code` | text | NO |  |  |
| 4 | `code_challenge_method` | USER-DEFINED | NO |  |  |
| 5 | `code_challenge` | text | NO |  |  |
| 6 | `provider_type` | text | NO |  |  |
| 7 | `provider_access_token` | text | YES |  |  |
| 8 | `provider_refresh_token` | text | YES |  |  |
| 9 | `created_at` | timestamp with time zone | YES |  |  |
| 10 | `updated_at` | timestamp with time zone | YES |  |  |
| 11 | `authentication_method` | text | NO |  |  |
| 12 | `auth_code_issued_at` | timestamp with time zone | YES |  |  |

## auth.identities

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `provider_id` | text | NO |  |  |
| 2 | `user_id` | uuid | NO |  |  |
| 3 | `identity_data` | jsonb | NO |  |  |
| 4 | `provider` | text | NO |  |  |
| 5 | `last_sign_in_at` | timestamp with time zone | YES |  |  |
| 6 | `created_at` | timestamp with time zone | YES |  |  |
| 7 | `updated_at` | timestamp with time zone | YES |  |  |
| 8 | `email` | text | YES |  |  |
| 9 | `id` | uuid | NO | gen_random_uuid() |  |

## auth.instances

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `uuid` | uuid | YES |  |  |
| 3 | `raw_base_config` | text | YES |  |  |
| 4 | `created_at` | timestamp with time zone | YES |  |  |
| 5 | `updated_at` | timestamp with time zone | YES |  |  |

## auth.mfa_amr_claims

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `session_id` | uuid | NO |  |  |
| 2 | `created_at` | timestamp with time zone | NO |  |  |
| 3 | `updated_at` | timestamp with time zone | NO |  |  |
| 4 | `authentication_method` | text | NO |  |  |
| 5 | `id` | uuid | NO |  |  |

## auth.mfa_challenges

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `factor_id` | uuid | NO |  |  |
| 3 | `created_at` | timestamp with time zone | NO |  |  |
| 4 | `verified_at` | timestamp with time zone | YES |  |  |
| 5 | `ip_address` | inet | NO |  |  |
| 6 | `otp_code` | text | YES |  |  |
| 7 | `web_authn_session_data` | jsonb | YES |  |  |

## auth.mfa_factors

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `user_id` | uuid | NO |  |  |
| 3 | `friendly_name` | text | YES |  |  |
| 4 | `factor_type` | USER-DEFINED | NO |  |  |
| 5 | `status` | USER-DEFINED | NO |  |  |
| 6 | `created_at` | timestamp with time zone | NO |  |  |
| 7 | `updated_at` | timestamp with time zone | NO |  |  |
| 8 | `secret` | text | YES |  |  |
| 9 | `phone` | text | YES |  |  |
| 10 | `last_challenged_at` | timestamp with time zone | YES |  |  |
| 11 | `web_authn_credential` | jsonb | YES |  |  |
| 12 | `web_authn_aaguid` | uuid | YES |  |  |

## auth.oauth_clients

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `client_id` | text | NO |  |  |
| 3 | `client_secret_hash` | text | NO |  |  |
| 4 | `registration_type` | USER-DEFINED | NO |  |  |
| 5 | `redirect_uris` | text | NO |  |  |
| 6 | `grant_types` | text | NO |  |  |
| 7 | `client_name` | text | YES |  |  |
| 8 | `client_uri` | text | YES |  |  |
| 9 | `logo_uri` | text | YES |  |  |
| 10 | `created_at` | timestamp with time zone | NO | now() |  |
| 11 | `updated_at` | timestamp with time zone | NO | now() |  |
| 12 | `deleted_at` | timestamp with time zone | YES |  |  |

## auth.one_time_tokens

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `user_id` | uuid | NO |  |  |
| 3 | `token_type` | USER-DEFINED | NO |  |  |
| 4 | `token_hash` | text | NO |  |  |
| 5 | `relates_to` | text | NO |  |  |
| 6 | `created_at` | timestamp without time zone | NO | now() |  |
| 7 | `updated_at` | timestamp without time zone | NO | now() |  |

## auth.refresh_tokens

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `instance_id` | uuid | YES |  |  |
| 2 | `id` | bigint | NO | nextval('auth.refresh_tokens_id_seq'::regclass) |  |
| 3 | `token` | character varying | YES |  |  |
| 4 | `user_id` | character varying | YES |  |  |
| 5 | `revoked` | boolean | YES |  |  |
| 6 | `created_at` | timestamp with time zone | YES |  |  |
| 7 | `updated_at` | timestamp with time zone | YES |  |  |
| 8 | `parent` | character varying | YES |  |  |
| 9 | `session_id` | uuid | YES |  |  |

## auth.saml_providers

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `sso_provider_id` | uuid | NO |  |  |
| 3 | `entity_id` | text | NO |  |  |
| 4 | `metadata_xml` | text | NO |  |  |
| 5 | `metadata_url` | text | YES |  |  |
| 6 | `attribute_mapping` | jsonb | YES |  |  |
| 7 | `created_at` | timestamp with time zone | YES |  |  |
| 8 | `updated_at` | timestamp with time zone | YES |  |  |
| 9 | `name_id_format` | text | YES |  |  |

## auth.saml_relay_states

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `sso_provider_id` | uuid | NO |  |  |
| 3 | `request_id` | text | NO |  |  |
| 4 | `for_email` | text | YES |  |  |
| 5 | `redirect_to` | text | YES |  |  |
| 7 | `created_at` | timestamp with time zone | YES |  |  |
| 8 | `updated_at` | timestamp with time zone | YES |  |  |
| 9 | `flow_state_id` | uuid | YES |  |  |

## auth.schema_migrations

- Filas: **62**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `version` | character varying | NO |  |  |

## auth.sessions

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `user_id` | uuid | NO |  |  |
| 3 | `created_at` | timestamp with time zone | YES |  |  |
| 4 | `updated_at` | timestamp with time zone | YES |  |  |
| 5 | `factor_id` | uuid | YES |  |  |
| 6 | `aal` | USER-DEFINED | YES |  |  |
| 7 | `not_after` | timestamp with time zone | YES |  |  |
| 8 | `refreshed_at` | timestamp without time zone | YES |  |  |
| 9 | `user_agent` | text | YES |  |  |
| 10 | `ip` | inet | YES |  |  |
| 11 | `tag` | text | YES |  |  |

## auth.sso_domains

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `sso_provider_id` | uuid | NO |  |  |
| 3 | `domain` | text | NO |  |  |
| 4 | `created_at` | timestamp with time zone | YES |  |  |
| 5 | `updated_at` | timestamp with time zone | YES |  |  |

## auth.sso_providers

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO |  |  |
| 2 | `resource_id` | text | YES |  |  |
| 3 | `created_at` | timestamp with time zone | YES |  |  |
| 4 | `updated_at` | timestamp with time zone | YES |  |  |
| 5 | `disabled` | boolean | YES |  |  |

## auth.users

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `instance_id` | uuid | YES |  |  |
| 2 | `id` | uuid | NO |  |  |
| 3 | `aud` | character varying | YES |  |  |
| 4 | `role` | character varying | YES |  |  |
| 5 | `email` | character varying | YES |  |  |
| 6 | `encrypted_password` | character varying | YES |  |  |
| 7 | `email_confirmed_at` | timestamp with time zone | YES |  |  |
| 8 | `invited_at` | timestamp with time zone | YES |  |  |
| 9 | `confirmation_token` | character varying | YES |  |  |
| 10 | `confirmation_sent_at` | timestamp with time zone | YES |  |  |
| 11 | `recovery_token` | character varying | YES |  |  |
| 12 | `recovery_sent_at` | timestamp with time zone | YES |  |  |
| 13 | `email_change_token_new` | character varying | YES |  |  |
| 14 | `email_change` | character varying | YES |  |  |
| 15 | `email_change_sent_at` | timestamp with time zone | YES |  |  |
| 16 | `last_sign_in_at` | timestamp with time zone | YES |  |  |
| 17 | `raw_app_meta_data` | jsonb | YES |  |  |
| 18 | `raw_user_meta_data` | jsonb | YES |  |  |
| 19 | `is_super_admin` | boolean | YES |  |  |
| 20 | `created_at` | timestamp with time zone | YES |  |  |
| 21 | `updated_at` | timestamp with time zone | YES |  |  |
| 22 | `phone` | text | YES | NULL::character varying |  |
| 23 | `phone_confirmed_at` | timestamp with time zone | YES |  |  |
| 24 | `phone_change` | text | YES | ''::character varying |  |
| 25 | `phone_change_token` | character varying | YES | ''::character varying |  |
| 26 | `phone_change_sent_at` | timestamp with time zone | YES |  |  |
| 27 | `confirmed_at` | timestamp with time zone | YES |  |  |
| 28 | `email_change_token_current` | character varying | YES | ''::character varying |  |
| 29 | `email_change_confirm_status` | smallint | YES | 0 |  |
| 30 | `banned_until` | timestamp with time zone | YES |  |  |
| 31 | `reauthentication_token` | character varying | YES | ''::character varying |  |
| 32 | `reauthentication_sent_at` | timestamp with time zone | YES |  |  |
| 33 | `is_sso_user` | boolean | NO | false |  |
| 34 | `deleted_at` | timestamp with time zone | YES |  |  |
| 35 | `is_anonymous` | boolean | NO | false |  |

## realtime.messages

- Filas: **0**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 3 | `topic` | text | NO |  |  |
| 4 | `extension` | text | NO |  |  |
| 5 | `payload` | jsonb | YES |  |  |
| 6 | `event` | text | YES |  |  |
| 7 | `private` | boolean | YES | false |  |
| 8 | `updated_at` | timestamp without time zone | NO | now() |  |
| 9 | `inserted_at` | timestamp without time zone | NO | now() |  |
| 10 | `id` | uuid | NO | gen_random_uuid() |  |

## realtime.schema_migrations

- Filas: **63**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `version` | bigint | NO |  |  |
| 2 | `inserted_at` | timestamp without time zone | YES |  |  |

## realtime.subscription

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | bigint | NO |  |  |
| 2 | `subscription_id` | uuid | NO |  |  |
| 4 | `entity` | regclass | NO |  |  |
| 5 | `filters` | ARRAY | NO | '{}'::realtime.user_defined_filter[] |  |
| 7 | `claims` | jsonb | NO |  |  |
| 8 | `claims_role` | regrole | NO |  |  |
| 9 | `created_at` | timestamp without time zone | NO | timezone('utc'::text, now()) |  |

## storage.buckets

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | text | NO |  |  |
| 2 | `name` | text | NO |  |  |
| 3 | `owner` | uuid | YES |  |  |
| 4 | `created_at` | timestamp with time zone | YES | now() |  |
| 5 | `updated_at` | timestamp with time zone | YES | now() |  |
| 6 | `public` | boolean | YES | false |  |
| 7 | `avif_autodetection` | boolean | YES | false |  |
| 8 | `file_size_limit` | bigint | YES |  |  |
| 9 | `allowed_mime_types` | ARRAY | YES |  |  |
| 10 | `owner_id` | text | YES |  |  |

## storage.migrations

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | integer | NO |  |  |
| 2 | `name` | character varying | NO |  |  |
| 3 | `hash` | character varying | NO |  |  |
| 4 | `executed_at` | timestamp without time zone | YES | CURRENT_TIMESTAMP |  |

## storage.objects

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `bucket_id` | text | YES |  |  |
| 3 | `name` | text | YES |  |  |
| 4 | `owner` | uuid | YES |  |  |
| 5 | `created_at` | timestamp with time zone | YES | now() |  |
| 6 | `updated_at` | timestamp with time zone | YES | now() |  |
| 7 | `last_accessed_at` | timestamp with time zone | YES | now() |  |
| 8 | `metadata` | jsonb | YES |  |  |
| 9 | `path_tokens` | ARRAY | YES |  |  |
| 10 | `version` | text | YES |  |  |
| 11 | `owner_id` | text | YES |  |  |
| 12 | `user_metadata` | jsonb | YES |  |  |

## storage.s3_multipart_uploads

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | text | NO |  |  |
| 2 | `in_progress_size` | bigint | NO | 0 |  |
| 3 | `upload_signature` | text | NO |  |  |
| 4 | `bucket_id` | text | NO |  |  |
| 5 | `key` | text | NO |  |  |
| 6 | `version` | text | NO |  |  |
| 7 | `owner_id` | text | YES |  |  |
| 8 | `created_at` | timestamp with time zone | NO | now() |  |
| 9 | `user_metadata` | jsonb | YES |  |  |

## storage.s3_multipart_uploads_parts

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `upload_id` | text | NO |  |  |
| 3 | `size` | bigint | NO | 0 |  |
| 4 | `part_number` | integer | NO |  |  |
| 5 | `bucket_id` | text | NO |  |  |
| 6 | `key` | text | NO |  |  |
| 7 | `etag` | text | NO |  |  |
| 8 | `owner_id` | text | YES |  |  |
| 9 | `version` | text | NO |  |  |
| 10 | `created_at` | timestamp with time zone | NO | now() |  |

## vault.secrets

- Filas: **-1**

### Campos

| # | columna | tipo | nulo | default | descripción |
|---:|---------|------|------|--------|-------------|
| 1 | `id` | uuid | NO | gen_random_uuid() |  |
| 2 | `name` | text | YES |  |  |
| 3 | `description` | text | NO | ''::text |  |
| 4 | `secret` | text | NO |  |  |
| 5 | `key_id` | uuid | YES |  |  |
| 6 | `nonce` | bytea | YES | vault._crypto_aead_det_noncegen() |  |
| 7 | `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |  |
| 8 | `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |  |

