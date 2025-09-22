import streamlit as st
import requests
from dotenv import load_dotenv
import os
import datetime
from typing import Optional, List

st.set_page_config(layout="wide", page_title="ennui-rag 2.0")
load_dotenv()

API_BASE_URL = os.getenv("BACKEND_URL")
API_BASE_URL_INTERNAL = os.getenv("BACKEND_URL_INTERNAL")
FRONTEND_URL = os.getenv("FRONTEND_URL")

LOGIN_URL = API_BASE_URL + "/auth/login"
SIGNUP_URL = API_BASE_URL + "/auth/signup"

# LOGIN_URL = os.getenv("LOGIN_URL")
# SIGNUP_URL = os.getenv("SIGNUP_URL")


# Custom CSS for the navigation bar and buttons
st.markdown("""
    <style>
    /* Full-width app container */
    .block-container {max-width: 100% !important; padding-left: 2rem; padding-right: 2rem;}
    .top-bar {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        background-color: #0d1117;
        padding: 10px;
        border-radius: 10px;
    }
    .top-bar > button {
        margin-left: 10px;
    }
    .content-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    .center-wrapper {
        min-height: 70vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .login-card {
        max-width: 520px;
        width: 100%;
        padding: 32px;
        border-radius: 12px;
        background: transparent;
        border: 1px solid rgba(0,0,0,0.15);
        box-shadow: none;
        text-align: center;
    }
    .login-card h1 {
        margin: 0 0 16px 0;
        font-size: 28px;
    }
    .login-actions { margin-top: 8px; }
    .login-actions .btn {
        display: inline-block;
        margin: 8px;
        padding: 10px 16px;
        border-radius: 8px;
        background: #0d6efd;
        color: #fff;
        text-decoration: none;
        font-weight: 600;
    }
    .login-actions .btn.outline {
        background: #ffffff;
        color: #0d6efd;
        border: 2px solid #0d6efd;
    }
    .recent-users { text-align: left; margin-top: 20px; }
    .recent-users h3 { margin: 0 0 8px 0; font-size: 16px; }
    .recent-users ul { padding-left: 20px; margin: 0; }
    .recent-users li { margin: 4px 0; }

    /* Toast styles */
    .toast { position: fixed; right: 24px; top: 72px; z-index: 9999; padding: 12px 16px; border-radius: 8px; color: #fff; box-shadow: 0 4px 16px rgba(0,0,0,0.15); animation: fadeOut 3s ease 0s 1 forwards; }
    .toast.success { background: #198754; }
    .toast.error { background: #dc3545; }
    .toast.warning { background: #ffc107; color: #111; }
    .toast.info { background: #0dcaf0; color: #111; }
    @keyframes fadeOut { 0% { opacity: 1; } 80% { opacity: 1; } 100% { opacity: 0; visibility: hidden; } }
    /* Floating notifications panel */
    .notif-panel { position: fixed; right: 24px; top: 72px; z-index: 9998; width: 360px; max-height: 60vh; overflow: auto; background: #ffffff; color: #111; border: 1px solid rgba(0,0,0,0.1); border-radius: 10px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); padding: 12px; }
    .notif-panel h4 { margin: 0 0 8px 0; font-size: 16px; }
    .notif-item { padding: 8px 10px; border-radius: 8px; margin: 6px 0; border-left: 4px solid #ddd; background: #f8f9fa; }
    .notif-item.success { border-left-color: #198754; }
    .notif-item.error { border-left-color: #dc3545; }
    .notif-item.warning { border-left-color: #ffc107; }
    .notif-item.info { border-left-color: #0dcaf0; }
    </style>
    """, unsafe_allow_html=True)

# Store tokens in session state
if "jwt" not in st.session_state:
    st.session_state["jwt"] = None
if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None
if "notifications" not in st.session_state:
    st.session_state["notifications"] = []  # list of {message, level, read}
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

