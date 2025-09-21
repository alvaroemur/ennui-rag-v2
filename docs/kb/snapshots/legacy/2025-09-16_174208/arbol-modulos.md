---
title: "Árbol de Módulos - Snapshot 2025-09-16_174208"
project: "ennui-rag"
doc_type: "kb"
version: "v0.1"
date: "2025-09-16_174208"
source_of_truth: "as-is"
---

# ennui-rag · Estructura de Archivos

## 📁 Estructura Completa del Proyecto

```
ennui-rag/
├─ .cursor/
  ├─ commands/
├─ configs/
  ├─ credentials/
    │  service_account.json  (2KB)
  │  base.yaml  (247B)
  │  dev.yaml  (138B)
├─ data/
  ├─ 1caxesJ5QtTLCf8wcsrZRmcCP1MVg65Xe/
    │  sessions.json  (211B)
  ├─ 1F3NQevlP-4m5NXImqPbibAEgtMr0B0s_/
    │  catalog_base.csv  (259KB)
    │  catalog_enriched_files.csv  (186KB)
    │  catalog_enriched_folders.csv  (45KB)
    │  sessions.json  (265B)
  ├─ projects/
    │  catalog_base.csv  (1MB)
  ├─ temp/
├─ database/
  │  __init__.py  (1KB)
  │  config.py  (4KB)
  │  example_usage.py  (6KB)
  │  init_db.py  (7KB)
  │  models.py  (16KB)
  │  README.md  (6KB)
  │  requirements.txt  (265B)
  │  seed_data.py  (26KB)
  │  setup_database.py  (7KB)
├─ db_docs/
  │  table_summaries.json  (15KB)
├─ docs/
  ├─ database/
    │  status.md  (44KB)
  ├─ design/
    ├─ blueprints/
      │  Arquitectura Lógica · v0.1 — 2025-09-15.md  (1KB)
      │  Flujo Cumplimiento · ennui-rag · v0.1 — 2025-09-15.mmd  (2KB)
      │  Flujo Cumplimiento · v0.1 — 2025-09-15.md  (2KB)
    ├─ decisiones/
      │  ADR-0001 Monorepo · v0.1 — 2025-09-15.md  (1KB)
      │  ADR-0002 Seeds-vs-CSV · v0.1 — 2025-09-15.md  (1KB)
    ├─ erd-objetivo/
      │  ERD Objetivo · ennui-rag · v0.1 — 2025-09-15.md  (5KB)
      │  ERD Objetivo · ennui-rag · v0.1 — 2025-09-15.mmd  (5KB)
    ├─ vision-narrativa/
      │  Vision · ennui-rag · v0.1 — 2025-09-15.md  (6KB)
    │  README.md  (1KB)
  ├─ kb/
    ├─ snapshots/
      ├─ 2025-09-16_174208/
      ├─ legacy/
        ├─ 2025-08-23_000000/
          │  kb_ennui_rag 2025-08-23.md  (6KB)
          │  README 2025-08-23.md  (3KB)
        ├─ 2025-08-24_000000/
          │  KB_COLAB 2025-08-24.md  (45KB)
          │  kb_ennui_rag 2025-08-24.md  (5KB)
          │  README 2025-08-24.md  (4KB)
        ├─ 2025-08-25_063323/
          │  KB_COLAB.md  (80KB)
        ├─ 2025-08-25_065020/
          │  KB_COLAB.md  (80KB)
          │  README.md  (924B)
        ├─ 2025-08-25_070034/
          │  KB_ennui_rag_v1.md  (19KB)
          │  README.md  (2KB)
        ├─ 2025-08-25_072016/
          │  KB_ennui_rag_v1.md  (76KB)
          │  README.md  (2KB)
        ├─ 2025-08-25_072209/
          │  KB_ennui_rag_v1.md  (76KB)
          │  README.md  (2KB)
        ├─ 2025-08-25_072348/
          │  KB_ennui_rag_v1.md  (76KB)
          │  README.md  (2KB)
        ├─ 2025-08-25_072515/
          │  KB_ennui_rag_v1.md  (76KB)
          │  README.md  (2KB)
        ├─ 2025-08-25_073322/
          │  KB_ennui_rag_v1.md  (77KB)
          │  README.md  (2KB)
        ├─ 2025-08-26_031354/
          │  KB_ennui_rag_v1.md  (78KB)
          │  README.md  (4KB)
        ├─ 2025-08-26_033120/
          │  KB_ennui_rag_v1.md  (80KB)
          │  README.md  (2KB)
        ├─ 2025-08-26_034311/
          │  KB_ennui_rag_v1.md  (79KB)
          │  README.md  (2KB)
        ├─ 2025-08-26_034904/
          │  KB_ennui_rag_v1.md  (79KB)
          │  README.md  (2KB)
        ├─ 2025-08-26_074404/
          │  KB_ennui_rag_v1.md  (80KB)
          │  README.md  (2KB)
        ├─ 2025-08-27_013533/
          │  KB_ennui_rag_v1.md  (92KB)
          │  README.md  (4KB)
        ├─ 2025-09-02_040055/
          │  KB_ennui_rag_v1.md  (996KB)
          │  README.md  (4KB)
        ├─ 2025-09-02_040642/
          │  KB_ennui_rag_v1.md  (90KB)
          │  README.md  (2KB)
        ├─ 2025-09-02_040650/
          │  KB_ennui_rag_v1.md  (90KB)
          │  README.md  (2KB)
        ├─ 2025-09-02_041102/
          │  KB_ennui_rag_v1.md  (90KB)
          │  README.md  (2KB)
        ├─ 2025-09-02_041311/
          │  KB_ennui_rag_v1.md  (90KB)
          │  README.md  (2KB)
        ├─ 2025-09-15_000000/
          │  arbol-modulos.md  (10KB)
          │  arquitectura-flujo.md  (3KB)
          │  notas-cambio.md  (1KB)
          │  operacion-troubleshooting.md  (2KB)
          │  resumen-ejecutivo.md  (2KB)
        ├─ 2025-09-16_173725/
          │  arbol-modulos.md  (140KB)
          │  arquitectura-flujo.md  (2KB)
          │  notas-cambio.md  (1KB)
          │  operacion-troubleshooting.md  (2KB)
          │  resumen-ejecutivo.md  (2KB)
        ├─ 2025-09-16_173856/
          │  arbol-modulos.md  (140KB)
          │  arquitectura-flujo.md  (2KB)
          │  notas-cambio.md  (1KB)
          │  operacion-troubleshooting.md  (2KB)
          │  resumen-ejecutivo.md  (2KB)
        │  README.md  (2KB)
    │  index.md  (879B)
    │  README.md  (3KB)
  ├─ playbooks/
    ├─ operacion/
      │  Generar-árbol-funciones · v0.1 — 2025-09-15.md  (1KB)
    ├─ prompts/
      │  Prompt-KB-Snapshot · v0.1 — 2025-09-15.md  (1KB)
  ├─ technical/
    │  complete.md  (19KB)
    │  context.md  (4KB)
    │  development.md  (849B)
    │  persistence.md  (9KB)
  │  README.md  (2KB)
├─ notebooks/
  ├─ data/
    ├─ 1caxesJ5QtTLCf8wcsrZRmcCP1MVg65Xe/
      │  sessions.json  (147B)
    ├─ 1F3NQevlP-4m5NXImqPbibAEgtMr0B0s_/
      │  catalog_base.csv  (259KB)
      │  sessions.json  (265B)
  │  ennui-rag-v1.ipynb  (175KB)
├─ src/
  ├─ ennui_rag/
    ├─ app/
      ├─ sections/
        │  __init__.py  (333B)
        │  cierre_panel.py  (12KB)
        │  diseno_metodologico_panel.py  (13KB)
        │  enrichment_panel.py  (1KB)
        │  etapas_panel.py  (14KB)
        │  indexing_panel.py  (3KB)
        │  me_panel.py  (13KB)
        │  processing_panel.py  (30KB)
        │  program_overview_panel.py  (12KB)
        │  search_panel.py  (3KB)
        │  state_panel.py  (1KB)
      │  __init__.py  (0B)
      │  ui_streamlit.py  (37KB)
      │  utils.py  (2KB)
    ├─ enrichment/
      │  __init__.py  (0B)
      │  extractors.py  (13KB)
      │  files.py  (5KB)
      │  files.py.bak  (5KB)
      │  fingerprints.py  (8KB)
      │  folders.py  (10KB)
      │  folders.py.bak  (10KB)
      │  heuristics.py  (8KB)
      │  models.py  (1KB)
      │  primer.py  (7KB)
    ├─ indexing/
      │  __init__.py  (176B)
      │  build.py  (827B)
      │  config_utils.py  (1KB)
      │  dataframe_utils.py  (325B)
      │  models.py  (590B)
      │  normalize.py  (3KB)
      │  paths.py  (347B)
      │  README_Indexing.md  (8KB)
      │  traversal.py  (4KB)
      │  utils.py  (598B)
    ├─ io/
      │  __init__.py  (0B)
      │  db.py  (2KB)
      │  drive_io.py  (2KB)
      │  llm.py  (6KB)
    ├─ persistence/
      │  __init__.py  (501B)
      │  base.py  (3KB)
      │  common.py  (1KB)
      │  flows.py  (6KB)
      │  forms.py  (10KB)
      │  mongo.py  (5KB)
      │  programs.py  (5KB)
      │  reader.py  (4KB)
      │  supabase.py  (5KB)
    ├─ pipelines/
      │  __init__.py  (946B)
      │  enrich_pipeline.py  (10KB)
      │  enrich_supabase_pipeline.py  (10KB)
      │  index_pipeline.py  (2KB)
      │  index_pipeline.py.bak  (2KB)
      │  project_pipeline.py  (4KB)
      │  project_supabase_pipeline.py  (9KB)
    ├─ search/
      │  __init__.py  (132B)
      │  answers.py  (2KB)
      │  loader.py  (6KB)
      │  rerank.py  (2KB)
      │  retrieve.py  (5KB)
      │  search.py  (3KB)
    │  __init__.py  (22B)
    │  deps_check.py  (751B)
    │  hooks.py  (111B)
    │  settings.py  (4KB)
├─ tests/
│  .cursorignore  (478B)
│  .env  (573B)
│  .env.example  (512B)
│  .gitignore  (797B)
│  jupyter.log  (169KB)
│  Makefile  (796B)
│  pyproject.toml  (331B)
│  README.md  (2KB)
│  requirements.txt  (353B)
│  working.log  (24KB)
```

## 🧩 Módulos y API mínima
#### `database/__init__.py`
**Docstring:** Ennui-RAG Database Package

This package contains the complete database setup for the ennui-rag system,
including SQLAlchemy models, configuration, and utilities.

Modules:
- models: SQLAlchemy models based on the ER diagram
- config: Database connection configuration
- init_db: Database initialization utilities
- seed_data: Sample data seeding
- setup_database: Main orchestration script

Usage:
    from database.config import setup_database
    from database.models import Program, Cohort
**Imports:** config.DatabaseConfig, config.get_database_config, config.setup_database, models.*
**Funciones:** —
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
"""
Ennui-RAG Database Package

This package contains the complete database setup for the ennui-rag system,
including SQLAlchemy models, configuration, and utilities.

Modules:
- models: SQLAlchemy models based on the ER diagram
- config: Database connection configuration
- init_db: Database initialization utilities
- seed_data: Sample data seeding
- setup_database: Main orchestration script

Usage:
    from database.config import setup_database
    from database.models import Program, Cohort
    
    # Setup database
    config = setup_database()
    
    # Use models
    with config.get_session_context() as session:
        programs = session.query(Program).all()
"""

from .config import get_database_config, setup_database, DatabaseConfig
from .models import *

__version__ = "1.0.0"
__author__ = "Ennui-RAG Team"

…

    'Application',
    'Participation',
    'Session',
    'Attendance',
    'Mentor',
    'MentoringMatch',
    'Requirement',
    'Assignment',
    'Evidence',
    'EvidenceContext',
    'Evaluation',
    'ComplianceStatus',
    'Document',
    'Extraction',
    'StagingAttendanceRow',
    'IdentityCandidate',
    'IdentityResolution',
    'LoadBatch',
    'RagNode',
]
```
</details>

#### `database/config.py`
**Docstring:** Database configuration and connection management.
This module handles MariaDB connection setup and configuration.
**Imports:** contextlib.contextmanager, os, sqlalchemy.create_engine, sqlalchemy.exc.SQLAlchemyError, sqlalchemy.orm.sessionmaker, sqlalchemy.text
**Funciones:** get_database_config(), setup_database(echo), __init__(self), create_engine(self, echo), create_session_factory(self), get_session(self), get_session_context(self), test_connection(self), get_database_info(self)
**Clases:** DatabaseConfig[__init__, create_engine, create_session_factory, get_session, get_session_context, test_connection, get_database_info]
<details><summary>Excerpt (head/tail)</summary>

```python
"""
Database configuration and connection management.
This module handles MariaDB connection setup and configuration.
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager


class DatabaseConfig:
    """Database configuration class for MariaDB connection."""
    
    def __init__(self):
        # Default database configuration
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '3306')
        self.username = os.getenv('DB_USERNAME', 'root')
        self.password = os.getenv('DB_PASSWORD', 'password')
        self.database = os.getenv('DB_NAME', 'ennui_rag')
        
        # Construct database URL
        self.database_url = f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        
        # Create engine and session factory
        self.engine = None
        self.SessionLocal = None
        

…

            'database': self.database,
            'database_url': self.database_url.replace(self.password, '***')
        }


# Global database configuration instance
db_config = DatabaseConfig()


def get_database_config():
    """Get the global database configuration instance."""
    return db_config


def setup_database(echo=False):
    """Setup database connection with configuration."""
    config = get_database_config()
    config.create_engine(echo=echo)
    config.create_session_factory()
    return config
```
</details>

#### `database/example_usage.py`
**Docstring:** Example usage of the ennui-rag database system with MariaDB.
This script demonstrates how to use the SQLAlchemy models and database operations.
**Imports:** database.config.setup_database, database.models.*, datetime.date, datetime.datetime, os, sys
**Funciones:** main()
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
#!/usr/bin/env python3
"""
Example usage of the ennui-rag database system with MariaDB.
This script demonstrates how to use the SQLAlchemy models and database operations.
"""

import sys
import os
from datetime import datetime, date

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import setup_database
from database.models import *


def main():
    """Demonstrate database usage examples."""
    print("🔍 Ennui-RAG Database Usage Examples")
    print("=" * 50)
    
    # Setup database connection
    print("1️⃣ Setting up database connection...")
    config = setup_database()
    
    if not config.test_connection():
        print("❌ Database connection failed. Please run setup_database.py first.")
        return
    

…

        participation_summary = session.query(
            Cohort.name.label('cohort_name'),
            Program.name.label('program_name'),
            session.query(Participation).filter(Participation.cohort_id == Cohort.id).count().label('participant_count')
        ).join(Program)\
        .group_by(Cohort.id, Cohort.name, Program.name)\
        .all()
        
        print("   Participation by cohort:")
        for row in participation_summary:
            print(f"   - {row.program_name} / {row.cohort_name}: {row.participant_count} participants")
    print()
    
    print("🎉 Database usage examples completed!")
    print()
    print("💡 You can modify these examples or create your own queries using the models in database/models.py")


if __name__ == "__main__":
    main()
```
</details>

#### `database/init_db.py`
**Docstring:** Database initialization script.
This module handles MariaDB database creation, dropping, and table creation.
**Imports:** database.config.get_database_config, database.models.Base, os, sqlalchemy.create_engine, sqlalchemy.exc.OperationalError, sqlalchemy.exc.SQLAlchemyError, sqlalchemy.text, sys
**Funciones:** main(), __init__(self), drop_database(self), create_database(self), create_tables(self), drop_tables(self), recreate_database(self), verify_setup(self)
**Clases:** DatabaseInitializer[__init__, drop_database, create_database, create_tables, drop_tables, recreate_database, verify_setup]
<details><summary>Excerpt (head/tail)</summary>

```python
"""
Database initialization script.
This module handles MariaDB database creation, dropping, and table creation.
"""

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import get_database_config
from database.models import Base


class DatabaseInitializer:
    """Database initialization and management class."""
    
    def __init__(self):
        self.config = get_database_config()
    
    def drop_database(self):
        """Drop the database if it exists."""
        try:
            # Connect to MariaDB server (not specific database)
            server_url = f"mysql+pymysql://{self.config.username}:{self.config.password}@{self.config.host}:{self.config.port}"
            
            # Create temporary engine to connect to MariaDB server

…

    
    try:
        # Recreate database (drop and create)
        initializer.recreate_database()
        
        # Verify setup
        print("\n🔍 Verifying database setup...")
        if initializer.verify_setup():
            print("🎉 Database initialization completed successfully!")
        else:
            print("❌ Database verification failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```
</details>

#### `database/models.py`
**Docstring:** SQLAlchemy models for the ennui-rag database system.
Based on the ER diagram, this module defines all database tables and relationships.
**Imports:** datetime.date, datetime.datetime, sqlalchemy.Boolean, sqlalchemy.Column, sqlalchemy.Date, sqlalchemy.DateTime, sqlalchemy.ForeignKey, sqlalchemy.Integer, sqlalchemy.JSON, sqlalchemy.Numeric, sqlalchemy.String, sqlalchemy.Text, sqlalchemy.create_engine, sqlalchemy.ext.declarative.declarative_base, sqlalchemy.orm.relationship, sqlalchemy.orm.sessionmaker
**Funciones:** —
**Clases:** Program[], Cohort[], Organization[], Person[], Application[], Participation[], Session[], Attendance[], Mentor[], MentoringMatch[], Requirement[], Assignment[], Evidence[], EvidenceContext[], Evaluation[], ComplianceStatus[], Document[], Extraction[], StagingAttendanceRow[], IdentityCandidate[], IdentityResolution[], LoadBatch[], RagNode[]
<details><summary>Excerpt (head/tail)</summary>

```python
"""
SQLAlchemy models for the ennui-rag database system.
Based on the ER diagram, this module defines all database tables and relationships.
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Boolean, Numeric, Text, 
    ForeignKey, JSON, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, date

