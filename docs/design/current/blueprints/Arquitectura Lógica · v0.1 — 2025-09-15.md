---
title: "Arquitectura Lógica"
project: "ennui-rag"
doc_type: "design"
version: "v0.1"
date: "2025-09-15"
source_of_truth: "to-be"
---

# Arquitectura Lógica · ennui-rag · v0.1

## Visión General

Sistema RAG (Retrieval-Augmented Generation) para gestión de programas educativos con cumplimiento de evidencias.

## Componentes Principales

### 1. Capa de Datos
- **Google Drive** - Almacenamiento de documentos
- **Supabase** - Base de datos relacional
- **MongoDB** - Persistencia de metadatos

### 2. Capa de Procesamiento
- **Indexación** - Extracción y normalización de contenido
- **Enriquecimiento** - Análisis de documentos y metadatos
- **Búsqueda** - RAG con recuperación y reranking

### 3. Capa de Aplicación
- **Streamlit UI** - Interfaz de usuario
- **APIs** - Servicios de backend
- **Pipelines** - Flujos de procesamiento

## Flujos Principales

1. **Indexación** - Documentos → Catálogo → Base de datos
2. **Enriquecimiento** - Análisis → Metadatos → RAG Index
3. **Búsqueda** - Query → Retrieval → Rerank → Respuesta
4. **Cumplimiento** - Evidencias → Evaluación → KPIs