def push_notification(message: str, level: str = "info"):
    st.session_state["notifications"].append({"message": message, "level": level, "read": False})
    st.session_state["unread_count"] = (st.session_state.get("unread_count") or 0) + 1

# Display the navigation bar
def render_navbar(title: str, breadcrumbs: Optional[List[str]] = None):
    with st.container():
        left, right = st.columns([3, 2])
        with left:
            if breadcrumbs and len(breadcrumbs) > 0:
                if len(breadcrumbs) > 1:
                    upper = " / ".join(breadcrumbs[:-1])
                    lower = breadcrumbs[-1]
                    st.caption(upper)
                    st.markdown(f"### {lower}")
                else:
                    st.caption("")
                    st.markdown(f"### {breadcrumbs[0]}")
            else:
                st.caption("")
                st.markdown(f"### {title}")
        with right:
            if st.session_state.get("jwt"):
                # Fetch email once if not set
                if not st.session_state.get("user_email"):
                    try:
                        r = requests.get(f"{API_BASE_URL_INTERNAL}/api/users/me", headers={"Authorization": f"Bearer {st.session_state['jwt']}"}, timeout=10)
                        if r.status_code == 200:
                            me = r.json()
                            st.session_state["user_email"] = me.get("email")
                            st.session_state["name"] = me.get("name") or st.session_state.get("name")
                    except Exception:
                        pass
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    st.caption(st.session_state.get("user_email") or st.session_state.get("name") or "Usuario")
                with cols[1]:
                    notif_count = st.session_state.get("unread_count", 0)
                    bell = f"🔔 {notif_count}" if notif_count else "🔔"
                    if st.button(bell, key="navbar_notifications"):
                        st.session_state["show_notifications"] = not st.session_state.get("show_notifications", False)
                        if st.session_state["show_notifications"]:
                            # mark all as read and reset counter
                            for n in st.session_state["notifications"]:
                                n["read"] = True
                            st.session_state["unread_count"] = 0
                with cols[2]:
                    if st.button("Log Out", key="navbar_logout"):
                        st.session_state["jwt"] = None
                        st.session_state["refresh_token"] = None
                        st.session_state["user_email"] = None
                        st.session_state["name"] = None
                        push_notification("Logged out successfully.", "success")
                        st.markdown(f'<meta http-equiv="refresh" content="0;url={FRONTEND_URL}">', unsafe_allow_html=True)
            else:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Log In", key="navbar_login"):
                        st.markdown(f'<meta http-equiv="refresh" content="0;url={LOGIN_URL}">', unsafe_allow_html=True)
                with c2:
                    if st.button("Sign Up", key="navbar_signup"):
                        st.markdown(f'<meta http-equiv="refresh" content="0;url={SIGNUP_URL}">', unsafe_allow_html=True)

    # Notifications dropdown/panel (floating HTML) under navbar
    if st.session_state.get("jwt") and st.session_state.get("show_notifications"):
        notifs = st.session_state.get("notifications", [])
        if not notifs:
            panel_html = "<div class='notif-panel'><h4>Notificaciones</h4><div class='notif-item info'>Sin notificaciones</div></div>"
        else:
            items_html = []
            for n in reversed(notifs[-10:]):
                level = (n.get("level") or "info").lower()
                msg = n.get("message") or ""
                items_html.append(f"<div class='notif-item {level}'>{msg}</div>")
            panel_html = "<div class='notif-panel'><h4>Notificaciones</h4>" + "".join(items_html) + "</div>"
        st.markdown(panel_html, unsafe_allow_html=True)

# Check if user is logged in
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
    # No limpiamos los query params para preservar la sesión tras recargar
else:
    pass

    
if not ("jwt" in st.session_state and st.session_state["jwt"] is not None):
    # Pantalla de login minimalista centrada
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



