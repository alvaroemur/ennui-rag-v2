"""
Repository Speak - Servicio de selección de archivos indexados, lectura vía LLM y conversión de formato
Speak = Conversación inteligente con archivos
"""
import streamlit as st
import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from config import API_BASE_URL_INTERNAL
from auth_utils import make_authenticated_request


def render_speak_screen():
    """Renderiza la pantalla principal del servicio Speak"""
    # Verificar que hay un programa seleccionado
    selected_program_id = st.session_state.get("selected_program_id")
    if not selected_program_id:
        st.error("No se ha seleccionado un programa.")
        if st.button("Volver a selección de programa"):
            st.session_state["view"] = "program_selection"
            st.rerun()
        st.stop()
    
    # Botón para volver
    if st.button("← Volver al Homepage"):
        st.session_state["view"] = "homepage"
        st.rerun()
    
    st.markdown("## 🗣️ Repository Speak - Conversación Inteligente")
    st.markdown("Servicio de selección de archivos indexados, lectura vía LLM y conversión de formato")
    
    # Obtener datos del programa
    program_data = get_program_data(selected_program_id)
    if not program_data:
        st.error("No se pudieron cargar los datos del programa.")
        return
    
    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["📁 Selección de Archivos", "🤖 Prompt", "📊 Resultados"])
    
    with tab1:
        render_file_selection_tab(selected_program_id, program_data)
    
    with tab2:
        render_prompt_tab(selected_program_id)
    
    with tab3:
        render_results_tab(selected_program_id)


def render_file_selection_tab(program_id: int, program_data: Dict):
    """Tab de selección de archivos indexados"""
    st.markdown("### 📁 Selección de Archivos Indexados")
    
    # Filtros de búsqueda
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Buscar archivos", placeholder="Ingresa palabras clave...")
    
    with col2:
        file_type_filter = st.selectbox(
            "Tipo de archivo",
            ["Todos", "PDF", "DOC", "DOCX", "TXT", "XLSX", "PPTX", "Google Docs"]
        )
    
    with col3:
        status_filter = st.selectbox(
            "Estado",
            ["Todos", "Completado", "Pendiente", "Fallido"]
        )
    
    # Botones de búsqueda
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🔍 Buscar Archivos", type="primary", use_container_width=True):
            search_files(program_id, search_query, file_type_filter, status_filter)
    
    with col2:
        if st.button("🔄 Limpiar Búsqueda", use_container_width=True):
            if "search_results" in st.session_state:
                del st.session_state["search_results"]
            st.rerun()
    
    # Mostrar archivos disponibles
    render_files_list(program_id, search_query, file_type_filter, status_filter)


