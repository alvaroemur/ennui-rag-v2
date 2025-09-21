erDiagram
    %% === Relaciones de programa y cohortes ===
    PROGRAM ||--o{ COHORT : has

    %% === Seleccion / postulaciones ===
    COHORT ||--o{ APPLICATION : opens
    ORGANIZATION ||--o{ APPLICATION : submits

    %% === Participacion de personas en la cohorte ===
    COHORT ||--o{ PARTICIPATION : enrolls
    PERSON ||--o{ PARTICIPATION : joins

    %% === Agenda y asistencia ===
    COHORT ||--o{ SESSION : schedules
    SESSION ||--o{ ATTENDANCE : records
    PERSON ||--o{ ATTENDANCE : attends

    %% === Mentorias ===
    PERSON ||--|| MENTOR : role_of
    MENTOR ||--o{ MENTORING_MATCH : assigned_to
    ORGANIZATION ||--o{ MENTORING_MATCH : receives
    COHORT ||--o{ MENTORING_MATCH : context

    %% === Cumplimiento (de-polimorfizado) ===
    COHORT ||--o{ REQUIREMENT : defines
    REQUIREMENT ||--o{ ASSIGNMENT : targets
    ASSIGNMENT ||--o{ EVIDENCE : has
    EVIDENCE ||--o{ EVALUATION : results_in
    REQUIREMENT ||--o{ COMPLIANCE_STATUS : summarized_as

    %% Contexto operativo de evidencias (hace visibles los vinculos)
    EVIDENCE ||--|| EVIDENCE_CONTEXT : provides
    EVIDENCE_CONTEXT }o--|| SESSION : relates_session
    EVIDENCE_CONTEXT }o--|| PERSON : relates_person
    EVIDENCE_CONTEXT }o--|| ORGANIZATION : relates_org

    %% Documental & Staging
    DOCUMENT ||--o{ EXTRACTION : parsed_into
    DOCUMENT ||--o{ STAGING_ATTENDANCE_ROW : provides_rows
    STAGING_ATTENDANCE_ROW ||--o{ IDENTITY_CANDIDATE : suggests
    STAGING_ATTENDANCE_ROW ||--|| IDENTITY_RESOLUTION : decides
    LOAD_BATCH ||--o{ STAGING_ATTENDANCE_ROW : loads

    %% RAG
    RAG_NODE }o--|| DOCUMENT : indexes

    %% === Definicion de entidades (campos minimos) ===
    PROGRAM {
      int id
      text name
    }
    COHORT {
      int id
      int program_id
      text name
      date start_date
      date end_date
      text status
    }
    ORGANIZATION {
      int id
      text legal_name
      text country
      text sector
      int contact_id
    }
    PERSON {
      int id
      text full_name
      text email
      text role
      int org_id
    }
    APPLICATION {
      int id
      int cohort_id
      int organization_id
      text status
      datetime submitted_at
    }
    PARTICIPATION {
      int id
      int cohort_id
      int person_id
      text role_in_cohort
      text status
    }
    SESSION {
      int id
      int cohort_id
      int module_id
      text type
      text title
      datetime scheduled_at
      int facilitator_id
    }
    ATTENDANCE {
      int id
      int session_id
      int person_id
      text status
      datetime check_in_at
    }
    MENTOR {
      int person_id
      text expertise
    }
    MENTORING_MATCH {
      int id
      int mentor_id
      int organization_id
      int cohort_id
      text status
    }
    REQUIREMENT {
      int id
      int cohort_id
      int type_id
      text title
      datetime window_start
      datetime window_end
      json policy_json
    }
    ASSIGNMENT {
      int id
      int requirement_id
      int subject_person_id
      int subject_org_id
      text status
    }
    EVIDENCE {
      int id
      int assignment_id
      int type_id
      int document_id
      text source
      json payload_json
    }
    EVIDENCE_CONTEXT {
      int evidence_id
      int session_id
      int person_id
      int organization_id
    }
    EVALUATION {
      int id
      int evidence_id
      int requirement_id
      text method
      numeric score
      boolean passed
      json details_json
    }
    COMPLIANCE_STATUS {
      int id
      int requirement_id
      text subject_type
      int subject_id
      text status
      numeric confidence
      text explanation
      datetime as_of
    }
    DOCUMENT {
      int id
      text drive_file_id
      text sha1
      text path
      text mime
    }
    EXTRACTION {
      int id
      int document_id
      text parser
      text version
      text schema_version
      numeric quality
    }
    STAGING_ATTENDANCE_ROW {
      int id
      int document_id
      int session_id
      text raw_name
      text norm_name
      text row_hash
      text status
    }
    IDENTITY_CANDIDATE {
      int id
      int staging_row_id
      int person_id
      json signals_json
      numeric base_score
    }
    IDENTITY_RESOLUTION {
      int id
      int staging_row_id
      int person_id_selected
      text method
      numeric confidence
      text explanation_text
      datetime decided_at
      int decided_by
    }
    LOAD_BATCH {
      int id
      int document_id
      datetime started_at
      datetime ended_at
      text status
      int inserted
      int updated
      int skipped
      int errors
    }
    RAG_NODE {
      int id
      int document_id
      text chunk
      json metadata_json
    }