nav_title = "ennui-rag 2.0"
if st.session_state.get("jwt"):
    if "view" in st.session_state and st.session_state["view"] == "create_program":
        render_navbar(nav_title, ["Programas", "Crear programa"])
    else:
        render_navbar(nav_title, ["Programas"])

    # Floating toast (auto-hides next rerun)
    if st.session_state.get("show_toast") and st.session_state.get("last_toast"):
        t = st.session_state["last_toast"]
        lvl = t.get("level", "info")
        msg = t.get("message", "")
        st.markdown(f"<div class='toast {lvl}'>{msg}</div>", unsafe_allow_html=True)
        # Hide on next rerun
        st.session_state["show_toast"] = False

# Vista principal: seleccionar o crear un programa (solo si autenticado)
if st.session_state["jwt"] is not None:
    # Ruta/pantalla actual dentro del área autenticada
    if "view" not in st.session_state:
        st.session_state["view"] = "home"  # home | create_program

    headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}

    # Pantalla: Crear programa (pantalla completa)
    if st.session_state["view"] == "create_program":
        folder_q = st.session_state.get("checked_folder")
        folder_name = st.session_state.get("checked_folder_name")
        if folder_q:
            st.caption(f"Carpeta de Drive: {folder_name or ''} ({folder_q})")

        with st.form("finalize_create_form_full"):
            internal_code = st.text_input("Código interno", max_chars=100)
            name = st.text_input("Nombre del programa", max_chars=200)
            main_client = st.text_input("Cliente principal", value="")
            main_beneficiaries = st.text_input("Beneficiarios principales", value="")
            start_date = st.date_input("Fecha de inicio", value=None)
            end_date = st.date_input("Fecha de fin", value=None)
            do_create = st.form_submit_button("Crear")
            if do_create:
                if not internal_code or not name:
                    st.warning("Completa los campos obligatorios: código y nombre.")
                else:
                    payload = {
                        "folder_link_or_id": folder_q,
                        "internal_code": internal_code,
                        "name": name,
                        "main_client": main_client or None,
                        "main_beneficiaries": main_beneficiaries or None,
                        "start_date": datetime.datetime.combine(start_date, datetime.time()).isoformat() if start_date else None,
                        "end_date": datetime.datetime.combine(end_date, datetime.time()).isoformat() if end_date else None,
                    }
                    try:
                        r = requests.post(f"{API_BASE_URL_INTERNAL}/api/programs/", headers=headers, json=payload, timeout=15)
                        if r.status_code == 200:
                            st.success("Programa creado correctamente.")
                            # Reset state y volver a home
                            st.session_state["view"] = "home"
                            st.session_state["create_step"] = "idle"
                            st.session_state["checked_folder"] = None
                            st.session_state["checked_folder_name"] = None
                            st.rerun()
                        elif r.status_code == 409:
                            st.info("Se detectó un programa recién creado para esta carpeta.")
                            st.session_state["view"] = "home"
                            st.session_state["create_step"] = "exists"
                        else:
                            try:
                                detail = r.json().get("detail")
                            except Exception:
                                detail = None
                            st.error(detail or "No se pudo crear el programa.")
                    except Exception:
                        st.error("Error de conexión al crear el programa.")

        if st.button("Cancelar", key="cancel_full_create"):
            st.session_state["view"] = "home"
            st.session_state["create_step"] = "idle"
            st.session_state["checked_folder"] = None
            st.session_state["checked_folder_name"] = None
            st.rerun()

        st.stop()

    # Pantalla principal autenticada

    # Tres columnas: Mis programas | Otros programas | Crear programa
    col1, col2, col3 = st.columns(3)

    # Sección: Mis programas
    with col1:
        st.subheader("Mis programas")
        try:
            resp = requests.get(f"{API_BASE_URL_INTERNAL}/api/programs/mine", headers=headers, timeout=10)
            if resp.status_code == 200:
                programs = resp.json()
                if programs:
                    with st.container(border=True):
                        labels = [
                            f"{p.get('name') or 'Sin nombre'} — {p.get('internal_code') or '-'} (ID {p['id']})"
                            for p in programs
                        ]
                        idx = st.selectbox("Selecciona un programa", range(len(labels)), format_func=lambda i: labels[i])
                        st.button("Abrir programa", help="Acción futura: navegar al detalle del programa")
                else:
                    st.info("No tienes programas aún.")
            else:
                st.error("No se pudieron cargar tus programas.")
        except Exception as e:
            st.error("Error de conexión al cargar programas.")

    # Sección: Otros programas (sin acceso ni solicitud)
    with col2:
        st.subheader("Otros programas existentes")
        try:
            r = requests.get(f"{API_BASE_URL_INTERNAL}/api/programs/others", headers=headers, timeout=15)
            if r.status_code == 200:
                others = r.json()
                if not others:
                    st.info("No hay otros programas disponibles.")
                else:
                    for p in others:
                        cols = st.columns([3, 1])
                        with cols[0]:
                            st.write(f"{p.get('name') or 'Sin nombre'} — {p.get('internal_code') or '-'} (ID {p['id']})")
                            st.caption(f"Drive: {p.get('drive_folder_name') or '-'} ({p.get('drive_folder_id')})")
                        with cols[1]:
                            if st.button("Solicitar acceso", key=f"req_{p['id']}"):
                                try:
                                    pr = requests.post(
                                        f"{API_BASE_URL_INTERNAL}/api/programs/request-access",
                                        headers=headers,
                                        json={"program_id": p["id"]},
                                        timeout=15,
                                    )
                                    if pr.status_code == 200:
                                        st.success("Solicitud enviada.")
                                        st.rerun()
                                    else:
                                        # Mostrar detalle si viene
                                        try:
                                            detail = pr.json().get("detail")
                                        except Exception:
                                            detail = None
                                        st.warning(detail or "No se pudo enviar la solicitud.")
                                except Exception:
                                    st.error("Error de conexión al solicitar acceso.")
            else:
                st.error("No se pudieron cargar otros programas.")
        except Exception:
            st.error("Error de conexión al cargar otros programas.")

    # Sección: Crear programa (paso 1 -> verificar carpeta; paso 2 -> completar campos)
    with col3:
        st.subheader("Crear programa")
        if "create_step" not in st.session_state:
            st.session_state["create_step"] = "idle"  # idle | exists | new
            st.session_state["checked_folder"] = None

        if st.session_state["create_step"] == "idle":
            with st.form("check_folder_form"):
                folder_q = st.text_input("Link o ID de carpeta de Drive", help="Se verificará acceso a la carpeta y si ya existe un programa para ella")
                do_check = st.form_submit_button("Verificar")
                if do_check:
                    if not folder_q:
                        st.warning("Ingresa un link o ID de carpeta.")
                    else:
                        try:
                            chk = requests.get(f"{API_BASE_URL_INTERNAL}/api/programs/check-drive", headers=headers, params={"q": folder_q}, timeout=20)
                            if chk.status_code == 200:
                                data = chk.json()
                                if not data.get("ok"):
                                    st.error("No se puede acceder a la carpeta de Drive o no es una carpeta.")
                                else:
                                    st.session_state["checked_folder"] = folder_q
                                    st.session_state["checked_folder_name"] = data.get("folder_name")
                                    if data.get("exists_program"):
                                        st.session_state["create_step"] = "exists"
                                    else:
                                        # Verificación correcta y no existe programa: ir a pantalla de creación
                                        st.session_state["view"] = "create_program"
                                        st.rerun()
                            else:
                                try:
                                    detail = chk.json().get("detail")
                                except Exception:
                                    detail = None
                                st.error(detail or "No se pudo verificar la carpeta.")
                        except Exception:
                            st.error("Error de conexión al verificar.")

        if st.session_state["create_step"] == "exists":
            st.info("Ya existe un programa para esta carpeta.")
            st.caption(f"Carpeta: {st.session_state.get('checked_folder_name') or ''} ({st.session_state['checked_folder']})")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Solicitar acceso", key="req_access_existing_folder"):
                    try:
                        rr = requests.post(
                            f"{API_BASE_URL_INTERNAL}/api/programs/request-access",
                            headers=headers,
                            json={"folder_link_or_id": st.session_state["checked_folder"]},
                            timeout=15,
                        )
                        if rr.status_code == 200:
                            st.success("Solicitud enviada.")
                            st.session_state["create_step"] = "idle"
                            st.session_state["checked_folder"] = None
                        else:
                            try:
                                detail = rr.json().get("detail")
                            except Exception:
                                detail = None
                            st.warning(detail or "No se pudo enviar la solicitud.")
                    except Exception:
                        st.error("Error de conexión al solicitar acceso.")
            with c2:
                if st.button("Cancelar", key="cancel_exists"):
                    st.session_state["create_step"] = "idle"
                    st.session_state["checked_folder"] = None

        if st.session_state["create_step"] == "new":
            st.success("Acceso a Drive verificado. No existe programa para esta carpeta.")
            st.caption(f"Carpeta: {st.session_state.get('checked_folder_name') or ''} ({st.session_state.get('checked_folder')})")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Continuar", key="continue_to_full_create"):
                    st.session_state["view"] = "create_program"
                    st.rerun()
            with c2:
                if st.button("Cancelar", key="cancel_new"):
                    st.session_state["create_step"] = "idle"
                    st.session_state["checked_folder"] = None
                    st.session_state["checked_folder_name"] = None

    st.divider()

    # Sección: Gestionar solicitudes (si eres propietario)
    st.subheader("Solicitudes recibidas (soy propietario)")
    try:
        r = requests.get(f"{API_BASE_URL_INTERNAL}/api/programs/requests", headers=headers, timeout=15)
        if r.status_code == 200:
            reqs = r.json()
            if not reqs:
                st.info("No hay solicitudes pendientes.")
            else:
                for pr in reqs:
                    with st.container(border=True):
                        st.write(f"Solicitud #{pr['id']} — Programa {pr['program_id']}")
                        st.write(f"Estado: {pr['status']}")
                        if pr.get('message'):
                            st.write(f"Mensaje: {pr['message']}")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("Aprobar", key=f"approve_{pr['id']}"):
                                try:
                                    ar = requests.post(f"{API_BASE_URL_INTERNAL}/api/programs/requests/{pr['id']}/approve", headers=headers, timeout=15)
                                    if ar.status_code == 200:
                                        st.success("Solicitud aprobada.")
                                        st.rerun()
                                    else:
                                        st.error("No se pudo aprobar la solicitud.")
                                except Exception:
                                    st.error("Error de conexión al aprobar.")
                        with c2:
                            if st.button("Rechazar", key=f"reject_{pr['id']}"):
                                try:
                                    rr = requests.post(f"{API_BASE_URL_INTERNAL}/api/programs/requests/{pr['id']}/reject", headers=headers, timeout=15)
                                    if rr.status_code == 200:
                                        st.success("Solicitud rechazada.")
                                        st.rerun()
                                    else:
                                        st.error("No se pudo rechazar la solicitud.")
                                except Exception:
                                    st.error("Error de conexión al rechazar.")
        else:
            st.error("No se pudieron cargar las solicitudes.")
    except Exception:
        st.error("Error de conexión al cargar solicitudes.")


# # Button to call unprotected API
# if st.button("Call Unprotected API"):
#     response = requests.get(f"{API_BASE_URL}/api/")
#     st.write("Response:", response.json())

# # Button to call protected API without JWT
# if st.button("Call Protected API without JWT"):
#     response = requests.get(f"{API_BASE_URL}/api/protected")
#     st.write("Response:", response.json())

# # Button to call protected API with JWT
# if st.button("Call Protected API with JWT"):
#     headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}
#     print(headers)
#     response = requests.get(f"{API_BASE_URL}/api/protected", headers=headers)
#     st.write("Response:", response.json())

# add a button to show all users
# if st.button("Show all users"):
#     headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}
#     response = requests.get(f"{API_BASE_URL}/api/users", headers=headers)
#     st.write("Response:", response.json())
