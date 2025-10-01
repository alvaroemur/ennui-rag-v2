"""
Pantalla de login de la aplicación
"""
import streamlit as st
import requests
from config import API_BASE_URL_INTERNAL, LOGIN_URL, SIGNUP_URL
from notifications import push_notification


def render_login_screen():
    """Renderiza la pantalla de login"""
    # Intentar cargar usuarios recientes (requiere auth; si falla, mostrar aviso)
    recent_users_html = "<p style='color:#6c757d;'>Inicia sesión para ver usuarios recientes.</p>"
    try:
        r = requests.get(f"{API_BASE_URL_INTERNAL}/api/public/recent-users")
        if r.status_code == 200:
            users = r.json()[:5]
            if users:
                items = "".join([
                    f"<li><a href=\"{LOGIN_URL}\" target=\"_self\">{u['name']} &lt;{u['email']}&gt;</a></li>"
                    for u in users
                ])
                recent_users_html = f"<ul>{items}</ul>"
    except Exception:
        pass

    st.markdown(
        f"""
        <div class="center-wrapper">
          <div class="login-card">
            <h1>ennui-rag 2.0</h1>
            <div class="login-actions">
              <a class="btn" target="_self" href="{LOGIN_URL}">Log In</a>
              <a class="btn outline" target="_self" href="{SIGNUP_URL}">Sign Up</a>
            </div>
            <div class="recent-users">
              <h3>Usuarios recientes</h3>
              {recent_users_html}
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def handle_login_redirect():
    """Maneja la redirección después del login"""
    query_params = st.query_params
    access_token = query_params.get("access_token", [None]) if "access_token" in query_params else None
    refresh_token = query_params.get("refresh_token", [None]) if "refresh_token" in query_params else None
    name = query_params.get("name", [None]) if "name" in query_params else None

    if "state" in query_params and query_params["state"] == "signup":
        st.info(f"No account found for {query_params['email']}. Please sign up.")
        del query_params["state"]

    if access_token and refresh_token:
        st.session_state["jwt"] = access_token
        st.session_state["refresh_token"] = refresh_token
        st.session_state["name"] = name
        # Push notification and show toast instead of green box (only once)
        if not st.session_state.get("login_notified"):
            push_notification("Successfully logged in!", "success")
            st.session_state["show_toast"] = True
            st.session_state["last_toast"] = {"message": "Successfully logged in!", "level": "success"}
            st.session_state["login_notified"] = True
