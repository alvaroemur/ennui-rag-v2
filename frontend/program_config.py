"""
Pantalla de configuración de programa
"""
import streamlit as st
import requests
from config import API_BASE_URL_INTERNAL


def render_program_config_screen():
    """Renderiza la pantalla de configuración de programa"""
    # Obtener datos del programa seleccionado
    selected_program_id = st.session_state.get("selected_program_id")
    if not selected_program_id:
        st.error("No se ha seleccionado un programa.")
        st.button("Volver", on_click=lambda: st.session_state.update({"view": "homepage"}))
        st.stop()

    headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}

    # Obtener datos del programa
    try:
        resp = requests.get(f"{API_BASE_URL_INTERNAL}/api/programs/{selected_program_id}", headers=headers, timeout=10)
        if resp.status_code == 200:
            program_data = resp.json()
        else:
            st.error("No se pudo cargar la información del programa.")
            st.button("Volver", on_click=lambda: st.session_state.update({"view": "homepage"}))
            st.stop()
    except Exception:
        st.error("Error de conexión al cargar el programa.")
        st.button("Volver", on_click=lambda: st.session_state.update({"view": "homepage"}))
        st.stop()

    # Botón para volver
    if st.button("← Volver al Homepage"):
        st.session_state["view"] = "homepage"
        st.rerun()
    
    st.title(f"Configuración del Programa: {program_data.get('name', 'Sin nombre')}")

    # Tabs para las diferentes secciones
    tab1, tab2, tab3 = st.tabs(["📝 Datos del Programa", "🎯 Alcance", "🔄 Teoría de Cambio"])

    with tab1:
        render_program_data_tab(program_data)

    with tab2:
        render_scope_tab()

    with tab3:
        render_theory_of_change_tab()

    st.stop()


def render_program_data_tab(program_data):
    """Renderiza la pestaña de datos del programa"""
    st.header("Actualización de Datos del Programa")
    st.info("Esta sección permite actualizar los datos definidos al crear el programa.")
    
    with st.form("update_program_data"):
        col1, col2 = st.columns(2)
        
        with col1:
            internal_code = st.text_input(
                "Código interno", 
                value=program_data.get('internal_code', ''),
                max_chars=100,
                help="Código único interno del programa"
            )
            name = st.text_input(
                "Nombre del programa", 
                value=program_data.get('name', ''),
                max_chars=200,
                help="Nombre oficial del programa"
            )
            main_client = st.text_input(
                "Cliente principal", 
                value=program_data.get('main_client', ''),
                help="Organización o entidad que financia el programa"
            )
        
        with col2:
            main_beneficiaries = st.text_input(
                "Beneficiarios principales", 
                value=program_data.get('main_beneficiaries', ''),
                help="Grupo objetivo del programa"
            )
            start_date = st.date_input(
                "Fecha de inicio", 
                value=program_data.get('start_date'),
                help="Fecha de inicio del programa"
            )
            end_date = st.date_input(
                "Fecha de fin", 
                value=program_data.get('end_date'),
                help="Fecha de finalización del programa"
            )
        
        st.markdown("---")
        st.markdown("**Estado actual:** Mockup - Funcionalidad de actualización pendiente de implementación")
        
        col_save, col_cancel = st.columns([1, 4])
        with col_save:
            if st.form_submit_button("💾 Guardar Cambios", type="primary"):
                st.info("Funcionalidad de guardado pendiente de implementación")
        with col_cancel:
            if st.form_submit_button("❌ Cancelar"):
                st.rerun()


def render_scope_tab():
    """Renderiza la pestaña de alcance del programa"""
    st.header("Alcance del Programa")
    st.info("Define los objetivos y fases del programa para establecer el alcance.")
    
    with st.expander("🎯 Objetivos del Programa", expanded=True):
        st.markdown("**Objetivo General:**")
        st.text_area(
            "Describe el objetivo principal del programa",
            placeholder="Ejemplo: Mejorar la calidad de vida de las comunidades rurales mediante el acceso a servicios básicos...",
            height=100,
            help="Objetivo general que el programa busca alcanzar"
        )
        
        st.markdown("**Objetivos Específicos:**")
        for i in range(3):
            st.text_input(
                f"Objetivo específico {i+1}",
                placeholder=f"Objetivo específico {i+1}...",
                key=f"specific_objective_{i}",
                help="Objetivos específicos y medibles del programa"
            )
    
    with st.expander("📋 Definición de Fases", expanded=True):
        st.markdown("**Fases del Programa:**")
        
        phases = ["Fase 1: Inicio", "Fase 2: Desarrollo", "Fase 3: Consolidación", "Fase 4: Cierre"]
        for i, phase in enumerate(phases):
            with st.container(border=True):
                st.markdown(f"**{phase}**")
                col_desc, col_dates = st.columns([2, 1])
                
                with col_desc:
                    st.text_area(
                        f"Descripción de {phase}",
                        placeholder=f"Describe las actividades y resultados esperados en {phase.lower()}...",
                        height=80,
                        key=f"phase_desc_{i}"
                    )
                
                with col_dates:
                    st.date_input(
                        f"Inicio {phase}",
                        key=f"phase_start_{i}",
                        help="Fecha de inicio de la fase"
                    )
                    st.date_input(
                        f"Fin {phase}",
                        key=f"phase_end_{i}",
                        help="Fecha de fin de la fase"
                    )
    
    st.markdown("---")
    st.markdown("**Estado actual:** Mockup - Funcionalidad de alcance pendiente de implementación")