Base = declarative_base()


class Program(Base):
    """Program entity - represents training programs."""
    __tablename__ = 'programs'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    
    # Relationships
    cohorts = relationship("Cohort", back_populates="program")


class Cohort(Base):
    """Cohort entity - represents specific cohorts within programs."""
    __tablename__ = 'cohorts'

…

    inserted = Column(Integer, nullable=False, default=0)
    updated = Column(Integer, nullable=False, default=0)
    skipped = Column(Integer, nullable=False, default=0)
    errors = Column(Integer, nullable=False, default=0)
    
    # Relationships
    document = relationship("Document", back_populates="load_batches")


class RagNode(Base):
    """RagNode entity - represents RAG (Retrieval-Augmented Generation) nodes."""
    __tablename__ = 'rag_nodes'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    chunk = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    
    # Relationships
    document = relationship("Document", back_populates="rag_nodes")
```
</details>

#### `database/seed_data.py`
**Docstring:** Seed data script for the ennui-rag database.
This module creates sample data for all tables to demonstrate the system.
**Imports:** database.config.get_database_config, database.models.*, datetime.date, datetime.datetime, datetime.timedelta, decimal.Decimal, os, sys
**Funciones:** main(), __init__(self), get_session(self), close_session(self), seed_all_data(self), seed_programs(self, session), seed_cohorts(self, session), seed_organizations(self, session), seed_persons(self, session), seed_applications(self, session), seed_participations(self, session), seed_sessions(self, session), seed_attendances(self, session), seed_mentors(self, session), seed_mentoring_matches(self, session), seed_requirements(self, session), seed_assignments(self, session), seed_documents(self, session), seed_evidences(self, session), seed_evidence_contexts(self, session), seed_evaluations(self, session), seed_compliance_statuses(self, session), seed_extractions(self, session), seed_staging_attendance_rows(self, session), seed_identity_candidates(self, session), seed_identity_resolutions(self, session), seed_load_batches(self, session), seed_rag_nodes(self, session)
**Clases:** DataSeeder[__init__, get_session, close_session, seed_all_data, seed_programs, seed_cohorts, seed_organizations, seed_persons, seed_applications, seed_participations, seed_sessions, seed_attendances]
<details><summary>Excerpt (head/tail)</summary>

```python
"""
Seed data script for the ennui-rag database.
This module creates sample data for all tables to demonstrate the system.
"""

import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import get_database_config
from database.models import *


class DataSeeder:
    """Class to handle seeding the database with sample data."""
    
    def __init__(self):
        self.config = get_database_config()
        self.session = None
    
    def get_session(self):
        """Get database session."""
        if self.session is None:
            self.config.create_session_factory()
            self.session = self.config.get_session()
        return self.session

…

        print(f"    ✅ Created {len(rag_nodes)} RAG nodes")


