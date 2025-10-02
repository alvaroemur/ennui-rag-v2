import streamlit as st
from config import CUSTOM_CSS
from sidebar_notifications import initialize_notifications, render_notifications_panel, render_toast
from sidebar_program_navigation import render_program_navigation_sidebar
from navbar import render_navbar
from login_screen import render_login_screen, handle_login_redirect
from create_program_screen import render_create_program_screen
from program_config import render_program_config_screen
from program_selection import render_program_selection
from homepage import render_homepage
from program_tracking import render_program_tracking
from program_mel import render_dashboard_screen
from repository_retrieval import render_retrieval_screen
from repository_search import render_search_screen

st.set_page_config(layout="wide", page_title="ennui-rag 2.0")

# Aplicar CSS personalizado
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Inicializar session state
if "jwt" not in st.session_state:
    st.session_state["jwt"] = None
if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None
if "session_id" not in st.session_state:
    st.session_state["session_id"] = None

# Inicializar sistema de notificaciones
initialize_notifications()

# Manejar redirección de login
handle_login_redirect()

# Verificar autenticación (session-based o token-based)
is_authenticated = False

if st.session_state.get("session_id"):
    # Session-based authentication - assume valid if session_id exists
    # Validation will happen when making authenticated requests
    is_authenticated = True
elif st.session_state.get("jwt"):
    # Legacy token-based authentication
    is_authenticated = True


# Mostrar pantalla de login si no está autenticado
if not is_authenticated:
    render_login_screen()

# Área autenticada
if is_authenticated:
    # Configurar breadcrumbs según la vista actual
    nav_title = "ennui-rag 2.0"
    if "view" in st.session_state and st.session_state["view"] == "create_program":
        render_navbar(nav_title, ["Programas", "Crear programa"])
    elif "view" in st.session_state and st.session_state["view"] == "program_config":
        render_navbar(nav_title, ["Programas", "Homepage", "Configuración"])
    elif "view" in st.session_state and st.session_state["view"] == "tracking":
        render_navbar(nav_title, ["Programas", "Homepage", "Seguimiento"])
    elif "view" in st.session_state and st.session_state["view"] == "dashboard":
        render_navbar(nav_title, ["Programas", "Homepage", "Dashboard"])
    elif "view" in st.session_state and st.session_state["view"] == "retrieval":
        render_navbar(nav_title, ["Programas", "Homepage", "Retrieval"])
    elif "view" in st.session_state and st.session_state["view"] == "search":
        render_navbar(nav_title, ["Programas", "Homepage", "Search"])
    elif "view" in st.session_state and st.session_state["view"] == "homepage":
        render_navbar(nav_title, ["Programas", "Homepage"])
    else:
        render_navbar(nav_title, ["Programas"])

    # Renderizar sidebar (navegación o notificaciones)
    render_program_navigation_sidebar()
    render_notifications_panel()
    render_toast()

    # Inicializar vista si no está definida
    if "view" not in st.session_state:
        st.session_state["view"] = "program_selection"  # program_selection | create_program | homepage | program_config | tracking | dashboard | retrieval | search

    # Renderizar pantallas según la vista actual
    if st.session_state["view"] == "create_program":
        render_create_program_screen()
    elif st.session_state["view"] == "homepage":
        render_homepage()
    elif st.session_state["view"] == "program_config":
        render_program_config_screen()
    elif st.session_state["view"] == "tracking":
        render_program_tracking()
    elif st.session_state["view"] == "dashboard":
        render_dashboard_screen()
    elif st.session_state["view"] == "retrieval":
        render_retrieval_screen()
    elif st.session_state["view"] == "search":
        render_search_screen()
    else:
        # Vista principal (selección de programa)
        render_program_selection()