def render_theory_of_change_tab():
    """Renderiza la pestaña de teoría de cambio"""
    st.header("Teoría de Cambio")
    st.info("Define los indicadores encadenados en tres niveles: Producto, Resultados e Impacto.")
    
    # Nivel 1: Producto
    with st.expander("📦 Nivel 1: Productos", expanded=True):
        st.markdown("**Indicadores de Producto:**")
        st.markdown("*Los productos son los bienes y servicios que se entregan directamente a los beneficiarios.*")
        
        for i in range(3):
            with st.container(border=True):
                st.markdown(f"**Producto {i+1}**")
                col_name, col_metric = st.columns([2, 1])
                
                with col_name:
                    st.text_input(
                        f"Nombre del producto {i+1}",
                        placeholder=f"Ejemplo: Talleres de capacitación, Material educativo, etc.",
                        key=f"product_name_{i}",
                        help="Nombre del producto o servicio entregado"
                    )
                
                with col_metric:
                    st.number_input(
                        f"Cantidad objetivo {i+1}",
                        min_value=0,
                        value=0,
                        key=f"product_quantity_{i}",
                        help="Cantidad objetivo del producto"
                    )
                
                st.text_area(
                    f"Descripción del producto {i+1}",
                    placeholder="Describe el producto, sus características y cómo se entrega...",
                    height=60,
                    key=f"product_desc_{i}"
                )
    
    # Nivel 2: Resultados
    with st.expander("📈 Nivel 2: Resultados", expanded=True):
        st.markdown("**Indicadores de Resultados:**")
        st.markdown("*Los resultados son los cambios en el comportamiento, conocimiento o actitudes de los beneficiarios.*")
        
        for i in range(3):
            with st.container(border=True):
                st.markdown(f"**Resultado {i+1}**")
                
                st.text_input(
                    f"Nombre del resultado {i+1}",
                    placeholder=f"Ejemplo: Aumento en conocimientos, Cambio de comportamiento, etc.",
                    key=f"result_name_{i}",
                    help="Nombre del resultado esperado"
                )
                
                col_metric, col_time = st.columns([1, 1])
                with col_metric:
                    st.number_input(
                        f"Porcentaje objetivo {i+1}",
                        min_value=0,
                        max_value=100,
                        value=0,
                        key=f"result_percentage_{i}",
                        help="Porcentaje objetivo del resultado"
                    )
                with col_time:
                    st.selectbox(
                        f"Plazo {i+1}",
                        ["Corto plazo", "Mediano plazo", "Largo plazo"],
                        key=f"result_timeframe_{i}",
                        help="Plazo esperado para el resultado"
                    )
                
                st.text_area(
                    f"Descripción del resultado {i+1}",
                    placeholder="Describe el resultado esperado y cómo se medirá...",
                    height=60,
                    key=f"result_desc_{i}"
                )
    
    # Nivel 3: Impacto
    with st.expander("🌟 Nivel 3: Impacto", expanded=True):
        st.markdown("**Indicadores de Impacto:**")
        st.markdown("*El impacto son los cambios a largo plazo en las condiciones de vida de los beneficiarios.*")
        
        for i in range(2):
            with st.container(border=True):
                st.markdown(f"**Impacto {i+1}**")
                
                st.text_input(
                    f"Nombre del impacto {i+1}",
                    placeholder=f"Ejemplo: Mejora en calidad de vida, Reducción de pobreza, etc.",
                    key=f"impact_name_{i}",
                    help="Nombre del impacto esperado"
                )
                
                col_metric, col_time = st.columns([1, 1])
                with col_metric:
                    st.number_input(
                        f"Porcentaje objetivo {i+1}",
                        min_value=0,
                        max_value=100,
                        value=0,
                        key=f"impact_percentage_{i}",
                        help="Porcentaje objetivo del impacto"
                    )
                with col_time:
                    st.selectbox(
                        f"Plazo {i+1}",
                        ["Mediano plazo", "Largo plazo", "Muy largo plazo"],
                        key=f"impact_timeframe_{i}",
                        help="Plazo esperado para el impacto"
                    )
                
                st.text_area(
                    f"Descripción del impacto {i+1}",
                    placeholder="Describe el impacto esperado y cómo se medirá...",
                    height=60,
                    key=f"impact_desc_{i}"
                )
    
    st.markdown("---")
    st.markdown("**Estado actual:** Mockup - Funcionalidad de teoría de cambio pendiente de implementación")
    
    # Botones de acción
    col_save, col_reset, col_cancel = st.columns([1, 1, 3])
    with col_save:
        if st.button("💾 Guardar Teoría de Cambio", type="primary"):
            st.info("Funcionalidad de guardado pendiente de implementación")
    with col_reset:
        if st.button("🔄 Reiniciar"):
            st.rerun()
    with col_cancel:
        if st.button("❌ Cancelar"):
            st.rerun()