def main():
    """Main function for data seeding."""
    print("🌱 Starting data seeding process...")
    
    seeder = DataSeeder()
    
    try:
        seeder.seed_all_data()
        print("🎉 Data seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Data seeding failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```
</details>

#### `database/setup_database.py`
**Docstring:** Main database setup script for the ennui-rag system.
This script orchestrates the complete MariaDB database setup process including:
- Database initialization (drop/create)
- Table creation
- Sample data seeding

Usage:
    python setup_database.py [--skip-seed] [--echo-sql] [--help]
**Imports:** argparse, database.config.get_database_config, database.init_db.DatabaseInitializer, database.seed_data.DataSeeder, datetime.datetime, os, pymysql, sqlalchemy, sys
**Funciones:** parse_arguments(), check_dependencies(), main(), __init__(self, echo_sql), print_banner(self), print_configuration(self), setup_database(self, skip_seed), print_summary(self, success)
**Clases:** DatabaseSetup[__init__, print_banner, print_configuration, setup_database, print_summary]
<details><summary>Excerpt (head/tail)</summary>

```python
#!/usr/bin/env python3
"""
Main database setup script for the ennui-rag system.
This script orchestrates the complete MariaDB database setup process including:
- Database initialization (drop/create)
- Table creation
- Sample data seeding

Usage:
    python setup_database.py [--skip-seed] [--echo-sql] [--help]
"""

import sys
import os
import argparse
from datetime import datetime

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import get_database_config
from database.init_db import DatabaseInitializer
from database.seed_data import DataSeeder


class DatabaseSetup:
    """Main class to orchestrate the complete database setup process."""
    
    def __init__(self, echo_sql=False):
        self.echo_sql = echo_sql

…

            response = input("🚨 This will DROP and recreate the database. Continue? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("❌ Setup cancelled by user")
                sys.exit(0)
        except KeyboardInterrupt:
            print("\n❌ Setup cancelled by user")
            sys.exit(0)
    
    # Perform database setup
    success = setup.setup_database(skip_seed=args.skip_seed)
    
    # Print summary
    setup.print_summary(success=success)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```
</details>

#### `src/ennui_rag/__init__.py`
**Funciones:** —
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
__version__ = "0.1.0"
```
</details>

#### `src/ennui_rag/app/__init__.py`
**Funciones:** —
**Clases:** —

#### `src/ennui_rag/app/sections/__init__.py`
**Imports:** cierre_panel.render_cierre_panel, diseno_metodologico_panel.render_diseno_metodologico_panel, etapas_panel.render_etapas_panel, me_panel.render_me_panel, program_overview_panel.render_program_overview
**Funciones:** —
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from .program_overview_panel import render_program_overview  # noqa: F401
from .etapas_panel import render_etapas_panel  # noqa: F401
from .diseno_metodologico_panel import render_diseno_metodologico_panel  # noqa: F401
from .cierre_panel import render_cierre_panel  # noqa: F401
from .me_panel import render_me_panel  # noqa: F401

```
</details>

#### `src/ennui_rag/app/sections/cierre_panel.py`
**Imports:** __future__.annotations, ennui_rag.persistence.programs.create_program, ennui_rag.persistence.programs.read_program, ennui_rag.persistence.programs.read_stage, ennui_rag.persistence.programs.upsert_stage, streamlit, time, typing.Any, typing.Dict, typing.List
**Funciones:** render_cierre_panel(container)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_cierre_panel; widgets: st.button, st.markdown, st.selectbox, st.text_input
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations

from typing import Dict, Any, List
import streamlit as st

from ennui_rag.persistence.programs import read_program, create_program, read_stage, upsert_stage


def render_cierre_panel(container, *, project_id: str):
    with container:
        st.subheader("📄 Cierre del programa")
        
        # Verificar que el proyecto existe
        prog = read_program(project_id) if project_id else None
        if not prog:
            st.warning("El proyecto no existe en `programs`.")
            if st.button("Iniciar definición de programa", key="btn_create_program_cierre"):
                created = create_program(project_id)
                if created.get("project_id"):
                    st.success("Proyecto creado.")
                    st.rerun()
                else:
                    st.error("No se pudo crear el proyecto.")
            return

        # Sección de documentos de cierre
        st.markdown("### 📋 Documentos de cierre")
        
        # Crear nuevo documento
        with st.expander("➕ Crear nuevo documento", expanded=False):

…

        try:
            data, updated_at = read_stage(project_id, "cierre")
            if data and data.get("documentos"):
                total_docs = len(data["documentos"])
                docs_borrador = len([d for d in data["documentos"] if d.get("status") == "borrador"])
                docs_compilados = len([d for d in data["documentos"] if d.get("status") == "compilado"])
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Total documentos", total_docs)
                with col_b:
                    st.metric("Borradores", docs_borrador)
                with col_c:
                    st.metric("Compilados", docs_compilados)
                
                st.caption(f"Última actualización: {updated_at or '—'}")
            else:
                st.info("Sin documentos de cierre")
        except Exception as e:
            st.error(f"Error leyendo estado: {e}")
```
</details>

#### `src/ennui_rag/app/sections/diseno_metodologico_panel.py`
**Imports:** __future__.annotations, datetime.datetime, datetime.timezone, ennui_rag.io.db.get_supabase, ennui_rag.persistence.programs.create_program, ennui_rag.persistence.programs.read_program, ennui_rag.persistence.programs.read_stage, ennui_rag.persistence.programs.upsert_stage, json, streamlit, time, typing.Any, typing.Dict, typing.List
**Funciones:** render_diseno_metodologico_panel(container)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_diseno_metodologico_panel; widgets: st.button, st.markdown, st.text_input
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations

from typing import Dict, Any, List
import streamlit as st

from ennui_rag.persistence.programs import read_program, create_program, read_stage, upsert_stage


def render_diseno_metodologico_panel(container, *, project_id: str):
    with container:
        # Verificar que el proyecto existe
        prog = read_program(project_id) if project_id else None
        if not prog:
            st.warning("El proyecto no existe en `programs`.")
            if st.button("Iniciar definición de programa", key="btn_create_program_diseno"):
                created = create_program(project_id)
                if created.get("project_id"):
                    st.success("Proyecto creado.")
                    st.rerun()
                else:
                    st.error("No se pudo crear el proyecto.")
            return

        # Obtener componentes activos desde la configuración del programa
        componentes_activos = prog.get('config', {}).get('componentes_activos', [])
        
        if not componentes_activos:
            st.info("No hay componentes activos. Ve a Overview para activar los componentes del programa.")
            return
        

…

        try:
            data, updated_at = read_stage(project_id, "diseno_metodologico")
            if data:
                archivos_count = data.get("archivos_count", 0)
                procesado_llm = data.get("procesado_llm", False)
                editado_manual = data.get("editado_manual", False)
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Archivos", archivos_count)
                with col_b:
                    st.metric("LLM", "✅" if procesado_llm else "❌")
                with col_c:
                    st.metric("Editado", "✅" if editado_manual else "❌")
                
                st.caption(f"Última actualización: {updated_at or '—'}")
            else:
                st.info("Sin datos de diseño metodológico")
        except Exception as e:
            st.error(f"Error leyendo estado: {e}")
```
</details>

#### `src/ennui_rag/app/sections/enrichment_panel.py`
**Imports:** __future__.annotations, contextlib.redirect_stdout, ennui_rag.pipelines.enrich_pipeline.run_enrich, io, streamlit, typing.Dict
**Funciones:** render_enrichment_panel(container)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_enrichment_panel; widgets: st.button, st.markdown
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/app/sections/enrichment_panel.py
from __future__ import annotations
import io
from contextlib import redirect_stdout
from typing import Dict
import streamlit as st

# Usamos exactamente el runner existente hoy
from ennui_rag.pipelines.enrich_pipeline import run_enrich


def render_enrichment_panel(container, *, env: str, proj: Dict[str, str]):
    with container:
        st.info("Este panel usa el `enrich_pipeline.run_enrich(env)` existente.")
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Ejecutar enriquecimiento ⚗️"):
                buf = io.StringIO()
                try:
                    with redirect_stdout(buf):
                        run_enrich(env=env)
                except Exception as e:
                    st.exception(e)
                finally:
                    logs = buf.getvalue()
                    if logs.strip():
                        st.success("Enriquecimiento ejecutado (logs):")
                        st.code(logs)
                    else:
                        st.warning("No se capturaron logs. Verifica implementación de run_enrich.")
        with col2:
            st.caption("Notas")
            st.markdown(
                "- `run_enrich(env)` ya ejecuta enriquecimiento completo.\n"
                "- Genera descripciones, etiquetas, entidades y embeddings (cuando aplica).\n"
                "- Persiste resultados idempotentes en CSV y BD opcionales.\n"
            )
```
</details>

#### `src/ennui_rag/app/sections/etapas_panel.py`
**Imports:** __future__.annotations, ennui_rag.persistence.flows.create_flow, ennui_rag.persistence.flows.create_step, ennui_rag.persistence.flows.delete_flow, ennui_rag.persistence.flows.list_flows, ennui_rag.persistence.flows.list_steps, ennui_rag.persistence.flows.reorder_steps, ennui_rag.persistence.forms.add_question, ennui_rag.persistence.forms.create_form, ennui_rag.persistence.forms.create_form_version, ennui_rag.persistence.forms.link_form_to_step, ennui_rag.persistence.forms.list_form_runs, ennui_rag.persistence.forms.list_form_versions, ennui_rag.persistence.forms.list_forms, ennui_rag.persistence.forms.list_published_versions, ennui_rag.persistence.forms.list_questions, ennui_rag.persistence.forms.publish_form_version, ennui_rag.persistence.programs.create_program, ennui_rag.persistence.programs.read_program, ennui_rag.persistence.programs.read_stage, ennui_rag.persistence.programs.upsert_stage, json, streamlit, typing.Any, typing.Dict, typing.List, typing.Tuple
**Funciones:** _json_dumps_pretty(obj), render_etapas_panel(container)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_etapas_panel; widgets: st.button, st.checkbox, st.markdown, st.selectbox, st.text_input
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations

from typing import Dict, Any, List, Tuple

import json
import streamlit as st

from ennui_rag.persistence.programs import (
    read_program,
    create_program,
    read_stage,
    upsert_stage,
)
from ennui_rag.persistence.flows import (
    create_flow,
    list_flows,
    delete_flow,
    create_step,
    list_steps,
    reorder_steps,
)
from ennui_rag.persistence.forms import (
    create_form,
    list_forms,
    create_form_version,
    publish_form_version,
    add_question,
    list_questions,
    link_form_to_step,
    list_form_versions,

…

            st.markdown("#### Funcionalidades planificadas:")
            st.markdown("- **Módulos**: estructura de contenido del programa")
            st.markdown("- **Lecciones**: unidades individuales de aprendizaje")
            st.markdown("- **Tareas**: ejercicios y evaluaciones")
            st.markdown("- **Formularios**: encuestas de satisfacción y evaluación")
            st.markdown("- **Vincular artefactos**: bindings con archivos y recursos")
            st.markdown("- **Acciones**: Validar/Ingerir/Derivar LLM/Exportar")

        # Tab 3: Acompañamiento
        with etapa_tab[2]:
            st.markdown("### 🤝 Acompañamiento")
            st.info("Panel en desarrollo: capacidad, sesiones, reportes, evidencias")
            
            # Placeholder para funcionalidad futura
            st.markdown("#### Funcionalidades planificadas:")
            st.markdown("- **Capacidad**: gestión de recursos y mentores")
            st.markdown("- **Sesiones**: programación y seguimiento")
            st.markdown("- **Reportes**: cumplimiento y métricas")
            st.markdown("- **Evidencias**: videos, transcripciones, documentos")
            st.markdown("- **Tablero**: estado general del acompañamiento")
```
</details>

#### `src/ennui_rag/app/sections/indexing_panel.py`
**Imports:** __future__.annotations, ennui_rag.pipelines.ensure_catalog, os, pandas, streamlit, typing.Any, typing.Dict, typing.Optional, utils.run_index_safe, utils.safe_read_csv
**Funciones:** render_indexing_panel(container)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_indexing_panel; widgets: st.button, st.dataframe, st.write
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/app/sections/indexing_panel.py
from __future__ import annotations
import os
from typing import Any, Dict, Optional
import pandas as pd
import streamlit as st

from ennui_rag.pipelines import ensure_catalog
from ..utils import safe_read_csv, run_index_safe

def render_indexing_panel(container, *, proj: Dict[str, Any], env: str, folder_id_input: str, max_items: Optional[int]):
    with container:
        st.subheader("📄 Catálogo del proyecto")
        if not proj:
            st.info("Selecciona un proyecto en la barra lateral (Folder ID o recientes).")
            return

        pid = proj.get("project_id")
        data_dir = proj.get("data_dir") or f"data/{pid}"
        st.write(f"**Project ID:** `{pid}`")
        st.write(f"**Data dir:** `{data_dir}`")

        a1, a2, a3 = st.columns([1, 1, 1])
        with a1:
            if st.button("Asegurar catálogo 💾"):
                try:
                    csv_path = ensure_catalog(pid, force=False, persist=True)
                    st.session_state["catalog_csv"] = csv_path
                    df = safe_read_csv(csv_path)
                    if df is not None and not df.empty:

…

                    res = run_index_safe(env=env, folder_id=fid, max_items=max_items)
                    st.success("Indexación ejecutada.")
                    if isinstance(res, pd.DataFrame):
                        st.caption("Resultado de indexación (vista rápida):")
                        st.dataframe(res.head(100), use_container_width=True, height=430)
                    else:
                        st.caption(f"Tipo de resultado: {type(res).__name__}")
                        st.text(str(res)[:1000])
                except Exception as e:
                    st.exception(e)

        with a3:
            if st.button("Ver catálogo actual 📑"):
                csv_path = st.session_state.get("catalog_csv") or os.path.join(data_dir, "catalog_base.csv")
                df = safe_read_csv(csv_path)
                if df is not None:
                    st.info(f"Mostrando: {csv_path}")
                    st.dataframe(df, use_container_width=True, height=430)
                else:
                    st.warning("No se encontró el catálogo. Pulsa 'Asegurar catálogo' o 'Indexar ahora'.")
```
</details>

#### `src/ennui_rag/app/sections/me_panel.py`
**Imports:** __future__.annotations, ennui_rag.persistence.programs.create_program, ennui_rag.persistence.programs.read_program, ennui_rag.persistence.programs.read_stage, ennui_rag.persistence.programs.upsert_stage, streamlit, typing.Any, typing.Dict, typing.List
**Funciones:** render_me_panel(container)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_me_panel; widgets: st.button, st.date_input, st.file_uploader, st.markdown, st.number_input, st.selectbox, st.text_input
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations

from typing import Dict, Any, List
import streamlit as st

from ennui_rag.persistence.programs import read_program, create_program, read_stage, upsert_stage


def render_me_panel(container, *, project_id: str):
    with container:
        st.subheader("📊 Monitoreo y Evaluación")
        
        # Verificar que el proyecto existe
        prog = read_program(project_id) if project_id else None
        if not prog:
            st.warning("El proyecto no existe en `programs`.")
            if st.button("Iniciar definición de programa", key="btn_create_program_me"):
                created = create_program(project_id)
                if created.get("project_id"):
                    st.success("Proyecto creado.")
                    st.rerun()
                else:
                    st.error("No se pudo crear el proyecto.")
            return

        # Sección de catálogo de indicadores
        st.markdown("### 📋 Catálogo de indicadores")
        
        # Crear nuevo indicador
        with st.expander("➕ Crear nuevo indicador", expanded=False):

…

        except Exception as e:
            st.error(f"Error leyendo dashboard: {e}")

        # Integración con Looker
        st.markdown("---")
        st.markdown("### 🔗 Integración con Looker")
        
        st.info("Configuración de integración con Looker en desarrollo")
        st.markdown("**Funcionalidades planificadas:**")
        st.markdown("- **Dashboard embebido**: mostrar dashboards de Looker en la UI")
        st.markdown("- **Sincronización automática**: valores se reflejan en tiempo real")
        st.markdown("- **Filtros por proyecto**: contexto automático del proyecto activo")
        st.markdown("- **Exportación**: generar reportes desde Looker")
        
        # Placeholder para configuración
        looker_url = st.text_input("URL base de Looker", placeholder="https://looker.company.com", key="looker_url_me")
        looker_project = st.text_input("Proyecto en Looker", placeholder="ennui_rag_programs", key="looker_project_me")
        
        if st.button("💾 Guardar configuración", key="save_looker_config"):
            st.info("Configuración de Looker en desarrollo")
```
</details>

#### `src/ennui_rag/app/sections/processing_panel.py`
**Imports:** __future__.annotations, contextlib.redirect_stdout, ennui_rag.app.utils.run_with_logs, ennui_rag.app.utils.safe_read_csv, ennui_rag.pipelines.ensure_catalog, ennui_rag.pipelines.ensure_catalog_and_enrich_supabase, ennui_rag.pipelines.project_pipeline.project_status, ennui_rag.pipelines.project_status, ennui_rag.pipelines.run_enrich, ennui_rag.pipelines.run_index, enrichment_panel.render_enrichment_panel, importlib.util, io, os, pandas, pathlib.Path, plotly.express, plotly.graph_objects, streamlit, sys, tempfile, time, typing.Any, typing.Dict, typing.Optional
**Funciones:** verify_project_access(project_id), check_catalog_exists(project_id), create_folder_tree_diagram(df, max_depth), _show_folder_structure_text(df, max_depth), render_processing_panel(container), _run_full_processing_pipeline(project_id, env), _render_indexing_summary(project_id, csv_path, catalog_df), _render_enrichment_panel(project_id, catalog_df, env), _run_enrichment_pipeline(project_id, env)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_enrichment_panel, render_indexing_panel, render_processing_panel; widgets: st.button, st.dataframe, st.markdown, st.plotly_chart, st.slider, st.write
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/app/sections/processing_panel.py
from __future__ import annotations
import os
import io
import time
from contextlib import redirect_stdout
from typing import Dict, Any, Optional
from pathlib import Path
import pandas as pd
import streamlit as st
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from ennui_rag.pipelines import (
    ensure_catalog, 
    run_index, 
    run_enrich,
    project_status,
    ensure_catalog_and_enrich_supabase
)
from ennui_rag.app.utils import safe_read_csv, run_with_logs


def verify_project_access(project_id: str) -> tuple[bool, str]:
    """
    Verifica si el proyecto existe y es accesible en Google Drive.

…

            output_placeholder.text(f"✅ Enriquecimiento completado. Logs:\n{logs}")
        except Exception as e:
            output_placeholder.text(f"❌ Error en enriquecimiento: {str(e)}")
            st.error(f"Error en el enriquecimiento: {e}")
            return
        
        # Limpiar la UI de progreso
        progress_container.empty()
        output_container.empty()
        
        # Mostrar mensaje de éxito y recargar
        st.success("🎉 ¡Enriquecimiento completado! Los datos han sido enriquecidos con descripciones y embeddings.")
        st.info("Recargando la vista...")
        
        # Forzar rerun para mostrar la vista actualizada
        st.rerun()
        
    except Exception as e:
        st.error(f"Error general en el enriquecimiento: {e}")
        output_placeholder.text(f"❌ Error general: {str(e)}")
```
</details>

#### `src/ennui_rag/app/sections/program_overview_panel.py`
**Imports:** __future__.annotations, datetime.datetime, datetime.timezone, ennui_rag.io.db.get_supabase, ennui_rag.persistence.programs.create_program, ennui_rag.persistence.programs.read_program, json, streamlit, typing.Any, typing.Dict, typing.List, typing.Tuple
**Funciones:** _now_iso(), _json_dumps_pretty(obj), render_program_overview(container)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_program_overview; widgets: st.button, st.checkbox, st.date_input, st.markdown, st.text_input
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations

from typing import Dict, Any, List, Tuple

import json
import streamlit as st
from datetime import datetime, timezone

from ennui_rag.persistence.programs import (
    read_program,
    create_program,
)
from ennui_rag.io.db import get_supabase


def _now_iso() -> str:
    """Devuelve la fecha actual en formato ISO"""
    return datetime.now(timezone.utc).isoformat()




def _json_dumps_pretty(obj: Any) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return "{}"


def render_program_overview(container):

…

                    "code": new_code,
                    "title": new_title,
                    "actors": new_actores,
                    "config": config_data,
                    "updated_at": _now_iso(),
                }
                
                result = sb.table("programs").update(update_payload).eq("project_id", project_id).execute()
                
                if result.data:
                    st.success("✅ Todos los cambios guardados exitosamente")
                    st.rerun()
                else:
                    st.error("❌ Error guardando los cambios")
                    
            except Exception as e:
                st.error(f"❌ Error guardando: {e}")



```
</details>

#### `src/ennui_rag/app/sections/search_panel.py`
**Imports:** __future__.annotations, ennui_rag.search.search_llm, pandas, streamlit, typing.Dict, typing.Optional
**Funciones:** render_search_panel(container)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_search_panel; widgets: st.checkbox, st.dataframe, st.form, st.form_submit_button, st.markdown, st.number_input, st.selectbox, st.text_input, st.write
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations
from typing import Dict, Optional
import pandas as pd
import streamlit as st

from ennui_rag.search import search_llm

def render_search_panel(container, *, proj: Dict[str, str]):
    with container:
        st.subheader("🔎 Búsqueda (LLM-aided)")
        if not proj:
            st.info("Selecciona un proyecto primero (en la barra lateral).")
            return

        pid = proj.get("project_id")
        if not pid:
            st.warning("No se encontró project_id en sesión.")
            return

        with st.form("search_form"):
            query = st.text_input("Consulta", placeholder="ej.: actas comité cronograma")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                k = st.number_input("Candidatos (k)", 10, 200, 60, step=10)
            with col2:
                n = st.number_input("Top N (rerank)", 5, 50, 12, step=1)
            with col3:
                kind = st.selectbox("Tipo", ["(todos)", "file", "folder"], index=0)
            with col4:
                as_answer = st.checkbox("Respuesta breve + citas", value=False)

…

                    line = f"• **{c['title']}** — {c['path']}"
                    if c.get("web_url"):
                        line += f" — [Abrir]({c['web_url']})"
                    st.markdown(line)
            return

        # Tabla de resultados
        df = search_llm(query, project_id=pid,
                        k=int(k), n=int(n), kind=_kind,
                        by_path=by_path or None, by_mime=by_mime or None,
                        modified_from=modified_from or None,
                        modified_to=modified_to or None,
                        debug=debug)
        if isinstance(df, pd.DataFrame) and not df.empty:
            st.success(f"{len(df)} resultados")
            show_cols = ["llm_score","title","name","path","topic","tags","mime","web_url"]
            exists = [c for c in show_cols if c in df.columns]
            st.dataframe(df[exists].head(200), use_container_width=True)
        else:
            st.info("Sin resultados")
```
</details>

#### `src/ennui_rag/app/sections/state_panel.py`
**Imports:** __future__.annotations, ennui_rag.pipelines.project_status, streamlit, typing.Dict
**Funciones:** render_state_panel(container)
**Clases:** —
**UI (heurística Streamlit):** hooks: render_state_panel; widgets: st.button, st.markdown
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/app/sections/state_panel.py
from __future__ import annotations
from typing import Dict
import streamlit as st
from ennui_rag.pipelines import project_status


def render_state_panel(container, *, proj: Dict[str, str]):
    with container:
        st.subheader("ℹ️ Estado")
        if not proj:
            st.info("Selecciona un proyecto para ver su estado.")
            return
        if st.button("Actualizar estado 🧭"):
            try:
                status = project_status(proj.get("project_id"))
                st.json(status)
            except Exception as e:
                st.exception(e)

        st.markdown("---")
        st.caption("Ayuda rápida")
        st.markdown(
            "- **Seleccionar proyecto**: pega un *Folder ID* o elige uno reciente.\n"
            "- **Asegurar catálogo**: crea/actualiza `catalog_base.csv` y persiste (si hay credenciales).\n"
            "- **Indexar ahora**: ejecuta `run_index(env, folder_id, max_items)`.\n"
            "- **Estado**: muestra metadatos del proyecto (última indexación, conteos, rutas).\n"
        )
```
</details>

#### `src/ennui_rag/app/ui_streamlit.py`
**Imports:** __future__.annotations, datetime.datetime, datetime.timezone, ennui_rag.persistence.programs.read_program, ennui_rag.pipelines.project_supabase_pipeline.list_recent_projects_supabase, ennui_rag.search.search_llm, enrichment_panel.render_enrichment_panel, indexing_panel.render_indexing_panel, json, os, pandas, pathlib.Path, sections.cierre_panel.render_cierre_panel, sections.diseno_metodologico_panel.render_diseno_metodologico_panel, sections.etapas_panel.render_etapas_panel, sections.me_panel.render_me_panel, sections.processing_panel.render_processing_panel, sections.program_overview_panel.render_program_overview, state_panel.render_state_panel, streamlit, typing.Dict
**Funciones:** _get_active_project(), _set_active_project(pid), _rerun(), _create_project_session(project_id), _get_program_name(project_id), _format_date_for_display(date_str), _render_program_menu(), _render_files_menu(), _render_project_selector_accordion(), _render_header(), _render_footer(), _render_section_header(section_name, breadcrumbs), _render_program_selector_main(), _render_app_config_modal(), render_search_panel(proj), _render_sidebar(proj), main()
**Clases:** —
**UI (heurística Streamlit):** hooks: render_cierre_panel, render_diseno_metodologico_panel, render_etapas_panel, render_me_panel, render_processing_panel, render_program_overview, render_search_panel, render_state_panel; widgets: st.button, st.checkbox, st.dataframe, st.form, st.form_submit_button, st.markdown, st.number_input, st.selectbox, st.sidebar, st.text_input, st.write
<details><summary>Excerpt (head/tail)</summary>

```python
# ui_streamlit.py
# Streamlit App para ennui-rag con panel de Búsqueda (LLM-aided) + SIDEBAR y rerun compatible
from __future__ import annotations

import os
from typing import Dict

import pandas as pd
import streamlit as st

# Paneles existentes (seguros ante ausencia)
try:
    from indexing_panel import render_indexing_panel
except Exception:
    render_indexing_panel = None

try:
    from enrichment_panel import render_enrichment_panel
except Exception:
    render_enrichment_panel = None

try:
    from state_panel import render_state_panel
except Exception:
    render_state_panel = None

try:
    from sections.program_overview_panel import render_program_overview
except Exception:
    render_program_overview = None

…

                        env="dev"
                    )
                except Exception as e:
                    st.exception(e)
            else:
                st.info("Panel de Procesamiento no disponible.")
        elif archivos_tab == "Búsqueda":
            render_search_panel(proj)
        elif archivos_tab == "Estadísticas":
            if render_state_panel:
                try:
                    render_state_panel(st.container(), proj=proj)
                except Exception as e:
                    st.exception(e)
            else:
                st.info("Panel de State no disponible.")


if __name__ == "__main__":
    main()
```
</details>

#### `src/ennui_rag/app/utils.py`
**Imports:** __future__.annotations, contextlib.redirect_stdout, ennui_rag.pipelines.run_index, io, os, pandas, streamlit, typing.Any, typing.Dict, typing.Optional, typing.Tuple
**Funciones:** get_proj(), set_proj(proj), _ensure_logbuf(), log(msg), clear_global_logs(), get_global_logs_text(), safe_read_csv(path), run_index_safe(env, folder_id, max_items), run_with_logs(), show_global_console(container)
**Clases:** —
**UI (heurística Streamlit):** widgets: st.button
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/app/utils.py
from __future__ import annotations
import os, io
from contextlib import redirect_stdout
from typing import Any, Dict, Optional, Tuple

import pandas as pd
import streamlit as st

from ennui_rag.pipelines import run_index

# --- Session helpers ---
def get_proj() -> Optional[Dict[str, Any]]:
    return st.session_state.get("proj")

def set_proj(proj: Dict[str, Any]) -> None:
    st.session_state["proj"] = proj or {}

# --- Global log buffer helpers ---
def _ensure_logbuf():
    if "GLOBAL_LOGS" not in st.session_state:
        st.session_state["GLOBAL_LOGS"] = []  # list[str]

def log(msg: str) -> None:
    _ensure_logbuf()
    st.session_state["GLOBAL_LOGS"].append(str(msg))

def clear_global_logs() -> None:
    st.session_state["GLOBAL_LOGS"] = []


…

    logs = buf.getvalue()
    if logs:
        try:
            log(logs)
        except Exception:
            pass
    return result, logs

# --- UI: consola global ---
def show_global_console(container) -> None:
    with container:
        st.subheader("🧰 Consola global de logs")
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("Limpiar consola 🧹"):
                clear_global_logs()
                st.toast("Consola limpiada", icon="🧼")
        with c2:
            st.caption("Se muestran los logs capturados de indexación/enriquecimiento.")
        st.text_area("", value=get_global_logs_text(), height=220)
```
</details>

#### `src/ennui_rag/deps_check.py`
**Imports:** dotenv.load_dotenv, googleapiclient.discovery, importlib.metadata.PackageNotFoundError, importlib.metadata.version, pinecone.Pinecone, psycopg2, pydantic.BaseModel, pymongo.MongoClient, supabase.create_client
**Funciones:** _v(p), print_versions(), smoke_imports()
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from importlib.metadata import version, PackageNotFoundError

def _v(p: str) -> str:
    try:
        return version(p)
    except PackageNotFoundError:
        return "—"

def print_versions():
    mods = {m: _v(m) for m in [
        "pandas","tenacity","openai","pydantic","sqlalchemy","pymongo",
        "dnspython","pinecone","jedi","supabase","psycopg2-binary"
    ]}
    print("✅ Versiones:", mods)

def smoke_imports():
    from supabase import create_client  # noqa
    import psycopg2  # noqa
    from pymongo import MongoClient  # noqa
    from pinecone import Pinecone  # noqa
    import googleapiclient.discovery  # noqa
    from pydantic import BaseModel  # noqa
    from dotenv import load_dotenv  # noqa
    print("✅ Imports OK")
```
</details>

#### `src/ennui_rag/enrichment/__init__.py`
**Funciones:** —
**Clases:** —

#### `src/ennui_rag/enrichment/extractors.py`
**Docstring:** ennui_rag.enrichment.extractors

Estrategias de extracción de snippets "ligeros" por tipo de archivo
(Google Drive). No usa variables globales; todo se inyecta por parámetros.

Depende de:
- .models: FileRow, SnippetResult
- googleapiclient (para descargas/export)
- pandas (opcional, sólo para Excel)

Diseño:
- Cada extractor implementa: matches(row) y extract(drive, row, ...)
- Dispatcher: get_snippet(drive, row, max_chars=1200, ...) que recorre
  los extractores en orden y devuelve el primer S
**Imports:** __future__.annotations, googleapiclient.errors.HttpError, googleapiclient.http.MediaIoBaseDownload, io, models.FileRow, models.SnippetResult, pandas, typing.Any, typing.List, typing.Optional
**Funciones:** _trim(text, max_chars), _safe_decode(data), _get_ext(row), _drive_export_to_text(drive, file_id, mime_target), _drive_get_media_head(drive, file_id), _drive_download_bytes(drive, file_id), _excel_snippet_from_bytes(data), get_snippet(drive, row), matches(self, row), extract(self, drive, row), matches(self, row), extract(self, drive, row), matches(self, row), extract(self, drive, row), matches(self, row), extract(self, drive, row), matches(self, row), extract(self, drive, row)
**Clases:** SnippetExtractor[matches, extract], GDocExtractor[matches, extract], SheetCsvExtractor[matches, extract], ExcelExtractor[matches, extract], TextLikeExtractor[matches, extract], HttpError[]
<details><summary>Excerpt (head/tail)</summary>

```python
"""ennui_rag.enrichment.extractors

Estrategias de extracción de snippets "ligeros" por tipo de archivo
(Google Drive). No usa variables globales; todo se inyecta por parámetros.

Depende de:
- .models: FileRow, SnippetResult
- googleapiclient (para descargas/export)
- pandas (opcional, sólo para Excel)

Diseño:
- Cada extractor implementa: matches(row) y extract(drive, row, ...)
- Dispatcher: get_snippet(drive, row, max_chars=1200, ...) que recorre
  los extractores en orden y devuelve el primer SnippetResult no vacío.

Calidades devueltas en SnippetResult.quality:
- "full": export de documento completo (p.ej., Google Docs/Sheets via export)
- "head": lectura parcial/cabecera (CSV/TXT/Excel sample)
- "none": sin texto disponible
"""
from __future__ import annotations

from typing import Any, Optional, List
import io

try:  # Import on demand; evita fallar si el entorno aún no instala dependencias
    from googleapiclient.http import MediaIoBaseDownload  # type: ignore
    from googleapiclient.errors import HttpError  # type: ignore
except Exception:  # pragma: no cover - entorno sin googleapiclient
    MediaIoBaseDownload = None  # type: ignore

…

                head_max_bytes=head_max_bytes,
                bytes_chunk=bytes_chunk,
            )
            if res and isinstance(res.text, str) and res.text.strip():
                return res
        except Exception:
            # Fallar suave: probamos siguiente extractor
            continue
    return SnippetResult()


__all__ = [
    "SnippetExtractor",
    "GDocExtractor",
    "SheetCsvExtractor",
    "ExcelExtractor",
    "TextLikeExtractor",
    "DEFAULT_EXTRACTORS",
    "get_snippet",
]
```
</details>

#### `src/ennui_rag/enrichment/files.py`
**Imports:** __future__.annotations, dataclasses.dataclass, dataclasses.field, extractors.get_snippet, fingerprints._now_iso, fingerprints.file_fingerprint, heuristics.as_list, heuristics.heuristic_file_enrichment, heuristics.normalize_tags, io.llm, json, models.EnrichedFile, models.FileRow, primer.ProgramPreset, primer.build_primer, typing.Any, typing.Dict, typing.Optional
**Funciones:** _ensure_primer(ctx), enrich_file_row(ctx, row)
**Clases:** Limits[], Flags[], Maps[], EnrichmentContext[]
<details><summary>Excerpt (head/tail)</summary>

```python
# =============================================
# files.py · ennui-rag · v0.1.1 (2025-08-24)
# - Usa heuristics.normalize_tags / heuristics.as_list
# =============================================
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import json

from .models import FileRow, EnrichedFile
from .extractors import get_snippet
from .heuristics import (
    heuristic_file_enrichment,
    normalize_tags,
    as_list,
)
from .fingerprints import file_fingerprint, _now_iso
from .primer import ProgramPreset, build_primer
from ..io import llm as llm_api
@dataclass
class Limits:
    file_max_chars: int = 1200
    file_max_output_tokens: int = 220
    file_temperature: float = 0.2
    head_max_lines: int = 60
    head_max_bytes: int = 256 * 1024
    bytes_chunk: int = 1024 * 1024



…

        summary_80w=summary,
        tags=tags,
        topic_label=topic,
        entities=entities,
        confidence=conf,
        notes_short=notes,
        fingerprint=fp,
        llm_recipe=ctx.recipe_version,
        indexed_at=_now_iso(),
    )
    return rec


__all__ = [
    "Limits",
    "Flags",
    "Maps",
    "EnrichmentContext",
    "enrich_file_row",
]
```
</details>

#### `src/ennui_rag/enrichment/fingerprints.py`
**Docstring:** Huella digital (fingerprints) e utilidades deterministas para idempotencia.

Diseño:
- Fingerprint de archivo = sha256 de campos estables + hash del snippet recortado.
- Fingerprint de carpeta = sha256 de (folder_id, modified, depth, recipe_ver) + conjunto
  ordenado de claves "file_id|fingerprint" de los hijos usados en el resumen.

Este módulo no depende del resto del paquete. Solo usa stdlib.
Si pandas está disponible, se aprovecha para detectar NaN con seguridad.
**Imports:** __future__.annotations, datetime.datetime, datetime.timezone, hashlib, json, pandas, typing.Iterable, typing.List, typing.Mapping, typing.Optional, typing.Sequence, typing.Tuple, typing.Union
**Funciones:** _sha256(text), _now_iso(), coalesce(), is_nan_like(v), safe_str(v, max_len), safe_int(v), norm_iso8601(v), file_fingerprint(row, snippet_text), child_key_fp(file_id, file_fp), folder_fingerprint(folder_row, child_keys_fps), g(k), g(k)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/enrichment/fingerprints.py
# -*- coding: utf-8 -*-
"""
Huella digital (fingerprints) e utilidades deterministas para idempotencia.

Diseño:
- Fingerprint de archivo = sha256 de campos estables + hash del snippet recortado.
- Fingerprint de carpeta = sha256 de (folder_id, modified, depth, recipe_ver) + conjunto
  ordenado de claves "file_id|fingerprint" de los hijos usados en el resumen.

Este módulo no depende del resto del paquete. Solo usa stdlib.
Si pandas está disponible, se aprovecha para detectar NaN con seguridad.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Iterable, List, Mapping, Optional, Sequence, Tuple, Union

try:
    import pandas as pd  # opcional
except Exception:  # pragma: no cover
    pd = None  # type: ignore

# --------------------------------------------------------------------------
# API pública
# --------------------------------------------------------------------------


…

    parts.extend(ordered_children)
    return _sha256("|".join(parts))

# --------------------------------------------------------------------------
# Ejemplos de uso (comentados)
# --------------------------------------------------------------------------
# file_fp = file_fingerprint(
#     row={"file_id":"abc", "modified":"2025-08-21T12:00:00Z", "size_bytes": 1024, "mime_type":"text/csv"},
#     snippet_text="col1,col2\n1,2\n",
#     snippet_max_chars=1200,
# )
#
# folder_fp = folder_fingerprint(
#     folder_row={"file_id":"F123", "modified":"2025-08-21T12:00:00Z", "depth":3},
#     child_keys_fps=[
#         child_key_fp("abc", file_fp),
#         child_key_fp("def", "deadbeef..."),
#     ],
#     recipe_ver="files:v1.0|folders:v1.0",
# )
```
</details>

#### `src/ennui_rag/enrichment/folders.py`
**Imports:** __future__.annotations, dataclasses.dataclass, dataclasses.field, fingerprints._now_iso, fingerprints.folder_fingerprint, heuristics.as_list, heuristics.heuristic_folder_enrichment, heuristics.normalize_tags, heuristics.safe_get, io.llm, json, models.EnrichedFolder, models.FileRow, pandas, primer.ProgramPreset, primer.build_primer, typing.Any, typing.Dict, typing.List, typing.Optional
**Funciones:** _ensure_primer(ctx), child_line_for_prompt(file_like, maxlen), select_folder_children(folder_row, files_join_df), pick_representative_children(children_df, k), _build_child_like(item), _build_user_payload_for_folder(folder_row, child_rows, primer_text), enrich_folder_row(ctx, folder_row, files_join_df)
**Clases:** Limits[], Flags[], Maps[], EnrichmentContext[]
<details><summary>Excerpt (head/tail)</summary>

```python
# =============================================
# folders.py · ennui-rag · v0.1.1 (2025-08-24)
# - Usa heuristics.safe_get / heuristics.as_list / heuristics.normalize_tags
# - Importa heuristic_folder_enrichment desde heuristics
# =============================================
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
import json
import pandas as pd

from .models import FileRow, EnrichedFolder
from .fingerprints import folder_fingerprint, _now_iso
from .primer import ProgramPreset, build_primer
from .heuristics import (
    heuristic_folder_enrichment,
    normalize_tags,
    as_list,
    safe_get,
)
from ..io import llm as llm_api
@dataclass
class Limits:
    folder_children_max: int = 15
    folder_child_line_chars: int = 260
    folder_max_output_tokens: int = 240
    folder_temperature: float = 0.2



…

        fingerprint=fp,
        llm_recipe=ctx.recipe_version,
        indexed_at=_now_iso(),
        relative_path=folder_row.relative_path,
        name=folder_row.name,
        children_count_total=int(num_kids_total),
        children_count_used=int(min(num_kids_total, ctx.limits.folder_children_max)),
    )
    return rec


