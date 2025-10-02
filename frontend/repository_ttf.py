"""
Repository TTF - Servicio de selección de archivos indexados, lectura vía LLM y conversión de formato
TTF = Text-to-Format (Texto a Formato)
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


def render_ttf_screen():
    """Renderiza la pantalla principal del servicio TTF"""
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
    
    st.markdown("## 🔄 Repository TTF - Text to Format")
    st.markdown("Servicio de selección de archivos indexados, lectura vía LLM y conversión de formato")
    
    # Obtener datos del programa
    program_data = get_program_data(selected_program_id)
    if not program_data:
        st.error("No se pudieron cargar los datos del programa.")
        return
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs(["📁 Selección de Archivos", "🤖 Lectura LLM", "🔄 Conversión", "📊 Resultados"])
    
    with tab1:
        render_file_selection_tab(selected_program_id, program_data)
    
    with tab2:
        render_llm_reading_tab(selected_program_id)
    
    with tab3:
        render_conversion_tab(selected_program_id)
    
    with tab4:
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
    
    # Botón de búsqueda
    if st.button("🔍 Buscar Archivos", type="primary"):
        search_files(program_id, search_query, file_type_filter, status_filter)
    
    # Mostrar archivos disponibles
    render_files_list(program_id, search_query, file_type_filter, status_filter)


def render_files_list(program_id: int, search_query: str, file_type_filter: str, status_filter: str):
    """Renderiza la lista de archivos con opciones de selección"""
    st.markdown("### Archivos Disponibles")
    
    # Obtener archivos (mockup por ahora)
    files_data = get_mockup_files_data()
    
    if not files_data:
        st.info("No hay archivos indexados disponibles.")
        return
    
    # Aplicar filtros
    filtered_files = apply_file_filters(files_data, search_query, file_type_filter, status_filter)
    
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
    
    # Tabla de archivos con checkboxes
    st.markdown("#### Selecciona archivos para procesar:")
    
    # Crear DataFrame para la tabla
    df_data = []
    for i, file in enumerate(filtered_files):
        df_data.append({
            "Seleccionar": st.checkbox("", key=f"select_{file['id']}", value=file.get("selected", False)),
            "Nombre": file["name"],
            "Tipo": file["type"],
            "Tamaño (KB)": round(file["file_size"] / 1024, 2),
            "Estado": file["status"],
            "Última modificación": file["modified_time"],
            "Ruta": file["path"]
        })
    
    # Mostrar tabla
    if df_data:
        df = pd.DataFrame(df_data)
        st.dataframe(
            df,
            use_container_width=True,
            height=400,
            column_config={
                "Seleccionar": st.column_config.CheckboxColumn("", width="small"),
                "Nombre": st.column_config.TextColumn("Nombre", width="medium"),
                "Tipo": st.column_config.TextColumn("Tipo", width="small"),
                "Tamaño (KB)": st.column_config.NumberColumn("Tamaño", width="small"),
                "Estado": st.column_config.TextColumn("Estado", width="small"),
                "Última modificación": st.column_config.DatetimeColumn("Modificado", width="medium"),
                "Ruta": st.column_config.TextColumn("Ruta", width="large")
            }
        )
    
    # Botones de acción
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("✅ Seleccionar Todos"):
            select_all_files(filtered_files)
    
    with col2:
        if st.button("❌ Deseleccionar Todos"):
            deselect_all_files(filtered_files)
    
    with col3:
        selected_files = [f for f in filtered_files if f.get("selected", False)]
        if selected_files:
            st.success(f"✅ {len(selected_files)} archivo(s) seleccionado(s)")
            if st.button("➡️ Continuar a Lectura LLM", type="primary"):
                st.session_state["selected_files_for_ttf"] = selected_files
                st.rerun()


def render_llm_reading_tab(program_id: int):
    """Tab de lectura de información vía LLM"""
    st.markdown("### 🤖 Lectura de Información vía LLM")
    
    # Verificar si hay archivos seleccionados
    selected_files = st.session_state.get("selected_files_for_ttf", [])
    if not selected_files:
        st.warning("⚠️ No hay archivos seleccionados. Ve a la pestaña 'Selección de Archivos' primero.")
        return
    
    st.info(f"📁 {len(selected_files)} archivo(s) seleccionado(s) para procesamiento")
    
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
    if st.button("🚀 Iniciar Procesamiento LLM", type="primary"):
        process_files_with_llm(selected_files, llm_model, temperature, max_tokens, language, custom_prompt)


def render_conversion_tab(program_id: int):
    """Tab de conversión de formato"""
    st.markdown("### 🔄 Conversión de Formato")
    
    # Verificar si hay resultados de LLM
    llm_results = st.session_state.get("llm_processing_results", [])
    if not llm_results:
        st.warning("⚠️ No hay resultados de procesamiento LLM. Ve a la pestaña 'Lectura LLM' primero.")
        return
    
    st.info(f"📊 {len(llm_results)} resultado(s) de LLM disponible(s)")
    
    # Configuración del formato de salida
    st.markdown("#### Configuración del Formato de Salida")
    
    col1, col2 = st.columns(2)
    
    with col1:
        output_format = st.selectbox(
            "Formato de salida",
            ["JSON", "XML", "CSV", "Markdown", "HTML", "PDF"],
            index=0
        )
        
        include_metadata = st.checkbox("Incluir metadatos", value=True)
    
    with col2:
        template_type = st.selectbox(
            "Tipo de plantilla",
            ["Estándar", "Personalizada", "Minimalista", "Detallada"],
            index=0
        )
        
        include_original_text = st.checkbox("Incluir texto original", value=False)
    
    # Configuración del campo JSON
    st.markdown("#### Configuración del Campo JSON")
    
    json_config = st.text_area(
        "Configuración JSON",
        value=get_default_json_config(),
        height=200,
        help="Define la estructura JSON que se aplicará a los datos procesados."
    )
    
    # Validar JSON
    try:
        json.loads(json_config)
        st.success("✅ Configuración JSON válida")
    except json.JSONDecodeError as e:
        st.error(f"❌ Error en la configuración JSON: {e}")
        return
    
    # Botón de conversión
    if st.button("🔄 Convertir a Formato", type="primary"):
        convert_to_format(llm_results, output_format, json_config, template_type, include_metadata, include_original_text)


def render_results_tab(program_id: int):
    """Tab de resultados"""
    st.markdown("### 📊 Resultados del Procesamiento")
    
    # Verificar si hay resultados de conversión
    conversion_results = st.session_state.get("conversion_results", [])
    if not conversion_results:
        st.warning("⚠️ No hay resultados de conversión. Completa el proceso de conversión primero.")
        return
    
    st.success(f"✅ {len(conversion_results)} resultado(s) de conversión disponible(s)")
    
    # Mostrar resumen
    render_results_summary(conversion_results)
    
    # Mostrar resultados detallados
    render_detailed_results(conversion_results)
    
    # Opciones de exportación
    render_export_options(conversion_results)


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


def select_all_files(files: List[Dict]):
    """Selecciona todos los archivos de la lista"""
    for file in files:
        file["selected"] = True
    st.rerun()


def deselect_all_files(files: List[Dict]):
    """Deselecciona todos los archivos de la lista"""
    for file in files:
        file["selected"] = False
    st.rerun()


def search_files(program_id: int, query: str, file_type: str, status: str):
    """Busca archivos según los criterios especificados"""
    # Esta función se conectaría con la API real
    st.info(f"🔍 Buscando archivos con: '{query}', tipo: '{file_type}', estado: '{status}'")
    # Por ahora solo refrescamos la página
    st.rerun()


def process_files_with_llm(files: List[Dict], model: str, temperature: float, max_tokens: int, language: str, prompt: str):
    """Procesa archivos seleccionados con LLM"""
    st.info("🚀 Iniciando procesamiento con LLM...")
    
    # Simular procesamiento
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    
    for i, file in enumerate(files):
        status_text.text(f"Procesando: {file['name']}")
        
        # Simular tiempo de procesamiento
        time.sleep(1)
        
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
                "processing_time": 1.2
            }
        }
        results.append(result)
        
        progress_bar.progress((i + 1) / len(files))
    
    # Guardar resultados en session state
    st.session_state["llm_processing_results"] = results
    
    status_text.text("✅ Procesamiento completado")
    st.success(f"✅ {len(results)} archivo(s) procesado(s) exitosamente")
    
    # Mostrar resumen de resultados
    st.markdown("#### Resumen del Procesamiento")
    for result in results:
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


def get_default_json_config() -> str:
    """Retorna la configuración JSON por defecto"""
    return json.dumps({
        "documento": {
            "id": "{{file_id}}",
            "nombre": "{{file_name}}",
            "fecha_procesamiento": "{{processed_at}}",
            "metadatos": {
                "modelo_llm": "{{llm_model}}",
                "idioma": "{{language}}",
                "temperatura": "{{temperature}}"
            },
            "contenido_procesado": {
                "objetivos": "{{objetivos_principales}}",
                "metodologias": "{{metodologias_utilizadas}}",
                "resultados": "{{resultados_obtenidos}}",
                "conclusiones": "{{conclusiones_importantes}}",
                "recomendaciones": "{{recomendaciones}}",
                "resumen": "{{resumen_ejecutivo}}",
                "palabras_clave": "{{palabras_clave}}",
                "confianza": "{{confianza_score}}"
            }
        }
    }, indent=2)


def convert_to_format(llm_results: List[Dict], output_format: str, json_config: str, template_type: str, include_metadata: bool, include_original_text: bool):
    """Convierte los resultados del LLM al formato especificado"""
    st.info("🔄 Iniciando conversión de formato...")
    
    # Simular conversión
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    conversion_results = []
    
    for i, result in enumerate(llm_results):
        status_text.text(f"Convirtiendo: {result['file_name']}")
        
        # Simular tiempo de conversión
        time.sleep(0.5)
        
        # Generar resultado de conversión mockup
        converted_result = {
            "file_id": result["file_id"],
            "file_name": result["file_name"],
            "output_format": output_format,
            "converted_at": datetime.now().isoformat(),
            "converted_content": generate_mockup_converted_content(result, output_format, json_config),
            "metadata": {
                "template_type": template_type,
                "include_metadata": include_metadata,
                "include_original_text": include_original_text,
                "conversion_time": 0.5
            }
        }
        conversion_results.append(converted_result)
        
        progress_bar.progress((i + 1) / len(llm_results))
    
    # Guardar resultados en session state
    st.session_state["conversion_results"] = conversion_results
    
    status_text.text("✅ Conversión completada")
    st.success(f"✅ {len(conversion_results)} archivo(s) convertido(s) exitosamente")


def generate_mockup_converted_content(result: Dict, output_format: str, json_config: str) -> str:
    """Genera contenido convertido mockup"""
    if output_format == "JSON":
        return json.dumps({
            "documento": {
                "id": result["file_id"],
                "nombre": result["file_name"],
                "fecha_procesamiento": result["processed_at"],
                "metadatos": result["metadata"],
                "contenido_procesado": result["llm_response"]
            }
        }, indent=2, ensure_ascii=False)
    
    elif output_format == "XML":
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<documento id="{result['file_id']}">
    <nombre>{result['file_name']}</nombre>
    <fecha_procesamiento>{result['processed_at']}</fecha_procesamiento>
    <contenido_procesado>
        <objetivos>{json.dumps(result['llm_response']['objetivos_principales'])}</objetivos>
        <metodologias>{json.dumps(result['llm_response']['metodologias_utilizadas'])}</metodologias>
        <resultados>{json.dumps(result['llm_response']['resultados_obtenidos'])}</resultados>
        <conclusiones>{json.dumps(result['llm_response']['conclusiones_importantes'])}</conclusiones>
        <recomendaciones>{json.dumps(result['llm_response']['recomendaciones'])}</recomendaciones>
    </contenido_procesado>
</documento>"""
    
    elif output_format == "CSV":
        return f"ID,Nombre,Objetivos,Metodologias,Resultados,Conclusiones,Recomendaciones\n{result['file_id']},{result['file_name']},\"{json.dumps(result['llm_response']['objetivos_principales'])}\",\"{json.dumps(result['llm_response']['metodologias_utilizadas'])}\",\"{json.dumps(result['llm_response']['resultados_obtenidos'])}\",\"{json.dumps(result['llm_response']['conclusiones_importantes'])}\",\"{json.dumps(result['llm_response']['recomendaciones'])}\""
    
    elif output_format == "Markdown":
        return f"""# {result['file_name']}

## Objetivos Principales
{chr(10).join(f"- {obj}" for obj in result['llm_response']['objetivos_principales'])}

## Metodologías Utilizadas
{chr(10).join(f"- {met}" for met in result['llm_response']['metodologias_utilizadas'])}

## Resultados Obtenidos
{chr(10).join(f"- {res}" for res in result['llm_response']['resultados_obtenidos'])}

## Conclusiones Importantes
{chr(10).join(f"- {con}" for con in result['llm_response']['conclusiones_importantes'])}

## Recomendaciones
{chr(10).join(f"- {rec}" for rec in result['llm_response']['recomendaciones'])}

---
*Procesado el {result['processed_at']} con {result['metadata']['llm_model']}*
"""
    
    else:  # HTML
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>{result['file_name']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; }}
        ul {{ margin: 10px 0; }}
        li {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h1>{result['file_name']}</h1>
    
    <h2>Objetivos Principales</h2>
    <ul>
        {chr(10).join(f"<li>{obj}</li>" for obj in result['llm_response']['objetivos_principales'])}
    </ul>
    
    <h2>Metodologías Utilizadas</h2>
    <ul>
        {chr(10).join(f"<li>{met}</li>" for met in result['llm_response']['metodologias_utilizadas'])}
    </ul>
    
    <h2>Resultados Obtenidos</h2>
    <ul>
        {chr(10).join(f"<li>{res}</li>" for res in result['llm_response']['resultados_obtenidos'])}
    </ul>
    
    <h2>Conclusiones Importantes</h2>
    <ul>
        {chr(10).join(f"<li>{con}</li>" for con in result['llm_response']['conclusiones_importantes'])}
    </ul>
    
    <h2>Recomendaciones</h2>
    <ul>
        {chr(10).join(f"<li>{rec}</li>" for rec in result['llm_response']['recomendaciones'])}
    </ul>
    
    <hr>
    <p><em>Procesado el {result['processed_at']} con {result['metadata']['llm_model']}</em></p>
</body>
</html>"""


def render_results_summary(conversion_results: List[Dict]):
    """Renderiza el resumen de resultados"""
    st.markdown("#### Resumen de Conversión")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Archivos Procesados", len(conversion_results))
    
    with col2:
        total_size = sum(len(result["converted_content"]) for result in conversion_results)
        st.metric("Tamaño Total (KB)", round(total_size / 1024, 2))
    
    with col3:
        formats = list(set(result["output_format"] for result in conversion_results))
        st.metric("Formatos Generados", len(formats))
    
    with col4:
        avg_processing_time = sum(result["metadata"]["conversion_time"] for result in conversion_results) / len(conversion_results)
        st.metric("Tiempo Promedio (s)", round(avg_processing_time, 2))


def render_detailed_results(conversion_results: List[Dict]):
    """Renderiza los resultados detallados"""
    st.markdown("#### Resultados Detallados")
    
    for result in conversion_results:
        with st.expander(f"📄 {result['file_name']} ({result['output_format']})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.code(result["converted_content"], language=result["output_format"].lower())
            
            with col2:
                st.json(result["metadata"])


def render_export_options(conversion_results: List[Dict]):
    """Renderiza las opciones de exportación"""
    st.markdown("#### Opciones de Exportación")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Descargar Todo (ZIP)", type="primary"):
            st.info("🚧 Funcionalidad de descarga ZIP pendiente de implementación")
    
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
