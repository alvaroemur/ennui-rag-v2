"""
Homepage del programa seleccionado con tarjetas
"""
import streamlit as st


def render_homepage():
    """Renderiza el homepage del programa con tarjetas"""
    # Contenido principal (sidebar se renderiza en app.py)
    render_homepage_content()


def render_homepage_content():
    """Renderiza el contenido principal del homepage"""
    st.markdown("## 🏠 Homepage del Programa")
    
    # Bloque: Gestión del programa
    st.markdown("### 📊 Gestión del programa")
    
    col1, col2, col3 = st.columns(3)
    
    # Tarjeta: Configuración
    with col1:
        render_configuration_card()
    
    # Tarjeta: Seguimiento
    with col2:
        render_tracking_card()
    
    # Tarjeta: Dashboard
    with col3:
        render_dashboard_card()
    
    st.divider()
    
    # Bloque: Carpeta
    st.markdown("### 📁 Carpeta")
    
    col1, col2 = st.columns(2)
    
    # Tarjeta: Retrieval
    with col1:
        render_retrieval_card()
    
    # Tarjeta: Search
    with col2:
        render_search_card()


def render_configuration_card():
    """Renderiza la tarjeta de Configuración"""
    with st.container(border=True, height=500):
        st.markdown("#### ⚙️ Configuración")
        st.markdown("Configura los parámetros y datos del programa")
        
        # Datos vivos - Barra de progreso
        st.markdown("**Progreso de configuración:**")
        progress = 75
        st.progress(progress / 100)
        st.caption(f"{progress}% completado")
        
        # Mensaje de estado
        remaining = 3
        st.warning(f"Te falta completar {remaining} secciones")
        
        # Botón de entrada
        if st.button("Entrar", key="config_enter", use_container_width=True):
            st.session_state["view"] = "program_config"
            st.rerun()


def render_tracking_card():
    """Renderiza la tarjeta de Seguimiento"""
    with st.container(border=True, height=500):
        st.markdown("#### 📈 Seguimiento")
        st.markdown("Monitorea el progreso y avance del programa")
        
        # Datos vivos - Métricas
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Avance", "68%", "5%")
            st.metric("Participantes", "12", "2")
        
        with col2:
            st.metric("Cumplimiento", "85%", "3%")
            st.metric("Activos", "8", "1")
        
        # Botón de entrada
        if st.button("Entrar", key="tracking_enter", use_container_width=True):
            st.session_state["view"] = "tracking"
            st.rerun()


def render_dashboard_card():
    """Renderiza la tarjeta de Dashboard"""
    with st.container(border=True, height=500):
        st.markdown("#### 📊 Dashboard")
        st.markdown("Indicadores y métricas clave del programa")
        
        # Datos vivos - Indicadores
        st.markdown("**Indicadores principales:**")
        
        # Indicador 1
        st.markdown("🌱 **Crecimiento de negocios**")
        st.progress(0.8)
        st.caption("80% - Objetivo alcanzado")
        
        # Indicador 2
        st.markdown("🤝 **Conexiones efectivas**")
        st.progress(0.6)
        st.caption("60% - En progreso")
        
        # Indicador 3
        st.markdown("💰 **Fundraising**")
        st.progress(0.4)
        st.caption("40% - Necesita atención")
        
        # Botón de entrada
        if st.button("Entrar", key="dashboard_enter", use_container_width=True):
            st.session_state["view"] = "dashboard"
            st.rerun()


def render_retrieval_card():
    """Renderiza la tarjeta de Retrieval"""
    with st.container(border=True, height=500):
        st.markdown("#### 🔍 Retrieval")
        st.markdown("Sistema de recuperación de información")
        
        # Datos vivos - Placeholder
        st.markdown("**Estado del sistema:**")
        st.success("✅ Activo")
        st.caption("Última actualización: hace 2 horas")
        
        # Métricas placeholder
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documentos", "1,247", "23")
        with col2:
            st.metric("Consultas", "89", "12")
        
        # Botón de entrada
        if st.button("Entrar", key="retrieval_enter", use_container_width=True):
            st.session_state["view"] = "retrieval"
            st.rerun()


def render_search_card():
    """Renderiza la tarjeta de Search"""
    with st.container(border=True, height=500):
        st.markdown("#### 🔎 Search")
        st.markdown("Motor de búsqueda avanzada")
        
        # Datos vivos - Placeholder
        st.markdown("**Estado del sistema:**")
        st.success("✅ Activo")
        st.caption("Índice actualizado: hace 1 hora")
        
        # Métricas placeholder
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Búsquedas", "156", "8")
        with col2:
            st.metric("Resultados", "1.2K", "45")
        
        # Botón de entrada
        if st.button("Entrar", key="search_enter", use_container_width=True):
            st.session_state["view"] = "search"
            st.rerun()