__all__ = [
    "Limits",
    "Flags",
    "Maps",
    "EnrichmentContext",
    "select_folder_children",
    "pick_representative_children",
    "enrich_folder_row",
]
```
</details>

#### `src/ennui_rag/enrichment/heuristics.py`
**Imports:** __future__.annotations, re, typing.Any, typing.Iterable, typing.List, typing.Mapping, typing.Sequence, unicodedata
**Funciones:** safe_get(obj, key, default), slugify_token(s), as_list(x), normalize_tags(tags), basename_no_ext(name), guess_basic_tags(), heuristic_file_enrichment(row_like), heuristic_folder_enrichment(folder_row_like, num_children, sample_tags)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# enrichment/heuristics.py
# -----------------------------------------
# Heurísticas "costo cero" (sin LLM) para enriquecer
# archivos y carpetas cuando no hay snippet o la señal es baja.
#
# Devuelve estructuras ligeras compatibles con los modelos de salida:
# - Archivos:  title_canonical, summary_80w, tags, topic_label, entities, confidence, notes_short
# - Carpetas:  title_canonical, summary_120w, tags, topic_label, entities, confidence, notes_short
#
# Uso:
#   from enrichment.heuristics import heuristic_file_enrichment, heuristic_folder_enrichment
#
# Nota: Mantener estas heurísticas deterministas e idempotentes.
# -----------------------------------------

from __future__ import annotations

from typing import Any, Iterable, List, Mapping, Sequence
import re
import unicodedata

__all__ = [
    "heuristic_file_enrichment",
    "heuristic_folder_enrichment",
    "normalize_tags",
    "guess_basic_tags",
    "safe_get",
    "as_list",
]


…

    name = str(safe_get(folder_row_like, "name") or "")[:80] or "Carpeta"
    rel = str(safe_get(folder_row_like, "relative_path") or "")

    # deduce tags desde muestra de hijos
    tags = normalize_tags(sample_tags or [], maxn=8)

    summary = (
        f"Carpeta con aproximadamente {int(num_children)} elementos. "
        f"Ruta: {rel or '/'}."
    )

    return {
        "title_canonical": name,
        "summary_120w": summary[:700],  # margen cómodo
        "tags": tags,
        "topic_label": "otro",
        "entities": [],
        "confidence": 0.35,
        "notes_short": "Generado sin LLM (carpeta con hijos insuficientemente enriquecidos).",
    }
```
</details>

#### `src/ennui_rag/enrichment/models.py`
**Imports:** pydantic.BaseModel, pydantic.Field, typing.List, typing.Optional
**Funciones:** —
**Clases:** FileRow[], SnippetResult[], EnrichedFile[], EnrichedFolder[]
<details><summary>Excerpt (head/tail)</summary>

```python
# models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class FileRow(BaseModel):
    drive_id: str
    file_id: str
    name: str
    relative_path: str
    extension: Optional[str] = ""
    mime_type: Optional[str] = ""
    modified: Optional[str] = None
    size_bytes: Optional[int] = None
    depth: int = 0

class SnippetResult(BaseModel):
    text: str = ""
    quality: str = "none"   # full|head|none
    bytes_used: int = 0

class EnrichedFile(BaseModel):
    drive_id: str
    file_id: str
    title_canonical: str
    summary_80w: str
    tags: List[str] = []
    topic_label: str = "otro"
    entities: List[str] = []
    confidence: float = 0.3
    notes_short: str = ""
    fingerprint: str
    llm_recipe: str
    indexed_at: str

class EnrichedFolder(BaseModel):
    drive_id: str
    folder_id: str
    title_canonical: str
    summary_120w: str
    tags: List[str] = []
    topic_label: str = "otro"
    entities: List[str] = []
    confidence: float = 0.35
    notes_short: str = ""
    fingerprint: str
    llm_recipe: str
    indexed_at: str
    relative_path: str
    name: str
    children_count_total: int
    children_count_used: int
```
</details>

#### `src/ennui_rag/enrichment/primer.py`
**Imports:** __future__.annotations, pydantic.BaseModel, pydantic.Field, typing.Dict, typing.List, typing.Optional, yaml
**Funciones:** _dedup_keep_order(items), _truncate(s, max_chars), _join_cap(items, sep, max_items, max_chars), build_primer(preset, glossary), load_presets_from_yaml(path), load_single_preset_from_yaml(path, name), default_preset()
**Clases:** ProgramPreset[]
<details><summary>Excerpt (head/tail)</summary>

```python
# primer.py
# -----------------------------------------------------------------------------
# Construcción de "primer" (contexto breve) para el LLM a partir de un preset
# de programa (aceleración, incubación, etc.) y un glosario opcional.
#
# Dependencias: solo estándar + pydantic (ya usada en el proyecto).
# -----------------------------------------------------------------------------

from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


# =========================
# Modelos y utilidades
# =========================

class ProgramPreset(BaseModel):
    """
    Preset declarativo del dominio del programa (p.ej., aceleración) que
    guía la redacción de resúmenes y etiquetas.

    Recomendación: guarda instancias en configs/presets.yaml y cárgalas
    con load_presets_from_yaml(...) (abajo).
    """
    name: str = Field(default="aceleracion_std")
    version: str = Field(default="1.0")

    # Núcleo semántico

…

def load_single_preset_from_yaml(path: str, name: str) -> ProgramPreset:
    """
    Atajo para cargar un preset específico por nombre desde un YAML.
    """
    presets = load_presets_from_yaml(path)
    if name not in presets:
        raise KeyError(f"No se encontró el preset '{name}' en {path}.")
    return presets[name]


# =========================
# Preset por defecto (fallback)
# =========================

def default_preset() -> ProgramPreset:
    """
    Devuelve un preset por defecto (aceleración estándar).
    Útil como fallback si no se ha configurado un YAML.
    """
    return ProgramPreset()
```
</details>

