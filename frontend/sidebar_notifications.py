"""
Sistema de notificaciones para la aplicación
"""
import streamlit as st
from typing import Optional, List


def initialize_notifications():
    """Inicializa el sistema de notificaciones en session_state"""
    if "notifications" not in st.session_state:
        st.session_state["notifications"] = []
    if "show_notifications" not in st.session_state:
        st.session_state["show_notifications"] = False
    if "unread_count" not in st.session_state:
        st.session_state["unread_count"] = 0
    if "show_toast" not in st.session_state:
        st.session_state["show_toast"] = False
    if "last_toast" not in st.session_state:
        st.session_state["last_toast"] = None
    if "login_notified" not in st.session_state:
        st.session_state["login_notified"] = False
    
    # Agregar notificaciones de prueba si no hay ninguna
    if not st.session_state["notifications"]:
        st.session_state["notifications"] = [
            {"message": "Bienvenido al sistema", "level": "success", "read": False},
            {"message": "Programa configurado correctamente", "level": "info", "read": False},
            {"message": "Nueva actualización disponible", "level": "warning", "read": False}
        ]
        st.session_state["unread_count"] = 3


def push_notification(message: str, level: str = "info"):
    """Agrega una nueva notificación al sistema"""
    st.session_state["notifications"].append({"message": message, "level": level, "read": False})
    st.session_state["unread_count"] = (st.session_state.get("unread_count") or 0) + 1


def render_notifications_panel():
    """Renderiza el panel de notificaciones en el sidebar"""
    # Mostrar notificaciones en todas las vistas autenticadas (incluyendo program_config)
    current_view = st.session_state.get("view", "")
    views_with_notifications = ["program_selection", "program_config", "homepage", "tracking", "dashboard", "retrieval", "search"]
    
    if ((st.session_state.get("jwt") or st.session_state.get("session_id")) and 
        st.session_state.get("show_notifications") and 
        current_view in views_with_notifications):
        notifs = st.session_state.get("notifications", [])
        with st.sidebar:
            st.markdown("### 🔔 Notificaciones")
            # Cambiar texto del botón según si hay navegación disponible
            if current_view in ["homepage", "tracking", "dashboard", "retrieval", "search"]:
                button_text = "← Volver a Navegación"
            else:
                button_text = "← Cerrar Notificaciones"
            
            if st.button(button_text, key="sidebar_back_to_nav"):
                st.session_state["show_notifications"] = False
                st.rerun()
            st.divider()
            if not notifs:
                st.info("Sin notificaciones")
            else:
                for n in reversed(notifs[-10:]):
                    level = (n.get("level") or "info").lower()
                    msg = n.get("message") or ""
                    if level == "success":
                        st.success(msg)
                    elif level == "error":
                        st.error(msg)
                    elif level == "warning":
                        st.warning(msg)
                    else:
                        st.info(msg)


def render_toast():
    """Renderiza el toast flotante"""
    if st.session_state.get("show_toast") and st.session_state.get("last_toast"):
        t = st.session_state["last_toast"]
        lvl = t.get("level", "info")
        msg = t.get("message", "")
        st.markdown(f"<div class='toast {lvl}'>{msg}</div>", unsafe_allow_html=True)
        # Hide on next rerun
        st.session_state["show_toast"] = False
