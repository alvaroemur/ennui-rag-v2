"""
Sidebar de Search del programa
"""
import streamlit as st


def render_search_screen():
    """Renderiza la pantalla de search"""
    # Botón para volver
    if st.button("← Volver al Homepage"):
        st.session_state["view"] = "homepage"
        st.rerun()
    
    st.markdown("## 🔎 Search del Programa")
    st.markdown("Motor de búsqueda avanzada")
    
    # Placeholder para contenido de search
    st.info("🚧 Pantalla de search en desarrollo")
    st.markdown("Aquí se mostrará el motor de búsqueda avanzada del programa")
    
    # Estado del sistema
    st.markdown("### Estado del Sistema")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Búsquedas Realizadas", "156", "8")
    with col2:
        st.metric("Resultados Generados", "1.2K", "45")
    with col3:
        st.metric("Precisión", "94%", "2%")
    
    # Última actualización
    st.success("✅ Sistema activo - Índice actualizado: hace 1 hora")