def render_files_list(program_id: int, search_query: str, file_type_filter: str, status_filter: str):
    """Renderiza la lista de archivos con opciones de selección"""
    st.markdown("### Archivos Disponibles")
    
    # Verificar si hay resultados de búsqueda
    search_results = st.session_state.get("search_results")
    
    if search_results and search_results.get("query") == search_query and search_results.get("file_type") == file_type_filter and search_results.get("status") == status_filter:
        # Usar resultados de búsqueda real
        files_data = search_results.get("files", [])
        total_count = search_results.get("total_count", 0)
        st.info(f"🔍 Mostrando {len(files_data)} de {total_count} resultados para: '{search_query}'")
    else:
        # Usar datos mockup por defecto
        files_data = get_mockup_files_data()
        if search_query or file_type_filter != "Todos" or status_filter != "Todos":
            st.info("💡 Usa el botón 'Buscar Archivos' para realizar una búsqueda real en la base de datos")
        else:
            st.info("📁 Mostrando archivos de ejemplo (datos mockup)")
    
    if not files_data:
        st.info("No hay archivos indexados disponibles.")
        return
    
    # Aplicar filtros (solo si no hay búsqueda activa)
    if not search_results or search_results.get("query") != search_query or search_results.get("file_type") != file_type_filter or search_results.get("status") != status_filter:
        filtered_files = apply_file_filters(files_data, search_query, file_type_filter, status_filter)
    else:
        filtered_files = files_data
    
    if not filtered_files:
        st.warning("No se encontraron archivos que coincidan con los filtros.")
        return
    
    # Mostrar estadísticas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total archivos", len(files_data))
    with col2:
        st.metric("Filtrados", len(filtered_files))
    with col3:
        selected_count = len([f for f in filtered_files if f.get("selected", False)])
        st.metric("Seleccionados", selected_count)
    with col4:
        total_size = sum(f.get("file_size", 0) for f in filtered_files)
        st.metric("Tamaño total (MB)", round(total_size / (1024 * 1024), 2))
    
    # Selección de archivo único
    st.markdown("#### Selecciona un archivo para procesar:")
    
    # Crear opciones para radio button
    file_options = []
    for i, file in enumerate(filtered_files):
        file_options.append(f"{file['name']} ({file['type']}) - {round(file['file_size'] / 1024, 2)} KB")
    
    if file_options:
        # Radio button para selección única
        selected_index = st.radio(
            "Archivos disponibles:",
            range(len(file_options)),
            format_func=lambda x: file_options[x],
            key=f"file_selection_{program_id}"
        )
        
        # Marcar el archivo seleccionado
        for i, file in enumerate(filtered_files):
            file["selected"] = (i == selected_index)
        
        # Guardar el estado actualizado en session state si hay búsqueda activa
        search_results = st.session_state.get("search_results")
        if search_results and search_results.get("query") == search_query and search_results.get("file_type") == file_type_filter and search_results.get("status") == status_filter:
            search_results["files"] = filtered_files
            st.session_state["search_results"] = search_results
    
    # Botón de carga de archivo
    if file_options:
        selected_file = filtered_files[selected_index]
        
        if st.button("📁 Cargar archivo", type="primary", use_container_width=True):
            st.session_state["selected_file_for_speak"] = selected_file
            st.rerun()
        
        # Mostrar detalles del archivo seleccionado
        if "selected_file_for_speak" in st.session_state:
            render_file_details(st.session_state["selected_file_for_speak"])


def render_file_details(selected_file: Dict):
    """Renderiza los detalles del archivo seleccionado"""
    st.markdown("### 📄 Detalles del archivo seleccionado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Información básica")
        st.write(f"**Nombre:** {selected_file['name']}")
        st.write(f"**Tipo:** {selected_file['type']}")
        st.write(f"**Tamaño:** {round(selected_file['file_size'] / 1024, 2)} KB")
        st.write(f"**Estado:** {selected_file['status']}")
        st.write(f"**Ruta:** {selected_file['path']}")
    
    with col2:
        st.markdown("#### Fechas")
        st.write(f"**Última modificación:** {selected_file['modified_time']}")
        if 'created_time' in selected_file:
            st.write(f"**Fecha de creación:** {selected_file['created_time']}")
    
    # Mostrar contenido si está disponible
    if 'content_text' in selected_file and selected_file['content_text']:
        st.markdown("#### Contenido del archivo")
        st.text_area("Texto extraído:", selected_file['content_text'], height=200, disabled=True)
    
    # Mensaje informativo
    st.info("ℹ️ El archivo se encuentra seleccionado. Puede proceder a la ventana de Prompt.")