#### `src/ennui_rag/hooks.py`
**Imports:** os
**Funciones:** apply_runtime_flags()
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
import os
def apply_runtime_flags():
    os.environ.setdefault('APP_DEBUG','0')

TEST_VAR = "v5 desde hooks.py"
```
</details>

#### `src/ennui_rag/indexing/__init__.py`
**Imports:** build.build_catalog_dataframe, build.save_catalog_csv, normalize.chunked, normalize.normalize_df_to_records, paths.CONFIG_PATH, paths.CSV_PATH, paths.project_csv_path
**Funciones:** —
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from .build import build_catalog_dataframe, save_catalog_csv
from .normalize import normalize_df_to_records, chunked
from .paths import CSV_PATH, CONFIG_PATH, project_csv_path
```
</details>

#### `src/ennui_rag/indexing/build.py`
**Imports:** dataframe_utils.ensure_extension, io.drive_io.get_drive_service, pandas, pathlib.Path, paths.CSV_PATH, traversal.walk_drive_tree, typing.Optional
**Funciones:** build_catalog_dataframe(root_id, max_items), save_catalog_csv(df, path)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from pathlib import Path
import pandas as pd
from typing import Optional
from .traversal import walk_drive_tree
from .dataframe_utils import ensure_extension
from ..io.drive_io import get_drive_service
from .paths import CSV_PATH

def build_catalog_dataframe(root_id: str, max_items: Optional[int] = None) -> pd.DataFrame:
    svc = get_drive_service()
    print("⏳ Recorriendo Drive (puede tardar)…")
    rows = walk_drive_tree(svc, root_id, max_items=max_items)
    df = pd.DataFrame.from_records(rows)
    df = ensure_extension(df)
    df.sort_values(["relative_path", "name"], inplace=True, kind="stable")
    return df

def save_catalog_csv(df: pd.DataFrame, path: str = CSV_PATH) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
```
</details>

#### `src/ennui_rag/indexing/config_utils.py`
**Imports:** json, os, paths.CONFIG_PATH, re, typing.Optional
**Funciones:** extract_folder_id(text), load_or_ask_root_id()
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
import json, os, re
from typing import Optional
from .paths import CONFIG_PATH

def extract_folder_id(text: str) -> Optional[str]:
    if not text: return None
    t = text.strip()
    if "/" not in t and " " not in t:
        return t
    m = re.search(r"/folders/([A-Za-z0-9_\-]+)", t) or re.search(r"[?&]id=([A-Za-z0-9_\-]+)", t)
    return m.group(1) if m else None

def load_or_ask_root_id() -> str:
    """Fallback interactivo si no hay root guardado (útil en prototipos/Colab)."""
    cfg_exists = os.path.exists(CONFIG_PATH)
    if cfg_exists:
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            rid = cfg.get("root_folder_id")
            if rid:
                print(f"📌 Usando raíz previa: {rid}")
                return rid
        except Exception:
            pass
    link_or_id = input("🔗 Pega link/ID de la carpeta raíz de Drive: ").strip()
    rid = extract_folder_id(link_or_id)
    if not rid:
        raise ValueError("No pude extraer un folder ID válido.")
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"root_folder_id": rid}, f, ensure_ascii=False, indent=2)
    print(f"✅ Raíz guardada en {CONFIG_PATH}")
    return rid
```
</details>

#### `src/ennui_rag/indexing/dataframe_utils.py`
**Imports:** pandas
**Funciones:** ensure_extension(df), _ext(name)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
import pandas as pd

def ensure_extension(df: pd.DataFrame) -> pd.DataFrame:
    def _ext(name: str) -> str:
        s = str(name or "")
        return s.rsplit(".", 1)[-1].lower() if "." in s else ""
    if "name" not in df.columns:
        df["name"] = ""
    df["extension"] = df["name"].map(_ext)
    return df
```
</details>

#### `src/ennui_rag/indexing/models.py`
**Imports:** pydantic.BaseModel, pydantic.Field, typing.Optional
**Funciones:** —
**Clases:** CatalogItem[]
<details><summary>Excerpt (head/tail)</summary>

```python
from typing import Optional
from pydantic import BaseModel, Field

class CatalogItem(BaseModel):
    project_id: str
    session_id: str
    root_folder_id: str
    file_id: str
    drive_id: str
    name: Optional[str] = None
    relative_path: Optional[str] = None
    type: Optional[str] = Field(default=None, pattern="^(file|folder)?$")
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None
    modified: Optional[str] = None
    owner: Optional[str] = None
    web_url: Optional[str] = None
    extension: Optional[str] = None
    indexed_at: str
```
</details>

#### `src/ennui_rag/indexing/normalize.py`
**Imports:** math, models.CatalogItem, pandas, typing.Any, typing.Dict, typing.List, typing.Optional, utils.chunked, utils.now_iso
**Funciones:** _to_int_or_none(x), normalize_df_to_records(df, project_id, session_id, root_folder_id)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/indexing/normalize.py
from typing import List, Dict, Any, Optional
import math, pandas as pd
from .models import CatalogItem
from .utils import now_iso, chunked  # reexportamos chunked aquí para conveniencia

def _to_int_or_none(x):
    if x is None: return None
    if isinstance(x, int): return x
    try:
        if isinstance(x, float) and math.isnan(x): return None
        return int(float(x))
    except Exception:
        return None

def normalize_df_to_records(
    df: pd.DataFrame,
    project_id: Optional[str] = None,
    session_id: Optional[str] = None,
    root_folder_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    req = ["file_id","drive_id","name","relative_path","type","mime_type",
           "size_bytes","modified","owner","web_url","extension"]
    missing = [c for c in req if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas esperadas en df: {missing}")

    # Fallback: si vienen en el DF, úsalos
    pj = project_id or df.attrs.get("project_id") or df.get("project_id")
    ss = session_id or df.attrs.get("session_id") or df.get("session_id")

…

            "root_folder_id": rf or pj,
            "file_id": (row.get("file_id") or "")[:255],
            "drive_id": (row.get("drive_id") or "")[:255],
            "name": None if pd.isna(row.get("name")) else str(row.get("name")),
            "relative_path": None if pd.isna(row.get("relative_path")) else str(row.get("relative_path")),
            "type": None if pd.isna(row.get("type")) else str(row.get("type")),
            "mime_type": None if pd.isna(row.get("mime_type")) else str(row.get("mime_type")),
            "size_bytes": _to_int_or_none(row.get("size_bytes")),
            "modified": None if pd.isna(row.get("modified")) else str(row.get("modified")),
            "owner": None if pd.isna(row.get("owner")) else str(row.get("owner")),
            "web_url": None if pd.isna(row.get("web_url")) else str(row.get("web_url")),
            "extension": None if pd.isna(row.get("extension")) else str(row.get("extension")),
            "indexed_at": ts,
        }
        try:
            CatalogItem(**rec)
            out.append(rec)
        except Exception as e:
            print("⚠️ Registro inválido, se omite:", rec.get("file_id"), "\n", e)
    return out
```
</details>

#### `src/ennui_rag/indexing/paths.py`
**Imports:** pathlib.Path
**Funciones:** project_csv_path(project_id)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from pathlib import Path

# Compatibilidad con código existente:
CONFIG_PATH = "catalog_config.json"
CSV_PATH = "data/projects/catalog_base.csv"  # usado hoy por save_catalog_csv

# Nuevo helper para cache por proyecto:
DATA_DIR = Path("data")

def project_csv_path(project_id: str) -> Path:
    return DATA_DIR / project_id / "catalog_base.csv"
```
</details>

#### `src/ennui_rag/indexing/traversal.py`
**Imports:** io.drive_io.get_drive_service, io.drive_io.get_file_meta, io.drive_io.list_children, pandas, time, typing.Dict, typing.List, typing.Optional, typing.Tuple, utils.is_folder
**Funciones:** walk_drive_tree(svc, root_id, max_items)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
import time, pandas as pd
from typing import Dict, List, Optional, Tuple
from ..io.drive_io import get_drive_service, get_file_meta as drv_get_file_meta, list_children as drv_list_children
from .utils import is_folder

def walk_drive_tree(svc, root_id: str, max_items: Optional[int] = None) -> List[Dict]:
    """DFS con soporte de Shortcuts y Shared Drives."""
    rows: List[Dict] = []

    root_meta = drv_get_file_meta(svc, root_id)
    if root_meta.get("mimeType") == "application/vnd.google-apps.shortcut":
        target = (root_meta.get("shortcutDetails") or {}).get("targetId")
        if not target:
            raise RuntimeError("Atajo de raíz sin targetId.")
        print(f"🔁 Raíz es atajo. Usando targetId: {target}")
        root_meta = drv_get_file_meta(svc, target)

    real_root_id = root_meta.get("id")
    root_name = root_meta.get("name", "root")
    rows.append({
        "file_id": real_root_id,
        "name": root_name,
        "relative_path": f"/{root_name}",
        "type": "folder",
        "mime_type": root_meta.get("mimeType"),
        "size_bytes": None,
        "modified": root_meta.get("modifiedTime"),
        "owner": (root_meta.get("owners", [{}])[0] or {}).get("emailAddress"),
        "web_url": root_meta.get("webViewLink"),
        "drive_id": real_root_id,

…

                    "web_url": f.get("webViewLink"),
                    "drive_id": real_root_id,
                }
                rows.append(rec)
                scanned += 1
                if folder:
                    stack.append((rec["file_id"], rec["relative_path"]))

                now = time.time()
                if now - last_print >= 3:
                    print(f"… indexados: {scanned} items (carpetas en stack: {len(stack)})")
                    last_print = now

                if max_items and scanned >= max_items:
                    print(f"🧪 Corte por max_items={max_items}")
                    return rows
            if not page_token:
                break

    return rows
```
</details>

#### `src/ennui_rag/indexing/utils.py`
**Imports:** datetime.datetime, datetime.timezone, typing.Any, typing.Dict, typing.Generator, typing.Iterable, typing.List
**Funciones:** is_folder(mime), now_iso(), chunked(iterable, size)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from typing import Iterable, Dict, List, Any, Generator
from datetime import datetime, timezone

def is_folder(mime: str) -> bool:
    return (mime or "").endswith("folder")

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def chunked(iterable: Iterable[Dict[str, Any]], size: int) -> Generator[List[Dict[str, Any]], None, None]:
    batch: List[Dict[str, Any]] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch
```
</details>

#### `src/ennui_rag/io/__init__.py`
**Funciones:** —
**Clases:** —

#### `src/ennui_rag/io/db.py`
**Imports:** __future__.annotations, os, pymongo.MongoClient, pymongo.database.Database, supabase.Client, supabase.create_client, typing.Optional
**Funciones:** _resolve_supabase_url(), _resolve_supabase_key(), get_supabase(), get_mongo(db_name)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/io/db.py
from __future__ import annotations

import os
from typing import Optional
from supabase import create_client, Client
from pymongo import MongoClient
from pymongo.database import Database

# Puedes ajustar este default si quieres alinear con tu settings.py
DEFAULT_SUPABASE_REF = os.getenv("SUPABASE_REF_DEFAULT", "refmyhnmpuerwpfjihtw")

def _resolve_supabase_url() -> str:
    """
    Resuelve SUPABASE_URL:
    - Usa SUPABASE_URL si está.
    - Si no, construye con SUPABASE_REF -> https://<ref>.supabase.co
    - Si tampoco hay ref, usa DEFAULT_SUPABASE_REF.
    """
    url = os.getenv("SUPABASE_URL")
    if url:
        return url
    ref = os.getenv("SUPABASE_REF") or DEFAULT_SUPABASE_REF
    return f"https://{ref}.supabase.co"

def _resolve_supabase_key() -> str:
    """
    Resuelve la API key:
    - Usa SUPABASE_KEY si está.
    - Si no, cae a SB_SECRET (service role).

…

    Devuelve un cliente Supabase funcionando aun si solo tienes SB_SECRET.
    También deja SUPABASE_URL/SUPABASE_KEY en el entorno para compatibilidad.
    """
    url = _resolve_supabase_url()
    key = _resolve_supabase_key()
    os.environ.setdefault("SUPABASE_URL", url)
    os.environ.setdefault("SUPABASE_KEY", key)
    return create_client(url, key)

def get_mongo(db_name: Optional[str] = None) -> Database:
    """
    Devuelve una Database de Mongo leyendo MONGO_URI y (opcional) MONGO_DB.
    """
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise RuntimeError("Falta MONGO_URI en el entorno.")
    client = MongoClient(uri)
    return client[db_name or os.getenv("MONGO_DB", "ennui_rag")]

__all__ = ["get_supabase", "get_mongo"]
```
</details>

#### `src/ennui_rag/io/drive_io.py`
**Imports:** google.oauth2.service_account.Credentials, googleapiclient.discovery.build, googleapiclient.errors.HttpError, pathlib.Path, tenacity.retry, tenacity.retry_if_exception_type, tenacity.stop_after_attempt, tenacity.wait_exponential, typing.Dict, typing.List, typing.Optional, typing.Tuple
**Funciones:** get_drive_service(), _is_retryable_http(e), get_file_meta(service, file_id), list_children(service, folder_id, page_token), list_files_from_config(config, service)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/io/drive_io.py
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Dynamically find service_account.json in configs/credentials/
SERVICE_ACCOUNT_FILE = "/home/alvaro_e_mur/ennui-rag/configs/credentials/service_account.json"

def get_drive_service():
    creds = Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE),
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)

def _is_retryable_http(e: HttpError) -> bool:
    try:
        s = e.resp.status
        return s == 429 or (500 <= s < 600)
    except Exception:
        return False

retry_policy = retry(
    reraise=True,
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    retry=retry_if_exception_type(HttpError),

…

        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        fields=fields,
        pageToken=page_token,
        pageSize=1000,
    ).execute()
    return resp.get("files", []), resp.get("nextPageToken")

def list_files_from_config(config: Dict, service=None) -> List[Dict]:
    folder_id = (config or {}).get("folder_id")
    if not folder_id:
        raise ValueError("No se definió 'folder_id' en el config")
    service = service or get_drive_service()
    out: List[Dict] = []
    token = None
    while True:
        items, token = list_children(service, folder_id, token)
        out.extend(items)
        if not token: break
    return out
```
</details>

#### `src/ennui_rag/io/llm.py`
**Docstring:** ennui_rag.io.llm

Wrapper único para llamadas a LLM en modo JSON.
Compatible con `files.py` (función pública `llm_json`).

Características:
- Usa OpenAI (cliente oficial `from openai import OpenAI`).
- `response_format={"type":"json_object"}` para obtener JSON estricto.
- Reintentos simples con backoff exponencial (2 reintentos por defecto).
- Sanitiza la salida y siempre retorna `dict` (o `{}` en fallo).

Variables de entorno relevantes:
- `OPENAI_API_KEY`           : clave del API
- `OPENAI_JS
**Imports:** __future__.annotations, json, openai.OpenAI, os, time, typing.Any, typing.Dict, typing.Optional
**Funciones:** _get_client(), _strip_markers(s), _safe_json_loads(s), llm_json()
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
"""ennui_rag.io.llm

Wrapper único para llamadas a LLM en modo JSON.
Compatible con `files.py` (función pública `llm_json`).

Características:
- Usa OpenAI (cliente oficial `from openai import OpenAI`).
- `response_format={"type":"json_object"}` para obtener JSON estricto.
- Reintentos simples con backoff exponencial (2 reintentos por defecto).
- Sanitiza la salida y siempre retorna `dict` (o `{}` en fallo).

Variables de entorno relevantes:
- `OPENAI_API_KEY`           : clave del API
- `OPENAI_JSON_MODEL`        : modelo para JSON-mode (por defecto: "gpt-4o-mini")
- `OPENAI_TIMEOUT_SECS`      : timeout en segundos (por defecto: 60)
- `OPENAI_MAX_RETRIES`       : reintentos adicionales (por defecto: 2)

Ejemplo:
    resp = llm_json(
        user_payload={"foo":"bar"},
        system="Eres un asistente…",
        max_tokens=220,
        temperature=0.2,
    )
"""
from __future__ import annotations

