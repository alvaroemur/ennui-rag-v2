---
title: "Vision · ennui-rag · v0.1"
project: "ennui-rag"
doc_type: "design"
version: "v0.1"
date: "2025-09-15"
source_of_truth: "to-be"
---

# Vision · ennui-rag · v0.1 — 2025-09-15

## Propósito y Alcance

ennui-rag es un sistema de gestión de programas educativos que combina capacidades de RAG (Retrieval-Augmented Generation) con un modelo robusto de cumplimiento de evidencias. El sistema está diseñado para automatizar la recolección, procesamiento y evaluación de evidencias de aprendizaje en programas de formación empresarial y educativa.

El alcance incluye la gestión completa del ciclo de vida de programas, desde la configuración inicial hasta la evaluación final, pasando por el seguimiento de participación, mentorías y cumplimiento de requisitos específicos.

## Usuarios y Casos de Uso

**Usuarios principales:**
- **Administradores de programas** - Configuran cohortes, definen requisitos y supervisan cumplimiento
- **Facilitadores** - Gestionan sesiones, registran asistencia y evalúan evidencias
- **Participantes** - Envían evidencias, consultan su progreso y acceden a recursos
- **Mentores** - Proporcionan apoyo personalizado a organizaciones participantes

**Casos de uso clave:**
- Configuración de programas con plantillas reutilizables
- Gestión de cohortes con múltiples organizaciones
- Procesamiento automático de evidencias desde Google Drive
- Evaluación de cumplimiento con métricas en tiempo real
- Generación de reportes y dashboards analíticos

## Arquitectura Lógica

El sistema se estructura en tres capas principales:

- **Capa de Datos** - Integra Google Drive para almacenamiento de documentos, BD relacional (hoy: Supabase; objetivo: Postgres con ORM) para datos estructurados y MongoDB para metadatos complejos
- **Capa de Procesamiento** - Incluye módulos de indexación para extracción de contenido, enriquecimiento con metadatos y búsqueda RAG con reranking
- **Capa de Aplicación** - Proporciona interfaz Streamlit, APIs de backend y pipelines de procesamiento automatizado
- **Capa de Cumplimiento** - Gestiona requisitos, asignaciones, evidencias y evaluaciones con contexto operativo
- **Capa de Conocimiento** - Mantiene índices RAG, dashboards analíticos y auditoría de eventos
- **Capa de Integración** - Conecta con sistemas externos y proporciona APIs para terceros

## Modelo de Datos

El modelo relacional se centra en entidades core:

- **Programas y Cohortes** - Estructura jerárquica que permite múltiples instancias de programas
- **Organizaciones y Personas** - Gestión de participantes con roles específicos y relaciones organizacionales
- **Sesiones y Asistencia** - Seguimiento detallado de participación con contexto temporal
- **Mentorías** - Sistema de matching entre mentores y organizaciones con seguimiento de relaciones
- **Cumplimiento** - Modelo despolimorfizado con requisitos, asignaciones, evidencias y evaluaciones
- **Evidencias y Contexto** - Vinculación explícita entre evidencias y contexto operativo (sesiones, personas, organizaciones)

## Flujo de Cumplimiento

El sistema implementa un pipeline de cumplimiento que comienza con la definición de requisitos específicos para cada cohorte. Estos requisitos se asignan a participantes individuales u organizaciones, quienes deben proporcionar evidencias dentro de ventanas de tiempo definidas.

Las evidencias se procesan automáticamente desde Google Drive, pasando por resolución de identidad y validación de contexto. El sistema evalúa cada evidencia contra los requisitos correspondientes, generando estados de cumplimiento que se consolidan en KPIs y dashboards en tiempo real.

## Integraciones y Fuentes

**Fuentes de datos principales:**
- **Google Drive API** - Almacenamiento y sincronización de documentos
- **BD relacional (hoy: Supabase; objetivo: Postgres con ORM)** - Datos estructurados con capacidades de tiempo real
- **MongoDB** - Persistencia de metadatos complejos y configuraciones
- **APIs de LLM** - Procesamiento de lenguaje natural para análisis de contenido

**Integraciones externas:**
- Sistemas de autenticación empresarial
- Herramientas de videoconferencia para sesiones
- Plataformas de comunicación para notificaciones
- Sistemas de reporting y business intelligence

## Roadmap y Entregables

**Fase 1 (Actual)** - MVP con funcionalidades core
- Configuración básica de programas y cohortes
- Procesamiento de evidencias desde Google Drive
- Sistema de cumplimiento con evaluación manual
- Interfaz Streamlit para administración

**Fase 2** - Automatización y escalabilidad
- Resolución automática de identidad
- Evaluación automatizada de evidencias
- Dashboards analíticos avanzados
- APIs para integración con terceros

**Fase 3** - Inteligencia y optimización
- Análisis predictivo de cumplimiento
- Recomendaciones personalizadas
- Optimización automática de programas
- Integración con ecosistemas educativos

## Decisiones Abiertas / Supuestos

**Supuestos técnicos:**
- Google Drive como fuente única de documentos
- BD relacional (hoy: Supabase; objetivo: Postgres con ORM) como base de datos principal
- Streamlit como interfaz de usuario inicial
- Modelos de LLM para procesamiento de contenido

**Decisiones pendientes:**
- Estrategia de backup y recuperación de datos
- Modelo de licenciamiento y monetización
- Integración con sistemas de gestión de aprendizaje (LMS)
- Estrategia de internacionalización y localización

**Riesgos identificados:**
- Dependencia de APIs externas (Google Drive, LLM)
- Escalabilidad de procesamiento de documentos
- Privacidad y seguridad de datos educativos
- Adopción y curva de aprendizaje de usuarios

---

## Referencias

- [Flujo%20de%20Cumplimiento](../blueprints/Flujo%20Cumplimiento%20·%20ennui-rag%20·%20v0.1%20—%202025-09-15.mmd)
- [ERD%20Objetivo](../erd-objetivo/ERD%20Objetivo%20·%20ennui-rag%20·%20v0.1%20—%202025-09-15.mmd)