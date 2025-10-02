"""
Pantalla de Dashboard del programa
"""
import streamlit as st


def render_dashboard_screen():
    """Renderiza la pantalla de dashboard del programa"""
    # Botón para volver
    if st.button("← Volver al Homepage", key="back_to_homepage_mel"):
        st.session_state["view"] = "homepage"
        st.rerun()
    
    st.markdown("## 📊 Dashboard del Programa")
    st.markdown("Indicadores y métricas clave del programa")
    
    # Placeholder para contenido de dashboard
    st.info("🚧 Pantalla de dashboard en desarrollo")
    st.markdown("Aquí se mostrarán los indicadores más relevantes del programa")
    
    # Indicadores de ejemplo
    st.markdown("### Indicadores Principales")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🌱 Crecimiento de Negocios")
        st.progress(0.8)
        st.caption("80% - Objetivo alcanzado")
        
        st.markdown("#### 🤝 Conexiones Efectivas")
        st.progress(0.6)
        st.caption("60% - En progreso")
    
    with col2:
        st.markdown("#### 💰 Fundraising")
        st.progress(0.4)
        st.caption("40% - Necesita atención")
        
        st.markdown("#### 📈 Impacto Social")
        st.progress(0.7)
        st.caption("70% - Buen progreso")