import json
import os
import time

…

                temperature=float(temperature),
                max_tokens=int(max_tokens),
                timeout=_timeout,  # soportado por el SDK v1
            )
            text = (resp.choices[0].message.content or "") if resp and resp.choices else ""
            return _safe_json_loads(text)
        except Exception as e:  # pragma: no cover - tolera errores de red/servicio
            last_err = e
            if attempt < _retries:
                # backoff exponencial: 0.5s, 1s, 2s…
                time.sleep(0.5 * (2**attempt))
                continue
            # último intento falló
            break

    # Fallo definitivo → retorna dict vacío
    return {}


__all__ = ["llm_json"]
```
</details>

#### `src/ennui_rag/persistence/__init__.py`
**Imports:** base.CatalogStore, base.persist_catalog_df, mongo.MongoStore, reader.get_supabase_status, reader.read_catalog_from_supabase, reader.read_catalog_with_fallback, reader.read_enriched_data_from_supabase, supabase.SupabaseStore
**Funciones:** —
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from .base import CatalogStore, persist_catalog_df
from .supabase import SupabaseStore
from .mongo import MongoStore
from .reader import (
    read_catalog_from_supabase,
    read_enriched_data_from_supabase,
    read_catalog_with_fallback,
    get_supabase_status
)

__all__ = [
    "CatalogStore",
    "persist_catalog_df",
    "SupabaseStore",
    "MongoStore",
    "read_catalog_from_supabase",
    "read_enriched_data_from_supabase",
    "read_catalog_with_fallback",
    "get_supabase_status"
]
```
</details>

#### `src/ennui_rag/persistence/base.py`
**Imports:** __future__.annotations, abc.ABC, abc.abstractmethod, common.chunked, common.deduplicate_by_file_and_drive, datetime.datetime, indexing.normalize_df_to_records, math, numpy, pandas, re, typing.Any, typing.Dict, typing.Iterable, typing.List, typing.Optional
**Funciones:** _sanitize_df(df), persist_catalog_df(df, stores, batch_size, deduplicate, project_id, session_id, root_folder_id), prepare(self), upsert(self, records, batch_size)
**Clases:** CatalogStore[prepare, upsert]
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/persistence/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, Dict, Any, List, Optional
import pandas as pd
import numpy as np
import math, re
from datetime import datetime

from ..indexing import normalize_df_to_records
from .common import chunked, deduplicate_by_file_and_drive

_INT_HINTS = re.compile(r"(?:^|_)(size|bytes?|count|num|pages?|version|epoch|quota|length)(?:_|$)", re.I)

def _sanitize_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    # Inf → NaN
    df = df.replace([np.inf, -np.inf], np.nan)
    # Forzar int-like
    cand = set()
    for col in df.columns:
        if _INT_HINTS.search(col):
            cand.add(col)
        elif pd.api.types.is_float_dtype(df[col]):
            s = df[col].dropna()
            if len(s) and np.all(np.isclose(s.values, np.round(s.values), equal_nan=True)):
                cand.add(col)
    for col in cand:
        try:

…

) -> Dict[str, int]:
    """Normaliza df → records y persiste en todos los stores (con limpieza y dedup)."""
    if deduplicate:
        df = deduplicate_by_file_and_drive(df)
    df = _sanitize_df(df)

    # Pasamos contexto al normalizador (soluciona el scope de project/session/root)
    records = normalize_df_to_records(
        df,
        project_id=project_id,
        session_id=session_id,
        root_folder_id=root_folder_id,
    )

    results = {}
    for store in stores:
        store.prepare()
        processed = store.upsert(records, batch_size=batch_size)
        results[store.__class__.__name__] = processed
    return results
```
</details>

#### `src/ennui_rag/persistence/common.py`
**Imports:** __future__.annotations, datetime.datetime, numpy, pandas, typing.Any, typing.Dict, typing.Iterable, typing.List
**Funciones:** chunked(iterable, size), _parse_dt_safe(x), deduplicate_by_file_and_drive(df)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/persistence/common.py
from __future__ import annotations
from typing import Iterable, Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime

def chunked(iterable: Iterable[Dict[str, Any]], size: int) -> Iterable[List[Dict[str, Any]]]:
    batch: List[Dict[str, Any]] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

def _parse_dt_safe(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    try:
        return datetime.fromisoformat(str(x).replace("Z","+00:00"))
    except Exception:
        return None

def deduplicate_by_file_and_drive(df: pd.DataFrame) -> pd.DataFrame:
    """Quita duplicados por (file_id, drive_id) conservando el 'modified' más reciente."""
    if df.empty:
        return df
    tmp = df.copy()
    tmp["_modified_dt"] = tmp["modified"].map(_parse_dt_safe) if "modified" in tmp.columns else None
    tmp.sort_values(["file_id","drive_id","_modified_dt"], inplace=True, kind="stable")
    out = tmp.drop_duplicates(subset=["file_id","drive_id"], keep="last").drop(columns=["_modified_dt"])
    return out
```
</details>

#### `src/ennui_rag/persistence/flows.py`
**Imports:** __future__.annotations, datetime.datetime, datetime.timezone, ennui_rag.io.db.get_supabase, ennui_rag.persistence.programs.read_program, supabase.Client, typing.Any, typing.Dict, typing.List, typing.Optional
**Funciones:** _client(), _now_iso(), _flow_exists(flow_id), create_flow(project_id, name, audience), list_flows(project_id), delete_flow(flow_id), _next_step_order(flow_id), create_step(flow_id, name), list_steps(flow_id), reorder_steps(flow_id, new_order)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from supabase import Client

from ennui_rag.io.db import get_supabase
from ennui_rag.persistence.programs import read_program


def _client() -> Client:
    return get_supabase()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _flow_exists(flow_id: str) -> bool:
    try:
        sb = _client()
        resp = sb.table("program_flows").select("id").eq("id", flow_id).limit(1).execute()
        return bool(resp.data)
    except Exception as e:
        print(f"❌ _flow_exists error (table=program_flows): {e}")
        return False


def create_flow(project_id: str, name: str, audience: Optional[str] = None) -> Dict[str, Any]:

…

                sb.table("flow_steps").update({"step_order": idx, "updated_at": _now_iso()}).eq("id", step_id).eq("flow_id", flow_id).execute()
                updated += 1
            except Exception as inner:
                print(f"❌ reorder_steps item error (table=flow_steps): {inner}")
        return {"updated": updated}
    except Exception as e:
        print(f"❌ reorder_steps error (table=flow_steps): {e}")
        return {"error": str(e)}


__all__ = [
    "create_flow",
    "list_flows",
    "delete_flow",
    "create_step",
    "list_steps",
    "reorder_steps",
]


```
</details>

#### `src/ennui_rag/persistence/forms.py`
**Imports:** __future__.annotations, datetime.datetime, datetime.timezone, ennui_rag.io.db.get_supabase, ennui_rag.persistence.programs.read_program, supabase.Client, typing.Any, typing.Dict, typing.List, typing.Optional
**Funciones:** _client(), _now_iso(), _form_exists(form_id), _version_exists(form_version_id), create_form(project_id, name, audience), list_forms(project_id), _next_form_version(form_id), create_form_version(form_id), list_form_versions(form_id), list_published_versions(form_id), _count_questions(form_version_id), publish_form_version(form_version_id), _next_q_order(form_version_id), add_question(form_version_id, q_code, q_label, q_type, q_options, required, q_order), list_questions(form_version_id), link_form_to_step(project_id, flow_id, step_id, form_version_id, cohort, flow_mode), list_form_runs(step_id)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from supabase import Client

from ennui_rag.io.db import get_supabase
from ennui_rag.persistence.programs import read_program


def _client() -> Client:
    return get_supabase()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _form_exists(form_id: str) -> bool:
    try:
        sb = _client()
        resp = sb.table("program_forms").select("id").eq("id", form_id).limit(1).execute()
        return bool(resp.data)
    except Exception as e:
        print(f"❌ _form_exists error (table=program_forms): {e}")
        return False


def _version_exists(form_version_id: str) -> bool:

…

    except Exception as e:
        print(f"❌ list_form_runs error (table=form_runs): {e}")
        return []


__all__ = [
    "create_form",
    "list_forms",
    "create_form_version",
    "publish_form_version",
    "add_question",
    "list_questions",
    "link_form_to_step",
    # helpers for UI
    "list_form_versions",
    "list_published_versions",
    "list_form_runs",
]


```
</details>

#### `src/ennui_rag/persistence/mongo.py`
**Imports:** __future__.annotations, math, pymongo.UpdateOne, pymongo.collection.Collection, pymongo.errors.BulkWriteError, typing.Any, typing.Dict, typing.Iterable, typing.Optional
**Funciones:** _is_nan(x), _clean_record(rec), __init__(self, collection, name), _safe_create_index(self, keys), prepare(self), upsert(self, records, batch_size), _flush()
**Clases:** MongoStore[__init__, _safe_create_index, prepare, upsert]
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/persistence/mongo.py
from __future__ import annotations

from typing import Iterable, Dict, Any, Optional
import math

from pymongo.collection import Collection
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError


def _is_nan(x: Any) -> bool:
    try:
        return isinstance(x, float) and math.isnan(x)
    except Exception:
        return False


def _clean_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Devuelve una copia de `rec` sin claves con valores None/NaN.
    Útil para no guardar `folder_id: null`, etc., que rompen índices únicos.
    """
    out = {}
    for k, v in rec.items():
        if v is None or _is_nan(v):
            continue
        out[k] = v
    return out


…

                    "drive_id": clean.get("drive_id"),
                    "folder_id": clean.get("folder_id"),
                }
            else:
                # Sin file_id ni folder_id no hay clave natural -> omitimos
                continue

            # Sanidad mínima: si faltan project_id o drive_id también omitimos
            if not filt.get("project_id") or not filt.get("drive_id"):
                continue

            ops_batch.append(UpdateOne(filt, {"$set": clean}, upsert=True))
            pending += 1

            if pending >= batch_size:
                _flush()

        # Flush final
        _flush()
        return total_ops
```
</details>

#### `src/ennui_rag/persistence/programs.py`
**Imports:** __future__.annotations, datetime.datetime, datetime.timezone, ennui_rag.io.db.get_supabase, supabase.Client, typing.Any, typing.Dict, typing.Optional, typing.Tuple
**Funciones:** _client(), _now_iso(), read_program(project_id), create_program(project_id), read_stage(project_id, stage), upsert_stage(project_id, stage, data)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple
from datetime import datetime, timezone

from supabase import Client

from ennui_rag.io.db import get_supabase


def _client() -> Client:
    return get_supabase()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_program(project_id: str) -> Optional[Dict[str, Any]]:
    """
    Lee una fila de `programs` por project_id.
    Devuelve None si no existe.
    """
    try:
        sb = _client()
        resp = (
            sb.table("programs")
            .select("*")
            .eq("project_id", project_id)
            .limit(1)

…

        resp = (
            sb.table("program_stages")
            .upsert(payload, on_conflict="project_id,stage", returning="representation")
            .execute()
        )
        rows = resp.data or []
        return rows[0] if rows else payload
    except Exception as e:
        print(f"❌ upsert_stage error: {e}")
        return {"project_id": project_id, "stage": stage, "data": data, "error": str(e)}


__all__ = [
    "read_program",
    "create_program",
    "read_stage",
    "upsert_stage",
]


```
</details>

#### `src/ennui_rag/persistence/reader.py`
**Docstring:** Reader para cargar datos desde Supabase en lugar de CSV.
Permite que todos los pipelines lean desde la base de datos.
**Imports:** __future__.annotations, io.db.get_supabase, pandas, supabase.SupabaseStore, typing.Any, typing.Dict, typing.List, typing.Optional
**Funciones:** read_catalog_from_supabase(project_id, table, limit), read_enriched_data_from_supabase(project_id, files_table, folders_table, limit), read_catalog_with_fallback(project_id, table, fallback_to_csv, csv_path, limit), get_supabase_status(project_id, table)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/persistence/reader.py
"""
Reader para cargar datos desde Supabase en lugar de CSV.
Permite que todos los pipelines lean desde la base de datos.
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional
import pandas as pd
from .supabase import SupabaseStore
from ..io.db import get_supabase

def read_catalog_from_supabase(
    project_id: str, 
    table: str = "catalog_drive",
    limit: Optional[int] = None
) -> pd.DataFrame:
    """
    Lee el catálogo completo desde Supabase para un proyecto específico.
    Reemplaza la lectura de catalog_base.csv.
    """
    try:
        client = get_supabase()
        store = SupabaseStore(client, table=table)
        
        # Leer datos desde Supabase
        records = store.select_by_project(project_id, limit=limit)
        
        if not records:
            print(f"⚠️ No se encontraron registros en Supabase para project_id: {project_id}")
            return pd.DataFrame()

…

        store = SupabaseStore(client, table=table)
        
        total_count = store.count()
        project_count = store.count_by_project(project_id)
        
        return {
            "table": table,
            "total_records": total_count,
            "project_records": project_count,
            "accessible": True
        }
        
    except Exception as e:
        return {
            "table": table,
            "total_records": 0,
            "project_records": 0,
            "accessible": False,
            "error": str(e)
        }
```
</details>

#### `src/ennui_rag/persistence/supabase.py`
**Imports:** __future__.annotations, base.CatalogStore, common.chunked, supabase.Client, typing.Any, typing.Dict, typing.Iterable, typing.List, typing.Optional
**Funciones:** __init__(self, client, table, on_conflict), prepare(self), upsert(self, records, batch_size), select_all(self, limit), select_by_project(self, project_id, limit), select_by_ids(self, file_ids, drive_id), count(self), count_by_project(self, project_id)
**Clases:** SupabaseStore[__init__, prepare, upsert, select_all, select_by_project, select_by_ids, count, count_by_project]
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/persistence/supabase.py
from __future__ import annotations
from typing import Iterable, Dict, Any, List, Optional
from supabase import Client
from .base import CatalogStore
from .common import chunked

class SupabaseStore(CatalogStore):
    def __init__(self, client: Client, table: str = "catalog_drive", on_conflict: str = "project_id,file_id,drive_id"):
        self.client = client
        self.table = table
        self.on_conflict = on_conflict
        self._keys = [k.strip() for k in on_conflict.split(",") if k.strip()]

    def prepare(self) -> None:
        try:
            self.client.table(self.table).select("*").limit(1).execute()
            print(f"✅ SupabaseStore: tabla '{self.table}' accesible")
        except Exception as e:
            print(f"ℹ️ SupabaseStore: tabla '{self.table}' no accesible aún:", e)

    def upsert(self, records: Iterable[Dict[str, Any]], batch_size: int = 500) -> int:
        total = 0
        for batch in chunked(records, batch_size):
            # dedup intra-batch por clave
            if self._keys:
                seen = set(); uniq = []
                for r in batch:
                    key = tuple(r.get(k) for k in self._keys)
                    if key in seen:

…

            print(f"❌ SupabaseStore error en select_by_ids: {e}")
            return []

    def count(self) -> int:
        """Cuenta el total de registros en la tabla"""
        try:
            response = self.client.table(self.table).select("file_id", count="exact").limit(1).execute()
            return response.count or 0
        except Exception as e:
            print(f"❌ SupabaseStore error en count: {e}")
            return 0

    def count_by_project(self, project_id: str) -> int:
        """Cuenta registros por project_id"""
        try:
            response = self.client.table(self.table).select("file_id", count="exact").eq("project_id", project_id).limit(1).execute()
            return response.count or 0
        except Exception as e:
            print(f"❌ SupabaseStore error en count_by_project: {e}")
            return 0
```
</details>

#### `src/ennui_rag/pipelines/__init__.py`
**Imports:** enrich_pipeline.run_enrich, enrich_supabase_pipeline.enrich_existing_project, enrich_supabase_pipeline.run_enrich_supabase, index_pipeline.run_index, project_pipeline.ensure_catalog, project_pipeline.list_recent_projects, project_pipeline.project_status, project_pipeline.select_project, project_supabase_pipeline.ensure_catalog_and_enrich_supabase, project_supabase_pipeline.list_recent_projects_supabase, project_supabase_pipeline.project_status_supabase, project_supabase_pipeline.reprocess_project_supabase, project_supabase_pipeline.select_project_supabase
**Funciones:** —
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from .index_pipeline import run_index
from .enrich_pipeline import run_enrich
from .project_pipeline import (
    select_project, 
    ensure_catalog, 
    project_status, 
    list_recent_projects
)
from .enrich_supabase_pipeline import (
    run_enrich_supabase,
    enrich_existing_project
)
from .project_supabase_pipeline import (
    select_project_supabase,
    ensure_catalog_and_enrich_supabase,
    project_status_supabase,
    list_recent_projects_supabase,
    reprocess_project_supabase
)