def render_prompt_tab(program_id: int):
    """Tab de prompt para procesamiento LLM"""
    st.markdown("### 🤖 Prompt")
    
    # Verificar si hay archivo seleccionado
    selected_file = st.session_state.get("selected_file_for_speak")
    if not selected_file:
        st.warning("⚠️ No hay archivo seleccionado. Ve a la pestaña 'Selección de Archivos' primero.")
        return
    
    st.info(f"📁 Archivo seleccionado: {selected_file['name']}")
    
    # Configuración del LLM
    st.markdown("#### Configuración del LLM")
    
    col1, col2 = st.columns(2)
    
    with col1:
        llm_model = st.selectbox(
            "Modelo de LLM",
            ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet", "claude-3-haiku"],
            index=0
        )
        
        temperature = st.slider("Temperatura", 0.0, 2.0, 0.7, 0.1)
    
    with col2:
        max_tokens = st.number_input("Máximo de tokens", 100, 4000, 1000)
        
        language = st.selectbox(
            "Idioma de salida",
            ["Español", "Inglés", "Francés", "Portugués"],
            index=0
        )
    
    # Prompt personalizado
    st.markdown("#### Prompt de Procesamiento")
    default_prompt = """Analiza el siguiente documento y extrae la información más relevante. 
    Identifica:
    1. Objetivos principales
    2. Metodologías utilizadas
    3. Resultados obtenidos
    4. Conclusiones importantes
    5. Recomendaciones
    
    Proporciona la información en un formato estructurado y claro."""
    
    custom_prompt = st.text_area(
        "Prompt personalizado",
        value=default_prompt,
        height=150,
        help="Personaliza el prompt que se enviará al LLM para procesar los documentos."
    )
    
    # Botón de procesamiento
    if st.button("🗣️ Iniciar Procesamiento LLM", type="primary"):
        process_file_with_llm(selected_file, llm_model, temperature, max_tokens, language, custom_prompt)




def render_results_tab(program_id: int):
    """Tab de resultados"""
    st.markdown("### 📊 Resultados del Procesamiento")
    
    # Verificar si hay resultado de LLM
    llm_result = st.session_state.get("llm_processing_result")
    if not llm_result:
        st.warning("⚠️ No hay resultado de procesamiento LLM. Ve a la pestaña 'Prompt' primero.")
        return
    
    st.success(f"✅ Resultado de procesamiento disponible para: {llm_result['file_name']}")
    
    # Mostrar resumen
    render_llm_result_summary(llm_result)
    
    # Mostrar resultado detallado
    render_detailed_llm_result(llm_result)
    
    # Opciones de exportación
    render_export_options(llm_result)


def get_mockup_files_data() -> List[Dict]:
    """Genera datos mockup de archivos indexados"""
    return [
        {
            "id": 1,
            "name": "Plan_Estrategico_2024.pdf",
            "type": "PDF",
            "file_size": 2048576,  # 2MB
            "status": "Completado",
            "modified_time": "2024-01-15 10:30:00",
            "path": "/Programas/Plan_2024/Plan_Estrategico_2024.pdf",
            "selected": False
        },
        {
            "id": 2,
            "name": "Informe_Trimestral_Q1.docx",
            "type": "DOCX",
            "file_size": 1024000,  # 1MB
            "status": "Completado",
            "modified_time": "2024-01-20 14:15:00",
            "path": "/Programas/Plan_2024/Informes/Informe_Trimestral_Q1.docx",
            "selected": False
        },
        {
            "id": 3,
            "name": "Metodologia_Implementacion.txt",
            "type": "TXT",
            "file_size": 512000,  # 512KB
            "status": "Completado",
            "modified_time": "2024-01-18 09:45:00",
            "path": "/Programas/Plan_2024/Metodologia_Implementacion.txt",
            "selected": False
        },
        {
            "id": 4,
            "name": "Presupuesto_Detallado.xlsx",
            "type": "XLSX",
            "file_size": 768000,  # 768KB
            "status": "Completado",
            "modified_time": "2024-01-22 16:20:00",
            "path": "/Programas/Plan_2024/Presupuesto_Detallado.xlsx",
            "selected": False
        },
        {
            "id": 5,
            "name": "Presentacion_Resultados.pptx",
            "type": "PPTX",
            "file_size": 1536000,  # 1.5MB
            "status": "Completado",
            "modified_time": "2024-01-25 11:30:00",
            "path": "/Programas/Plan_2024/Presentaciones/Presentacion_Resultados.pptx",
            "selected": False
        },
        {
            "id": 6,
            "name": "Documento_Colaborativo",
            "type": "Google Docs",
            "file_size": 256000,  # 256KB
            "status": "Completado",
            "modified_time": "2024-01-28 13:45:00",
            "path": "/Programas/Plan_2024/Colaborativo/Documento_Colaborativo",
            "selected": False
        },
        {
            "id": 7,
            "name": "Manual_Procedimientos.pdf",
            "type": "PDF",
            "file_size": 3072000,  # 3MB
            "status": "Pendiente",
            "modified_time": "2024-01-30 08:15:00",
            "path": "/Programas/Plan_2024/Manuales/Manual_Procedimientos.pdf",
            "selected": False
        },
        {
            "id": 8,
            "name": "Archivo_Corrupto.docx",
            "type": "DOCX",
            "file_size": 0,
            "status": "Fallido",
            "modified_time": "2024-01-12 12:00:00",
            "path": "/Programas/Plan_2024/Archivo_Corrupto.docx",
            "selected": False
        }
    ]


