"""
Sidebar de Retrieval del programa - VERSIÓN MEJORADA CON MONITOREO
"""
import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
from config import API_BASE_URL_INTERNAL
from auth_utils import make_authenticated_request


def render_retrieval_screen():
    """Renderiza la pantalla de retrieval"""
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
    
    st.markdown("## 🔍 Retrieval del Programa")
    st.markdown("Sistema de recuperación de información")
    
    # Verificar estado del backend
    render_backend_health_check()
    
    # Obtener datos del programa y estado de indexación
    program_data = get_program_data(selected_program_id)
    indexing_status = get_indexing_status(selected_program_id)
    file_stats = get_file_stats(selected_program_id)
    
    # Estado del sistema
    st.markdown("### Estado del Sistema")
    col1, col2, col3, col4 = st.columns(4)
    
    # Nivel de recuperación con estados dinámicos
    with col1:
        recovery_level = get_recovery_level(indexing_status, file_stats)
        st.metric("Nivel de recuperación", recovery_level)
    
    # Métricas dinámicas
    with col2:
        indexed_docs = file_stats.get("completed_files", 0) if file_stats else 0
        st.metric("Documentos Indexados", f"{indexed_docs:,}")
    
    with col3:
        st.metric("Consultas Procesadas", "89", "12")  # Placeholder
    
    with col4:
        st.metric("Tiempo Promedio", "0.3s", "-0.1s")  # Placeholder
    
    # Monitoreo detallado del estado de indexación
    render_indexing_status_details(selected_program_id, indexing_status, file_stats)
    
    # Botones de indexación
    render_indexing_buttons(selected_program_id, indexing_status, file_stats)
    
    # Última actualización
    last_update = get_last_update_time(indexing_status, file_stats)
    if last_update:
        st.success(f"✅ Sistema activo - Última actualización: {last_update}")
    else:
        st.info("ℹ️ Sistema listo para indexación")
    
    # Visualización del dataframe del repositorio
    render_repository_dataframe(selected_program_id, file_stats)


def check_backend_health():
    """Verifica si el backend está funcionando"""
    try:
        resp = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/", timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


def render_backend_health_check():
    """Renderiza el estado de salud del servicio"""
    st.markdown("#### Estado del Servicio Backend")
    
    if check_backend_health():
        st.success("✅ Backend funcionando correctamente")
    else:
        st.error("❌ Backend no disponible")
        st.warning("Verifica que el servicio backend esté ejecutándose en el puerto 7000")
        
        # Instrucciones para verificar el servicio
        st.markdown("**Para verificar el servicio manualmente:**")
        st.code("""
# Verificar contenedores Docker
docker-compose ps

# Ver logs del backend
docker-compose logs backend

# Verificar puerto
curl http://localhost:7000/
        """)
        
        if st.button("🔄 Verificar nuevamente"):
            st.rerun()


def render_indexing_status_details(program_id, indexing_status, file_stats):
    """Renderiza detalles del estado de indexación"""
    st.markdown("#### Estado del Servicio de Indexación")
    
    if indexing_status:
        status = indexing_status.get("status", "unknown")
        progress = indexing_status.get("progress", {})
        
        # Mostrar estado actual
        if status == "running":
            st.info("🔄 **Indexación en progreso**")
            render_indexing_progress(indexing_status)
        elif status == "completed":
            st.success("✅ **Indexación completada**")
        elif status == "failed":
            st.error("❌ **Indexación falló**")
        elif status == "pending":
            st.warning("⏳ **Indexación pendiente**")
        else:
            st.info(f"ℹ️ **Estado: {status}**")
        
        # Mostrar progreso si está disponible
        if progress:
            total = progress.get("total_files", 0)
            processed = progress.get("processed_files", 0)
            successful = progress.get("successful_files", 0)
            failed = progress.get("failed_files", 0)
            
            if total > 0:
                progress_percent = (processed / total) * 100
                st.progress(progress_percent / 100)
                st.caption(f"Progreso: {processed}/{total} archivos ({progress_percent:.1f}%)")
                
                # Métricas detalladas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total archivos", total)
                with col2:
                    st.metric("Procesados", processed)
                with col3:
                    st.metric("Exitosos", successful)
                with col4:
                    st.metric("Fallidos", failed)
        
        # Mostrar timestamps
        if indexing_status.get("started_at"):
            st.caption(f"🕐 Iniciado: {indexing_status['started_at']}")
        if indexing_status.get("completed_at"):
            st.caption(f"✅ Completado: {indexing_status['completed_at']}")
        if indexing_status.get("error_message"):
            st.error(f"❌ Error: {indexing_status['error_message']}")
    
    else:
        st.info("ℹ️ No hay trabajos de indexación activos")
    
    # Botón para refrescar estado
    if st.button("🔄 Refrescar estado", key="refresh_indexing_status"):
        st.rerun()