__all__ = [
    # Pipelines originales
    "run_index",
    "run_enrich", 
    "select_project",
    "ensure_catalog",
    "project_status",
    "list_recent_projects",
    
    # Nuevos pipelines de Supabase
    "run_enrich_supabase",
    "enrich_existing_project",
    "select_project_supabase",
    "ensure_catalog_and_enrich_supabase",
    "project_status_supabase",
    "list_recent_projects_supabase",
    "reprocess_project_supabase"
]
```
</details>

#### `src/ennui_rag/pipelines/enrich_pipeline.py`
**Imports:** __future__.annotations, enrichment.files.EnrichmentContext, enrichment.files.enrich_file_row, enrichment.folders.EnrichmentContext, enrichment.folders.enrich_folder_row, enrichment.folders.select_folder_children, enrichment.models.FileRow, indexing.paths.project_csv_path, io.db.get_mongo, io.db.get_supabase, json, numpy, pandas, pathlib.Path, persistence.mongo.MongoStore, persistence.reader.read_catalog_from_supabase, persistence.reader.read_enriched_data_from_supabase, persistence.supabase.SupabaseStore, settings.get_config, typing.Any, typing.Dict, typing.List, typing.Optional
**Funciones:** _read_catalog(project_id, input_csv, use_supabase), _series_to_filerow(row), _row_is_folder(row), _ensure_output_dir(project_id), _persist_csv(project_id, files, folders), _persist_db_sb(sb_tbl_files, sb_tbl_folders, files, folders), _persist_db_mongo(mongo_db, col_files, col_folders, files, folders), run_enrich(env, project_id, input_csv, max_items, persist_csv, persist_supabase, persist_mongo, use_supabase, sb_tables, mongo_cfg), _safe_int(x, default)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/pipelines/enrich_pipeline.py
from __future__ import annotations

from typing import Optional, List, Dict, Any
from pathlib import Path
import json

import numpy as np
import pandas as pd

# Config / rutas
from ..settings import get_config
from ..indexing.paths import project_csv_path

# Enriquecimiento (ya implementado en el repo)
# - Files: enrich_file_row(ctx, row)  → EnrichedFile (pydantic model)
# - Folders: enrich_folder_row(ctx, folder_row, files_join_df) → EnrichedFolder
from ..enrichment.files import EnrichmentContext as FileCtx, enrich_file_row
from ..enrichment.folders import EnrichmentContext as FolderCtx, enrich_folder_row, select_folder_children
from ..enrichment.models import FileRow

# Persistencia y lectura desde Supabase
from ..io.db import get_supabase, get_mongo
from ..persistence.supabase import SupabaseStore
from ..persistence.mongo import MongoStore
from ..persistence.reader import read_catalog_from_supabase, read_enriched_data_from_supabase


def _read_catalog(project_id: str, input_csv: Optional[str] = None, use_supabase: bool = True) -> pd.DataFrame:
    """

…

        "counts": {"files": len(files_out), "folders": len(folders_out)},
    }

    # Persistencias - SIEMPRE se hace persistencia en Supabase por defecto
    if persist_csv:
        csv_paths = _persist_csv(project_id, files_out, folders_out)
        result.update({"csv": csv_paths})

    if persist_supabase:
        sb_tables = sb_tables or {"files": "enriched_files", "folders": "enriched_folders"}
        sb_res = _persist_db_sb(sb_tables["files"], sb_tables["folders"], files_out, folders_out)
        result.setdefault("db", {}).update(sb_res)

    if persist_mongo:
        mongo_cfg = mongo_cfg or {"db": os.getenv("MONGO_DB", "ennui_rag"), "files": "enriched_files", "folders": "enriched_folders"}
        mg_res = _persist_db_mongo(mongo_cfg["db"], mongo_cfg["files"], mongo_cfg["folders"], files_out, folders_out)
        result.setdefault("db", {}).update(mg_res)

    print("✅ Enrichment DONE:", result)
    return result
```
</details>

#### `src/ennui_rag/pipelines/enrich_supabase_pipeline.py`
**Docstring:** Pipeline de enriquecimiento que SIEMPRE usa Supabase para lectura y persistencia.
Reemplaza la dependencia de archivos CSV locales.
**Imports:** __future__.annotations, enrichment.files.EnrichmentContext, enrichment.files.enrich_file_row, enrichment.folders.EnrichmentContext, enrichment.folders.enrich_folder_row, enrichment.folders.select_folder_children, enrichment.models.FileRow, io.db.get_mongo, io.db.get_supabase, json, numpy, os, pandas, persistence.mongo.MongoStore, persistence.reader.read_catalog_from_supabase, persistence.reader.read_enriched_data_from_supabase, persistence.supabase.SupabaseStore, settings.get_config, typing.Any, typing.Dict, typing.List, typing.Optional
**Funciones:** _series_to_filerow(row), _persist_enriched_to_supabase(project_id, files, folders, sb_tables), _persist_enriched_to_mongo(project_id, files, folders, mongo_cfg), run_enrich_supabase(env, project_id, max_items, persist_supabase, persist_mongo, sb_tables, mongo_cfg), enrich_existing_project(project_id, env, max_items, force_reprocess), _safe_int(x, default)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/pipelines/enrich_supabase_pipeline.py
"""
Pipeline de enriquecimiento que SIEMPRE usa Supabase para lectura y persistencia.
Reemplaza la dependencia de archivos CSV locales.
"""
from __future__ import annotations

from typing import Optional, List, Dict, Any
import json
import os

import numpy as np
import pandas as pd

# Config / rutas
from ..settings import get_config

# Enriquecimiento
from ..enrichment.files import EnrichmentContext as FileCtx, enrich_file_row
from ..enrichment.folders import EnrichmentContext as FolderCtx, enrich_folder_row, select_folder_children
from ..enrichment.models import FileRow

# Persistencia y lectura desde Supabase
from ..io.db import get_supabase, get_mongo
from ..persistence.supabase import SupabaseStore
from ..persistence.mongo import MongoStore
from ..persistence.reader import read_catalog_from_supabase


def _series_to_filerow(row: pd.Series) -> FileRow:

…

            existing_files, existing_folders = read_enriched_data_from_supabase(project_id)
            if not existing_files.empty or not existing_folders.empty:
                print(f"ℹ️ Ya existen datos enriquecidos: {len(existing_files)} archivos, {len(existing_folders)} carpetas")
                if input("¿Reenriquecer? (y/N): ").lower() != 'y':
                    return {
                        "project_id": project_id,
                        "status": "skipped",
                        "reason": "Data already exists"
                    }
        except Exception as e:
            print(f"ℹ️ No se pudieron verificar datos existentes: {e}")
    
    # Ejecutar enriquecimiento
    return run_enrich_supabase(
        env=env,
        project_id=project_id,
        max_items=max_items,
        persist_supabase=True,
        persist_mongo=False
    )
```
</details>

#### `src/ennui_rag/pipelines/index_pipeline.py`
**Imports:** ennui_rag.io.db.get_mongo, ennui_rag.io.db.get_supabase, indexing.build_catalog_dataframe, indexing.save_catalog_csv, indexing.utils.now_iso, pandas, persistence.base.persist_catalog_df, persistence.mongo.MongoStore, persistence.supabase.SupabaseStore, settings.get_config, typing.List, typing.Optional
**Funciones:** run_index(env, folder_id, max_items, stores, save_csv, always_persist)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/pipelines/index_pipeline.py
from typing import Optional, List
import pandas as pd
from ..settings import get_config
from ..indexing import build_catalog_dataframe, save_catalog_csv
from ..persistence.base import persist_catalog_df
from ..persistence.mongo import MongoStore
from ..persistence.supabase import SupabaseStore
from ..indexing.utils import now_iso
from ennui_rag.io.db import get_supabase, get_mongo

def run_index(
    env: str = "dev",
    folder_id: Optional[str] = None,
    max_items: Optional[int] = None,
    stores: Optional[List] = None,
    save_csv: bool = True,
    always_persist: bool = True,  # Nuevo parámetro para forzar persistencia
) -> pd.DataFrame:
    env_vars, cfg = get_config(env)
    root_folder_id = folder_id or cfg.get("folder_id")
    if not root_folder_id:
        raise ValueError("Falta 'folder_id' en configs/*.yaml")

    df = build_catalog_dataframe(root_folder_id, max_items=max_items)
    if save_csv:
        save_catalog_csv(df)

    # Contexto de normalización/persistencia
    project_id = root_folder_id

…

                get_supabase(),
                table="catalog_drive",
                on_conflict="project_id,file_id,drive_id"  # o "file_id,drive_id" según tu índice
            ))

    if stores:
        results = persist_catalog_df(
            df,
            stores,
            batch_size=500,
            deduplicate=True,
            project_id=project_id,
            session_id=session_id,
            root_folder_id=root_folder_id,
        )
        print("📊 Persistencia:", results)
    elif always_persist:
        print("⚠️ No se pudo inicializar stores para persistencia")

    return df
```
</details>

#### `src/ennui_rag/pipelines/project_pipeline.py`
**Imports:** __future__.annotations, datetime.datetime, datetime.timezone, index_pipeline.run_index, indexing.build.save_catalog_csv, indexing.paths.project_csv_path, json, os, pathlib.Path, pymongo.MongoClient, supabase.create_client
**Funciones:** _now_utc(), _project_dir(project_id), _sessions_path(project_id), _read_json(path), _write_json(path, data), select_project(folder_id), ensure_catalog(project_id, force, max_items, persist), project_status(project_id), list_recent_projects(limit)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json, os

from .index_pipeline import run_index
from ..indexing.paths import project_csv_path
from ..indexing.build import save_catalog_csv  # <-- usar guardado directo

DATA_DIR = Path("data")

def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _project_dir(project_id: str) -> Path:
    p = DATA_DIR / project_id
    p.mkdir(parents=True, exist_ok=True)
    return p

def _sessions_path(project_id: str) -> Path:
    return _project_dir(project_id) / "sessions.json"

def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

…

    return {
        "project_id": project_id,
        "csv_path": str(csv_proj) if csv_proj.exists() else None,
        "csv_rows": n_csv,
        "last_indexed_at": sess.get("last_indexed_at"),
        "supabase_count": sb,
        "mongo_count": mg,
    }

def list_recent_projects(limit: int = 10) -> list[dict]:
    out = []
    for p in DATA_DIR.glob("*/sessions.json"):
        try:
            meta = _read_json(p)
            meta["project_id"] = p.parent.name
            out.append(meta)
        except Exception:
            pass
    out.sort(key=lambda m: m.get("last_indexed_at") or m.get("updated_at") or "", reverse=True)
    return out[:limit]
```
</details>

#### `src/ennui_rag/pipelines/project_supabase_pipeline.py`
**Docstring:** Pipeline de proyecto que SIEMPRE usa Supabase para datos enriquecidos.
Reemplaza la dependencia de archivos CSV locales.
**Imports:** __future__.annotations, datetime.datetime, datetime.timezone, enrich_supabase_pipeline.run_enrich_supabase, index_pipeline.run_index, indexing.build.save_catalog_csv, indexing.paths.project_csv_path, json, os, pathlib.Path, persistence.reader.get_supabase_status, persistence.reader.read_enriched_data_from_supabase
**Funciones:** _now_utc(), _project_dir(project_id), _sessions_path(project_id), _read_json(path), _write_json(path, data), select_project_supabase(folder_id), ensure_catalog_and_enrich_supabase(project_id, force, max_items, persist, enrich), project_status_supabase(project_id), list_recent_projects_supabase(limit), reprocess_project_supabase(project_id, force_reindex, force_reenrich, max_items)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/pipelines/project_supabase_pipeline.py
"""
Pipeline de proyecto que SIEMPRE usa Supabase para datos enriquecidos.
Reemplaza la dependencia de archivos CSV locales.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json, os

from .index_pipeline import run_index
from .enrich_supabase_pipeline import run_enrich_supabase
from ..indexing.paths import project_csv_path
from ..indexing.build import save_catalog_csv
from ..persistence.reader import get_supabase_status

DATA_DIR = Path("data")


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _project_dir(project_id: str) -> Path:
    p = DATA_DIR / project_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def _sessions_path(project_id: str) -> Path:

…

        try:
            enrich_result = run_enrich_supabase(
                env="dev",
                project_id=project_id,
                max_items=max_items,
                persist_supabase=True
            )
            result["enrichment"] = enrich_result
        except Exception as e:
            result["enrichment"] = {
                "status": "error",
                "error": str(e)
            }
    
    # 3. Estado final
    final_status = project_status_supabase(project_id)
    result["final_status"] = final_status
    
    print(f"✅ Reprocesamiento completado: {result}")
    return result
```
</details>

#### `src/ennui_rag/search/__init__.py`
**Docstring:** ennui_rag.search
Inicialización del subpaquete de búsqueda.
**Imports:** search.search_llm
**Funciones:** —
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
"""
ennui_rag.search
Inicialización del subpaquete de búsqueda.
"""
from .search import search_llm

__all__ = ["search_llm"]
```
</details>

#### `src/ennui_rag/search/answers.py`
**Docstring:** answers.py · ennui_rag.search
Modo respuesta breve con citas a los documentos top-k.
**Imports:** __future__.annotations, ennui_rag.io.llm.llm_json, pandas, typing.Any, typing.Dict, typing.List
**Funciones:** _mk_citation(row), answer_with_citations(query, ranked_df, k)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# -*- coding: utf-8 -*-
"""
answers.py · ennui_rag.search
Modo respuesta breve con citas a los documentos top-k.
"""
from __future__ import annotations

from typing import List, Dict, Any
import pandas as pd
from ennui_rag.io.llm import llm_json

__all__ = ["answer_with_citations"]


def _mk_citation(row: pd.Series) -> Dict[str, Any]:
    return {
        "title": str(row.get("title", "") or row.get("name", ""))[:160],
        "path": str(row.get("path", "") or row.get("relative_path", "")),
        "web_url": str(row.get("web_url", "")),
        "mime": str(row.get("mime", "") or row.get("mime_type", "")),
    }


def answer_with_citations(query: str, ranked_df: pd.DataFrame, k: int = 5) -> Dict[str, Any]:
    if ranked_df is None or ranked_df.empty:
        return {"answer": "", "citations": []}

    top = ranked_df.head(k).copy()
    evidence = []
    for _, r in top.iterrows():
        evidence.append({
            "title": str(r.get("title", "") or r.get("name", ""))[:160],
            "summary": str(r.get("llm_highlight", "") or r.get("summary", ""))[:800],
            "topic": str(r.get("topic", "")),
            "tags": str(r.get("tags", "")),
        })

    system = (
        "Eres un asistente que responde de forma breve y precisa usando SOLO la evidencia dada. "
        "Si falta información, dilo explícitamente. Devuelve JSON con 'answer' y NO inventes nada."
    )

    resp = llm_json(
        user_payload={"query": query, "evidence": evidence},
        system=system,
        max_tokens=220,
        temperature=0.2,
    ) or {}

    citations = [_mk_citation(r) for _, r in top.iterrows()]
    return {"answer": resp.get("answer", ""), "citations": citations}
```
</details>