def apply_file_filters(files: List[Dict], search_query: str, file_type_filter: str, status_filter: str) -> List[Dict]:
    """Aplica filtros a la lista de archivos"""
    filtered = files.copy()
    
    # Filtro de búsqueda
    if search_query:
        filtered = [f for f in filtered if search_query.lower() in f["name"].lower()]
    
    # Filtro de tipo de archivo
    if file_type_filter != "Todos":
        filtered = [f for f in filtered if f["type"] == file_type_filter]
    
    # Filtro de estado
    if status_filter != "Todos":
        filtered = [f for f in filtered if f["status"] == status_filter]
    
    return filtered




def search_files(program_id: int, query: str, file_type: str, status: str):
    """Busca archivos según los criterios especificados"""
    try:
        # Preparar parámetros de búsqueda
        search_params = {
            "program_id": program_id,
            "query": query if query else "",
            "file_types": [file_type.lower()] if file_type != "Todos" else None,
            "limit": 100
        }
        
        # Filtrar tipos de archivo nulos
        if search_params["file_types"] is None:
            del search_params["file_types"]
        
        # Realizar búsqueda en la API
        resp = make_authenticated_request(
            "POST", 
            f"{API_BASE_URL_INTERNAL}/api/indexing/search", 
            json=search_params,
            timeout=15
        )
        
        if resp.status_code == 200:
            search_result = resp.json()
            files_data = search_result.get("files", [])
            total_count = search_result.get("total_count", 0)
            
            # Convertir a formato esperado por la interfaz
            converted_files = []
            for file in files_data:
                # Mapear tipos de archivo a formato esperado
                file_type_mapping = {
                    "pdf": "PDF",
                    "docx": "DOCX", 
                    "doc": "DOC",
                    "txt": "TXT",
                    "xlsx": "XLSX",
                    "pptx": "PPTX",
                    "google_doc": "Google Docs"
                }
                
                converted_file = {
                    "id": file.get("id"),
                    "name": file.get("drive_file_name", ""),
                    "type": file_type_mapping.get(file.get("file_type", ""), file.get("file_type", "").upper()),
                    "file_size": file.get("file_size", 0),
                    "status": "Completado" if file.get("indexing_status") == "completed" else file.get("indexing_status", ""),
                    "modified_time": file.get("drive_modified_time", ""),
                    "path": file.get("drive_file_id", ""),
                    "selected": False
                }
                converted_files.append(converted_file)
            
            # Aplicar filtro de estado si no es "Todos"
            if status != "Todos":
                converted_files = [f for f in converted_files if f["status"] == status]
            
            # Guardar resultados en session state para mostrarlos
            st.session_state["search_results"] = {
                "files": converted_files,
                "total_count": total_count,
                "query": query,
                "file_type": file_type,
                "status": status
            }
            
            st.success(f"✅ Encontrados {len(converted_files)} archivo(s) de {total_count} total")
            
        else:
            error_msg = resp.json().get("detail", "Error desconocido") if resp.headers.get("content-type", "").startswith("application/json") else resp.text
            st.error(f"❌ Error en la búsqueda: {error_msg}")
            
    except Exception as e:
        st.error(f"❌ Error de conexión: {str(e)}")
    
    # Refrescar la página para mostrar resultados
    st.rerun()


