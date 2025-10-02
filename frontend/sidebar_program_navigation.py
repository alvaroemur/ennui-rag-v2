"""
Sidebar de navegación del programa
"""
import streamlit as st


def render_program_navigation_sidebar():
    """Renderiza el sidebar de navegación del programa"""
    # Solo mostrar sidebar de navegación en vistas del programa abierto
    current_view = st.session_state.get("view", "")
    views_with_navigation = ["homepage", "program_config", "tracking", "dashboard", "retrieval", "search"]
    
    if (st.session_state.get("jwt") or st.session_state.get("session_id")) and current_view in views_with_navigation:
        with st.sidebar:
            st.markdown("### 🧭 Navegación")
            
            # Bloque: Gestión del programa
            st.markdown("#### 📊 Gestión del programa")
            
            # Botón: Configuración
            if st.button("⚙️ Configuración", key="sidebar_config", use_container_width=True):
                st.session_state["view"] = "program_config"
                st.rerun()
            
            # Botón: Seguimiento
            if st.button("📈 Seguimiento", key="sidebar_tracking", use_container_width=True):
                st.session_state["view"] = "tracking"
                st.rerun()
            
            # Botón: Dashboard
            if st.button("📊 Dashboard", key="sidebar_dashboard", use_container_width=True):
                st.session_state["view"] = "dashboard"
                st.rerun()
            
            st.divider()
            
            # Bloque: Carpeta
            st.markdown("#### 📁 Carpeta")
            
            # Botón: Retrieval
            if st.button("🔍 Retrieval", key="sidebar_retrieval", use_container_width=True):
                st.session_state["view"] = "retrieval"
                st.rerun()
            
            # Botón: Search
            if st.button("🔎 Search", key="sidebar_search", use_container_width=True):
                st.session_state["view"] = "search"
                st.rerun()
            
            st.divider()
            
            # Botón: Volver a selección de programa
            if st.button("🏠 Volver a Programas", key="sidebar_back", use_container_width=True):
                st.session_state["view"] = "program_selection"
                st.rerun()