#### `src/ennui_rag/search/loader.py`
**Docstring:** loader.py · ennui_rag.search
Carga robusta del corpus desde Supabase o CSV enriquecidos con fallback al catálogo base.
**Imports:** __future__.annotations, ast, pandas, pathlib.Path, persistence.reader.read_catalog_from_supabase, persistence.reader.read_enriched_data_from_supabase, typing.List, typing.Optional
**Funciones:** _safe_read_csv(p), _to_list(x), load_corpus_from_supabase(project_id, limit), _normalize_corpus_columns(df), load_corpus(project_id, data_dir, use_supabase)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# -*- coding: utf-8 -*-
"""
loader.py · ennui_rag.search
Carga robusta del corpus desde Supabase o CSV enriquecidos con fallback al catálogo base.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional
import ast
import pandas as pd

# Importar el reader de Supabase
from ..persistence.reader import read_catalog_from_supabase, read_enriched_data_from_supabase

__all__ = [
    "FILES_NAME",
    "FOLDERS_NAME",
    "BASE_NAME",
    "load_corpus",
    "load_corpus_from_supabase",
]

FILES_NAME = "catalog_enriched_files.csv"
FOLDERS_NAME = "catalog_enriched_folders.csv"
BASE_NAME = "catalog_base.csv"


def _safe_read_csv(p: Path) -> pd.DataFrame:
    if not p.exists():

…

        ]:
            if c not in base.columns:
                base[c] = ""
        return base

    parts = []
    if not df_f.empty:
        df_f = df_f.copy()
        df_f["kind"] = "file"
        parts.append(df_f)
    if not df_d.empty:
        df_d = df_d.copy()
        df_d["kind"] = "folder"
        if "summary_80w" not in df_d.columns and "summary_120w" in df_d.columns:
            df_d["summary_80w"] = df_d["summary_120w"]
        parts.append(df_d)

    df = pd.concat(parts, ignore_index=True)

    return _normalize_corpus_columns(df)
```
</details>

#### `src/ennui_rag/search/rerank.py`
**Docstring:** rerank.py · ennui_rag.search
Rerankeado con LLM en modo JSON usando ennui_rag.io.llm.llm_json.
**Imports:** __future__.annotations, ennui_rag.io.llm.llm_json, pandas, typing.Any, typing.Dict, typing.List
**Funciones:** _compact_row(row, max_chars), llm_rerank(query, candidates_df, top_n), cut(s, n)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# -*- coding: utf-8 -*-
"""
rerank.py · ennui_rag.search
Rerankeado con LLM en modo JSON usando ennui_rag.io.llm.llm_json.
"""
from __future__ import annotations

from typing import Any, Dict, List
import pandas as pd
from ennui_rag.io.llm import llm_json

__all__ = [
    "llm_rerank",
]


def _compact_row(row: pd.Series, max_chars: int = 600) -> Dict[str, Any]:
    def cut(s, n):
        s = str(s or "")
        return s[:n] + ("…" if len(s) > n else "")

    return {
        "kind": row.get("kind", ""),
        "drive_id": row.get("drive_id", ""),
        "file_id": row.get("file_id", "") or row.get("folder_id", ""),
        "name": cut(row.get("name", ""), 180),
        "title": cut(row.get("title_canonical", ""), 200),
        "path": cut(row.get("relative_path", ""), 180),
        "topic": cut(row.get("topic_label", ""), 40),
        "summary": cut(row.get("summary_80w", ""), max_chars),

…

        "candidates": items,
    }

    resp = llm_json(user_payload=payload, system=system, max_tokens=280, temperature=0.2)
    results = (resp or {}).get("results", [])

    out: List[Dict[str, Any]] = []
    for r in results[:top_n]:
        try:
            idx = int(r.get("idx", -1))
            if 0 <= idx < len(items):
                it = dict(items[idx])
                it["llm_score"] = float(r.get("score", 0))
                it["llm_reason"] = r.get("reason", "")
                it["llm_highlight"] = r.get("highlight", "")
                out.append(it)
        except Exception:
            continue

    return out
```
</details>

#### `src/ennui_rag/search/retrieve.py`
**Docstring:** retrieve.py · ennui_rag.search
Recuperación lexical simple con tolerancia a corpus escaso, filtros opcionales
y soporte híbrido con embeddings si existen.
**Imports:** __future__.annotations, ast, numpy, pandas, re, typing.List, typing.Optional
**Funciones:** _tok(s), _as_str(x), _score_row(row, q_tokens), _apply_filters(df, by_path, by_mime, modified_from, modified_to), retrieve_candidates(df, query, k, filter_kind, by_path, by_mime, modified_from, modified_to), _to_vec(x), _cos(a, b), retrieve_candidates_hybrid(df, query, k, q_vec, filter_kind, by_path, by_mime, modified_from, modified_to)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# -*- coding: utf-8 -*-
"""
retrieve.py · ennui_rag.search
Recuperación lexical simple con tolerancia a corpus escaso, filtros opcionales
y soporte híbrido con embeddings si existen.
"""
from __future__ import annotations

from typing import Optional, List
import re
import ast
import numpy as np
import pandas as pd

__all__ = [
    "retrieve_candidates",
    "retrieve_candidates_hybrid",
]


def _tok(s: str) -> List[str]:
    s = (s or "").lower()
    return re.findall(r"[a-záéíóúüñ0-9#+\-_/\.]{2,}", s)


def _as_str(x) -> str:
    if isinstance(x, str):
        return x
    try:
        return ", ".join(ast.literal_eval(x)) if isinstance(x, str) and x.strip().startswith("[") else str(x or "")

…

    modified_from: str | None = None,
    modified_to: str | None = None,
) -> pd.DataFrame:
    base = retrieve_candidates(df, query, k=max(k * 3, 60), filter_kind=filter_kind,
                               by_path=by_path, by_mime=by_mime,
                               modified_from=modified_from, modified_to=modified_to)
    if q_vec is None or base.empty:
        return base.head(k)
    tmp = base.copy()
    if "_vec" not in tmp.columns:
        if "embedding" in tmp.columns:
            tmp["_vec"] = tmp["embedding"].map(_to_vec)
        else:
            tmp["_vec"] = None
    tmp["_cos"] = tmp["_vec"].map(lambda v: _cos(q_vec, v))
    tmp["_mix"] = np.clip(tmp["_cos"], 0, 1) * 1.25
    tmp["_rank"] = np.arange(len(tmp), dtype=float)
    tmp["_final"] = (1.0 / (1.0 + tmp["_rank"])) + tmp["_mix"]
    tmp.sort_values("_final", ascending=False, inplace=True, kind="stable")
    return tmp.head(k).drop(columns=["_cos", "_mix", "_rank", "_final"], errors="ignore")
```
</details>

#### `src/ennui_rag/search/search.py`
**Docstring:** search.py · ennui_rag.search
Orquestación end-to-end: carga corpus → retrieve → rerank → DataFrame o Answer
**Imports:** __future__.annotations, answers.answer_with_citations, loader.load_corpus, pandas, pathlib.Path, rerank.llm_rerank, retrieve.retrieve_candidates, retrieve.retrieve_candidates_hybrid, typing.Optional
**Funciones:** search_llm(query, project_id)
**Clases:** —
<details><summary>Excerpt (head/tail)</summary>

```python
# -*- coding: utf-8 -*-
"""
search.py · ennui_rag.search
Orquestación end-to-end: carga corpus → retrieve → rerank → DataFrame o Answer
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional
import pandas as pd

from .loader import load_corpus
from .retrieve import retrieve_candidates, retrieve_candidates_hybrid
from .rerank import llm_rerank
from .answers import answer_with_citations

__all__ = ["search_llm"]


def search_llm(
    query: str,
    project_id: str,
    *,
    data_dir: Path | None = None,
    k: int = 40,
    n: int = 12,
    kind: Optional[str] = None,
    use_embeddings: bool = False,
    q_vec = None,
    by_path: str | None = None,

…

            "topic_label": "topic",
            "mime_type": "mime",
        }, inplace=True)
    else:
        out = pd.DataFrame(ranked)

    if as_answer:
        return answer_with_citations(query, out, k=answer_k)

    if return_candidates:
        return {"candidates": cand, "ranked": out}

    order = [
        "llm_score","title","name","path","topic","tags","entities",
        "mime","web_url","llm_reason","llm_highlight","kind","drive_id","file_id",
    ]
    for c in order:
        if c not in out.columns:
            out[c] = ""
    return out[order]
```
</details>

#### `src/ennui_rag/settings.py`
**Imports:** __future__.annotations, os, pathlib.Path, pydantic_settings.BaseSettings, pydantic_settings.SettingsConfigDict, pymongo.MongoClient, supabase.create_client, typing.Any, typing.Dict, typing.Tuple, yaml
**Funciones:** _load_yaml(path), _init_supabase(env_vars), _init_postgres(env_vars), _init_mongo(env_vars), get_config(env)
**Clases:** Env[]
<details><summary>Excerpt (head/tail)</summary>

```python
# src/ennui_rag/settings.py
from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Tuple, Dict, Any
import yaml
import os

ROOT = Path(__file__).resolve().parents[2]  # carpeta del proyecto

# 👉 REF de tu proyecto (extraído de tu DSN de ejemplo).
#    Si en el futuro cambias de proyecto, puedes setear SUPABASE_REF en el entorno.
DEFAULT_SUPABASE_REF = "refmyhnmpuerwpfjihtw"

class Env(BaseSettings):
    # --- Claves y conexiones base ---
    OPENAI_API_KEY: str | None = None

    # Supabase
    SB_SECRET: str | None = None           # service role de Supabase (API REST)
    SB_PASSWORD: str | None = None         # password del usuario postgres (DB directa)

    # Opcional: permitir override del ref si algún día cambia
    SUPABASE_REF: str | None = None

    # Derivados (se rellenan en tiempo de ejecución)
    SUPABASE_URL: str | None = None        # https://<ref>.supabase.co
    SUPABASE_KEY: str | None = None        # = SB_SECRET
    POSTGRES_DSN: str | None = None        # postgresql://postgres:PW@db.<ref>.supabase.co:5432/postgres


…

        env_vars.MONGO_CLIENT = MongoClient(uri)
        print("✅ Mongo client inicializado")
    except Exception as e:
        print("⚠️ No se pudo inicializar Mongo client:", e)
        env_vars.MONGO_CLIENT = None

def get_config(env: str = "dev") -> Tuple[Env, Dict[str, Any]]:
    env_vars = Env()

    # Inicializar derivados/conexiones usando SOLO SB_SECRET y SB_PASSWORD
    _init_supabase(env_vars)   # arma SUPABASE_URL, SUPABASE_KEY y SUPABASE_CLIENT
    _init_postgres(env_vars)   # arma POSTGRES_DSN
    _init_mongo(env_vars)      # opcional

    # Mezcla de configuración YAML
    base = _load_yaml(ROOT / "configs" / "base.yaml")
    env_cfg = _load_yaml(ROOT / "configs" / f"{env}.yaml")
    cfg = {**base, **env_cfg}

    return env_vars, cfg
```
</details>

## 🧵 Pipelines clave
### Pipelines Clave

- **project_pipeline**:
  - **select_project**: Permite seleccionar un proyecto específico para trabajar. Asegura que se esté operando sobre el proyecto correcto.
  - **ensure_catalog**: Verifica que el catálogo de proyectos esté actualizado y disponible. Previene errores por falta de datos.
  - **project_status**: Consulta el estado actual del proyecto seleccionado. Facilita el seguimiento del progreso.
  - **list_recent_projects**: Muestra una lista de los proyectos más recientes. Ayuda a identificar y acceder rápidamente a los proyectos activos.

- **index_pipeline**:
  - **run_index**: Ejecuta el proceso de indexación de datos. Acepta parámetros como el tipo de datos a indexar y la frecuencia de actualización. Los efectos incluyen la mejora en la velocidad de búsqueda y la organización de datos, optimizando el rendimiento del sistema.

- **enrich_pipeline**:
  - Actualmente no se aplica, pero se considera para el futuro. Este pipeline podría enfocarse en enriquecer los datos existentes con información adicional, mejorando la calidad y utilidad de los datos en el sistema.

### Notas Editoriales
- Se han actualizado los flujos de trabajo para reflejar el uso de timestamps y archivos especializados, lo que mejora la trazabilidad y la gestión de datos.
- Se ha implementado un sistema de legacy automatizado que limita la intervención manual, aumentando la eficiencia y reduciendo errores.

## 💾 Persistencia de datos
## Persistencia de Datos

### 1. Sanitización
- **Objetivo**: Asegurar que los datos sean válidos y utilizables.
- **Acciones**:
  - Convertir valores NaN e Inf a `None`.
  - Asegurar que los datos numéricos sean enteros.

### 2. Deduplicación
- **Método**: Eliminar duplicados basándose en la combinación de `file_id` y `drive_id`.
- **Criterio**: Mantener la entrada con la fecha de modificación más reciente.

### 3. Almacenamiento
- **SupabaseStore**: Utilizar la opción `on_conflict` para manejar conflictos de datos.
- **MongoStore**: Implementar índices para optimizar las consultas y mejorar el rendimiento.

### Recomendaciones Operativas
1. **Revisar el flujo de datos**: Asegúrate de que todos los procesos de entrada de datos sigan el nuevo flujo con timestamps y archivos especializados.
2. **Monitorear la automatización**: Verifica regularmente el sistema de legacy automatizado para asegurar que funcione correctamente y no genere datos duplicados.

## 📐 Decisiones (ADR-lite)
### Decisiones de diseño (ADR-lite)

1. **Decisión:** Utilizar CSV por proyecto.
   - **Motivación:** Facilitar la portabilidad y el manejo de datos entre diferentes entornos y herramientas.
   - **Consecuencias:** Se requiere un proceso de validación para asegurar la integridad de los datos al importar/exportar.

2. **Decisión:** Implementar clave compuesta para las entidades principales.
   - **Motivación:** Mejorar la unicidad y evitar colisiones en los identificadores de registros.
   - **Consecuencias:** Aumenta la complejidad en las consultas y puede requerir ajustes en la lógica de la base de datos.

3. **Decisión:** Asegurar idempotencia en las operaciones de carga de datos.
   - **Motivación:** Prevenir duplicados y mantener la consistencia de los datos en la base de datos.
   - **Consecuencias:** Se necesita un mecanismo para identificar y manejar cargas repetidas, lo que puede incrementar el tiempo de procesamiento.

4. **Decisión:** Desarrollar la interfaz de usuario con Streamlit.
   - **Motivación:** Proporcionar una experiencia interactiva y accesible para los usuarios finales.
   - **Consecuencias:** Dependencia de la infraestructura de Streamlit y la necesidad de capacitación para los usuarios sobre su uso.

5. **Decisión:** Establecer límites en la integración con Google Colab y Google Drive.
   - **Motivación:** Optimizar el rendimiento y evitar problemas de latencia en la carga de datos.
   - **Consecuencias:** Puede limitar la escalabilidad y requerir soluciones alternativas para manejar grandes volúmenes de datos.

6. **Decisión:** Automatizar el sistema de legacy para la gestión de snapshots.
   - **Motivación:** Mantener un registro

## ⚠️ Riesgos y mitigaciones
### Riesgos y Mitigaciones

- **Riesgo: Límites de API en la indexación de Drive**
  - **Mitigación:** Implementar un sistema de manejo de errores que limite las solicitudes a la API, distribuyendo las peticiones a lo largo del tiempo.

- **Riesgo: Datos corruptos durante la indexación**
  - **Mitigación:** Establecer validaciones de integridad de datos post-indexación y crear copias de seguridad periódicas.

- **Riesgo: Tiempos de procesamiento prolongados**
  - **Mitigación:** Optimizar el flujo de trabajo mediante la paralelización de tareas y el uso de archivos especializados para reducir la carga.

- **Riesgo: Costos inesperados por uso excesivo de recursos**
  - **Mitigación:** Monitorear el uso de recursos en tiempo real y establecer alertas para evitar sobrecostos.

- **Riesgo: Incompatibilidad en el entorno de Colab**
  - **Mitigación:** Probar el flujo en diferentes entornos de Colab y documentar configuraciones específicas para asegurar compatibilidad.

- **Riesgo: Fallos en el sistema de legacy automatizado**
  - **Mitigación:** Realizar pruebas regulares y mantener un plan de contingencia para restaurar el sistema en caso de fallos.

- **Riesgo: Falta de documentación actualizada**
  - **Mitigación:** Establecer un proceso de revisión y actualización continua del README y otros documentos relevantes.

## 🗺️ Roadmap
# Roadmap Priorizado para ennui-rag

1. **Actualizar README**
   - **Criterios de aceptación**: Incluir flujo actual con timestamps, archivos especializados y detalles del sistema de legacy automatizado. Validar con el equipo que la documentación sea clara y completa.

2. **Optimizar Pipelines de Indexación**
   - **Criterios de aceptación**: Reducir el tiempo de indexación en un 20%. Realizar pruebas de rendimiento y documentar mejoras.

3. **Implementar Enriquecimiento de Datos**
   - **Criterios de aceptación**: Integrar al menos 3 nuevas fuentes de datos para enriquecer la información indexada. Validar la calidad de los datos enriquecidos con métricas de precisión.

4. **Refactorizar Código de APIs**
   - **Criterios de aceptación**: Mejorar la legibilidad y modularidad de al menos 10 módulos Python. Realizar pruebas unitarias y asegurar que la cobertura de pruebas sea del 80%.

5. **Añadir Funcionalidades a la UI de Streamlit**
   - **Criterios de aceptación**: Implementar al menos 3 nuevas características solicitadas por usuarios. Realizar pruebas de usabilidad y obtener feedback positivo del

---
> Generado con Python a partir del árbol de archivos, parsers AST y extractos de docs/notebooks, con secciones enriquecidas por LLM (OpenAI).