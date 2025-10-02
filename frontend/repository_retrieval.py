"""
Sidebar de Retrieval del programa
"""
import streamlit as st


def render_retrieval_screen():
    """Renderiza la pantalla de retrieval"""
    # Botón para volver
    if st.button("← Volver al Homepage"):
        st.session_state["view"] = "homepage"
        st.rerun()
    
    st.markdown("## 🔍 Retrieval del Programa")
    st.markdown("Sistema de recuperación de información")
    
    # Placeholder para contenido de retrieval
    st.info("🚧 Pantalla de retrieval en desarrollo")
    st.markdown("Aquí se mostrará el sistema de recuperación de información del programa")
    
    # Estado del sistema
    st.markdown("### Estado del Sistema")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Documentos Indexados", "1,247", "23")
    with col2:
        st.metric("Consultas Procesadas", "89", "12")
    with col3:
        st.metric("Tiempo Promedio", "0.3s", "-0.1s")
    
    # Última actualización
    st.success("✅ Sistema activo - Última actualización: hace 2 horas")