def render_indexing_progress(indexing_status):
    """Renderiza el progreso de indexación en tiempo real"""
    st.markdown("#### Progreso de Indexación")
    
    progress = indexing_status.get("progress", {})
    total = progress.get("total_files", 0)
    processed = progress.get("processed_files", 0)
    successful = progress.get("successful_files", 0)
    failed = progress.get("failed_files", 0)
    
    if total > 0:
        progress_percent = (processed / total) * 100
        
        # Barra de progreso principal
        st.progress(progress_percent / 100)
        st.caption(f"Procesando archivos: {processed}/{total} ({progress_percent:.1f}%)")
        
        # Métricas en tiempo real
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", total)
        with col2:
            st.metric("Procesados", processed, f"+{processed}")
        with col3:
            st.metric("Exitosos", successful, f"+{successful}")
        with col4:
            st.metric("Fallidos", failed, f"+{failed}")
        
        # Auto-refresh cada 5 segundos si está indexando
        if indexing_status.get("status") == "running":
            st.markdown("🔄 Actualizando automáticamente...")
            time.sleep(5)
            st.rerun()
    else:
        st.info("⏳ Preparando indexación...")
        time.sleep(2)
        st.rerun()


def get_program_data(program_id):
    """Obtiene los datos del programa"""
    try:
        resp = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/api/programs/{program_id}", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


def get_indexing_status(program_id):
    """Obtiene el estado de indexación del programa"""
    try:
        resp = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/api/indexing/jobs/{program_id}", timeout=10)
        if resp.status_code == 200:
            jobs = resp.json()
            # Retornar el trabajo más reciente
            if jobs:
                return jobs[0]  # Asumiendo que están ordenados por fecha
        return None
    except Exception:
        return None


def get_file_stats(program_id):
    """Obtiene estadísticas de archivos indexados"""
    try:
        resp = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/api/indexing/files/{program_id}/stats", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


def get_recovery_level(indexing_status, file_stats):
    """Determina el nivel de recuperación basado en el estado de indexación"""
    if not indexing_status and not file_stats:
        return "Carpeta validada"
    
    if indexing_status and indexing_status.get("status") == "completed":
        return "Carpeta indexada"
    elif indexing_status and indexing_status.get("status") == "running":
        return "Indexando..."
    elif file_stats and file_stats.get("completed_files", 0) > 0:
        return "Carpeta indexada"
    else:
        return "Carpeta validada"


def get_last_update_time(indexing_status, file_stats):
    """Obtiene el tiempo de la última actualización"""
    if indexing_status and indexing_status.get("completed_at"):
        return f"hace {datetime.now().hour - 2} horas"  # Placeholder
    elif file_stats and file_stats.get("last_updated"):
        return f"hace {datetime.now().hour - 1} horas"  # Placeholder
    return None


