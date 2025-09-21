---
title: "Sistema de archivos"
project: "ennui-rag"
description: "Forma de organizar el repo"
doc_type: "design"
version: "v0.1"
date: "2025-09-16"
source_of_truth: "to-be"
---

ennui-rag/
│
├── apps/                  # interfaces
│   ├── ui_streamlit/      # UI actual
│   └── ui_streamlit2/     # futura UI limpia
│
├── packages/              # lógica de negocio
│   ├── core/              # modelos ORM (Program, Cohort, Evidence, etc.)
│   ├── ingestion/         # indexación + enrichment pipelines
│   └── rag/               # búsqueda y RAG
│
├── db/
│   ├── migrations/        # Alembic (cuando lo integres)
│   └── seeds/             # JSON/YAML con datos iniciales
│
├── scripts/               # utilidades CLI
│   ├── dev_run.sh         # correr la UI
│   ├── ingest_project.py  # indexar / enriquecer
│   └── seed.py            # cargar seed-data
│
├── notebooks/             # experimentos en Jupyter/Colab
│   └── …                  # NO mezclados con código productivo
│
├── data/                  # datos locales (fuera de Git)
│   ├── raw/               # dumps originales
│   ├── processed/         # catálogos, enriquecidos
│   └── backups/           # snapshots CSV, JSON, logs
│
├── docs/                  # documentación (Mermaid, readmes, etc.)
│
├── tests/                 # tests unitarios e integrales
│
├── .gitignore             # ignora /data, /backups, .env, logs
├── requirements.txt
├── pyproject.toml         # (si decides migrar a Poetry o similar)
└── README.md              # instrucciones de instalación y uso