def process_file_with_llm(file: Dict, model: str, temperature: float, max_tokens: int, language: str, prompt: str):
    """Procesa un archivo seleccionado con LLM"""
    st.info("🗣️ Iniciando procesamiento con LLM...")
    
    # Simular procesamiento
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text(f"Procesando: {file['name']}")
    
    # Simular tiempo de procesamiento
    time.sleep(2)
    
    # Generar resultado mockup
    result = {
        "file_id": file["id"],
        "file_name": file["name"],
        "processed_at": datetime.now().isoformat(),
        "llm_model": model,
        "llm_response": generate_mockup_llm_response(file["name"]),
        "metadata": {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "language": language,
            "processing_time": 2.0
        }
    }
    
    progress_bar.progress(1.0)
    
    # Guardar resultado en session state
    st.session_state["llm_processing_result"] = result
    
    status_text.text("✅ Procesamiento completado")
    st.success(f"✅ Archivo '{file['name']}' procesado exitosamente")
    
    # Mostrar resumen del resultado
    st.markdown("#### Resumen del Procesamiento")
    with st.expander(f"📄 {result['file_name']}"):
        st.json(result["llm_response"])


def generate_mockup_llm_response(file_name: str) -> Dict:
    """Genera una respuesta mockup del LLM"""
    return {
        "objetivos_principales": [
            "Mejorar la eficiencia operativa",
            "Aumentar la satisfacción del cliente",
            "Optimizar los procesos internos"
        ],
        "metodologias_utilizadas": [
            "Análisis de datos cuantitativos",
            "Entrevistas con stakeholders",
            "Benchmarking de mejores prácticas"
        ],
        "resultados_obtenidos": [
            "Incremento del 25% en la productividad",
            "Reducción del 30% en costos operativos",
            "Mejora del 40% en satisfacción del cliente"
        ],
        "conclusiones_importantes": [
            "La implementación fue exitosa",
            "Se requieren ajustes menores",
            "El ROI es positivo a corto plazo"
        ],
        "recomendaciones": [
            "Continuar con la fase 2 del proyecto",
            "Capacitar al personal en nuevas herramientas",
            "Establecer métricas de seguimiento"
        ],
        "resumen_ejecutivo": f"El documento '{file_name}' presenta un análisis detallado de la implementación del proyecto, mostrando resultados positivos y recomendaciones claras para el futuro.",
        "palabras_clave": ["eficiencia", "optimización", "productividad", "satisfacción", "ROI"],
        "confianza_score": 0.87
    }


def render_llm_result_summary(llm_result: Dict):
    """Renderiza el resumen del resultado del LLM"""
    st.markdown("#### Resumen del Procesamiento LLM")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Archivo Procesado", 1)
    
    with col2:
        content_size = len(str(llm_result["llm_response"]))
        st.metric("Tamaño (KB)", round(content_size / 1024, 2))
    
    with col3:
        st.metric("Modelo LLM", llm_result["llm_model"])
    
    with col4:
        processing_time = llm_result["metadata"]["processing_time"]
        st.metric("Tiempo (s)", round(processing_time, 2))


def render_detailed_llm_result(llm_result: Dict):
    """Renderiza el resultado detallado del LLM"""
    st.markdown("#### Resultado Detallado")
    
    with st.expander(f"📄 {llm_result['file_name']} (LLM: {llm_result['llm_model']})"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.json(llm_result["llm_response"])
        
        with col2:
            st.json(llm_result["metadata"])


def render_export_options(llm_result: Dict):
    """Renderiza las opciones de exportación"""
    st.markdown("#### Opciones de Exportación")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Descargar JSON", type="primary"):
            st.info("🚧 Funcionalidad de descarga pendiente de implementación")
    
    with col2:
        if st.button("📋 Copiar al Portapapeles"):
            st.info("🚧 Funcionalidad de copia pendiente de implementación")
    
    with col3:
        if st.button("📧 Enviar por Email"):
            st.info("🚧 Funcionalidad de email pendiente de implementación")


def get_program_data(program_id: int) -> Optional[Dict]:
    """Obtiene los datos del programa"""
    try:
        resp = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/api/programs/{program_id}", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None