def render_indexing_buttons(program_id, indexing_status, file_stats):
    """Renderiza los botones de indexación según el estado"""
    st.markdown("### Acciones de Indexación")
    
    # Determinar si ya se ha indexado
    is_indexed = (
        (indexing_status and indexing_status.get("status") == "completed") or
        (file_stats and file_stats.get("completed_files", 0) > 0)
    )
    
    # Determinar si está indexando actualmente
    is_indexing = indexing_status and indexing_status.get("status") == "running"
    
    if is_indexing:
        # Mostrar progreso de indexación
        st.info("🔄 **Indexación en progreso - Los botones están deshabilitados**")
    elif not is_indexed:
        # Estado inicial - solo botón de iniciar indexación
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            if st.button("🚀 Iniciar indexación", type="primary", use_container_width=True):
                start_indexing(program_id)
    else:
        # Ya indexado - botones de reindexar y enriquecimiento
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🔄 Reindexar", use_container_width=True):
                start_indexing(program_id)
        with col2:
            if st.button("✨ Iniciar enriquecimiento", use_container_width=True):
                st.info("🚧 Funcionalidad de enriquecimiento pendiente de implementación")


def start_indexing(program_id):
    """Inicia el proceso de indexación"""
    try:
        data = {
            "program_id": program_id,
            "job_type": "full_scan",
            "include_trashed": False
        }
        
        resp = make_authenticated_request(
            "POST", 
            f"{API_BASE_URL_INTERNAL}/api/indexing/scan", 
            json=data,
            timeout=30
        )
        
        if resp.status_code == 200:
            result = resp.json()
            st.success(f"✅ Indexación iniciada exitosamente. Job ID: {result.get('job_id')}")
            st.rerun()
        else:
            error_msg = resp.json().get("detail", "Error desconocido")
            st.error(f"❌ Error al iniciar indexación: {error_msg}")
    except Exception as e:
        st.error(f"❌ Error de conexión: {str(e)}")


def render_repository_dataframe(program_id, file_stats):
    """Renderiza el dataframe del repositorio si existe"""
    if not file_stats or file_stats.get("completed_files", 0) == 0:
        return  # No mostrar la sección si no hay datos
    
    st.markdown("### 📊 Repositorio Indexado")
    
    # Obtener archivos indexados
    try:
        resp = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/api/indexing/files/{program_id}?limit=100", timeout=10)
        if resp.status_code == 200:
            files = resp.json()
            
            if files:
                # Crear DataFrame
                df_data = []
                for file in files:
                    df_data.append({
                        "Nombre": file.get("drive_file_name", ""),
                        "Tipo": file.get("file_type", ""),
                        "Tamaño (KB)": round(file.get("file_size", 0) / 1024, 2),
                        "Estado": file.get("indexing_status", ""),
                        "Última modificación": file.get("drive_modified_time", ""),
                        "Ruta": file.get("drive_file_path", "")
                    })
                
                df = pd.DataFrame(df_data)
                
                # Mostrar estadísticas resumidas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total archivos", len(files))
                with col2:
                    completed = len([f for f in files if f.get("indexing_status") == "completed"])
                    st.metric("Completados", completed)
                with col3:
                    failed = len([f for f in files if f.get("indexing_status") == "failed"])
                    st.metric("Fallidos", failed)
                with col4:
                    total_size = sum(f.get("file_size", 0) for f in files)
                    st.metric("Tamaño total (MB)", round(total_size / (1024 * 1024), 2))
                
                # Mostrar tabla
                st.dataframe(
                    df,
                    use_container_width=True,
                    height=400,
                    column_config={
                        "Nombre": st.column_config.TextColumn("Nombre del archivo", width="medium"),
                        "Tipo": st.column_config.TextColumn("Tipo", width="small"),
                        "Tamaño (KB)": st.column_config.NumberColumn("Tamaño (KB)", width="small"),
                        "Estado": st.column_config.TextColumn("Estado", width="small"),
                        "Última modificación": st.column_config.DatetimeColumn("Última modificación", width="medium"),
                        "Ruta": st.column_config.TextColumn("Ruta", width="large")
                    }
                )
            else:
                st.info("No hay archivos indexados aún.")
        else:
            st.warning("No se pudieron cargar los archivos del repositorio.")
    except Exception as e:
        st.warning(f"Error al cargar archivos del repositorio: {str(e)}")
