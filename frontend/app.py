import streamlit as st
from config import CUSTOM_CSS
from notifications import initialize_notifications, render_notifications_panel, render_toast
from navbar import render_navbar
from login_screen import render_login_screen, handle_login_redirect
from create_program_screen import render_create_program_screen
from program_config_screen import render_program_config_screen
from main_dashboard import render_main_dashboard

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
    # Session-based authentication
    from auth_utils import validate_session
    st.write(f"DEBUG: Attempting session-based authentication")
    if validate_session():
        is_authenticated = True
        st.write(f"DEBUG: Session-based authentication successful")
    else:
        st.write(f"DEBUG: Session-based authentication failed")
elif st.session_state.get("jwt"):
    # Legacy token-based authentication
    st.write(f"DEBUG: Using legacy token-based authentication")
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
        render_navbar(nav_title, ["Programas", "Configuración"])
    else:
        render_navbar(nav_title, ["Programas"])

    # Renderizar notificaciones
    render_notifications_panel()
    render_toast()

    # Inicializar vista si no está definida
    if "view" not in st.session_state:
        st.session_state["view"] = "home"  # home | create_program | program_config

    # Renderizar pantallas según la vista actual
    if st.session_state["view"] == "create_program":
        render_create_program_screen()
    elif st.session_state["view"] == "program_config":
        render_program_config_screen()
    else:
        # Vista principal (home)
        render_main_dashboard()
