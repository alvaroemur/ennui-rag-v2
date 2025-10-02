"""
Pantalla de Seguimiento del programa
"""
import streamlit as st


def render_program_tracking():
    """Renderiza la pantalla de seguimiento del programa"""
    # Botón para volver
    if st.button("← Volver al Homepage"):
        st.session_state["view"] = "homepage"
        st.rerun()
    
    st.markdown("## 📈 Seguimiento del Programa (en desarrollo)")
    st.markdown("Monitorea el progreso y avance del programa")
    
    # Placeholder para contenido de seguimiento
    st.info("🚧 Pantalla de seguimiento en desarrollo")
    st.markdown("Aquí se mostrarán métricas de progreso, participantes activos, índices de cumplimiento, etc.")
    
    # Métricas de ejemplo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avance General", "68%", "5%")
    with col2:
        st.metric("Participantes Activos", "12", "2")
    with col3:
        st.metric("Cumplimiento", "85%", "3%")