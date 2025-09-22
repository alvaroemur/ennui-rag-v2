import streamlit as st
import requests
from dotenv import load_dotenv
import os

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
    </style>
    """, unsafe_allow_html=True)

# Store tokens in session state
if "jwt" not in st.session_state:
    st.session_state["jwt"] = None
if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None

# Display the navigation bar
st.markdown('<div class="navbar">', unsafe_allow_html=True)

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
    st.success("Successfully logged in!")
    # st.query_params  # Clear URL parameters
else:
    st.info("Please sign up or log in.")

# Display login/signup buttons if not logged in; otherwise, display logout
if "jwt" in st.session_state and st.session_state["jwt"] is not None:
    st.write(f"Welcome, {st.session_state['name']}!")
    logout_clicked = st.button("Logout")
    if logout_clicked:
        # Clear session state tokens
        st.session_state["jwt"] = None
        st.session_state["refresh_token"] = None
        access_token = None
        refresh_token = None
        st.success("Logged out successfully.")
        # Redirect to the login/signup page
        st.markdown(f'<meta http-equiv="refresh" content="0;url={FRONTEND_URL}">', unsafe_allow_html=True)

    
else:
    login_clicked = st.button("Log In")
    signup_clicked = st.button("Sign Up")

    if login_clicked:
        # Redirect user to the login page
        print(f'Redirecting to: {LOGIN_URL}')
        st.markdown(f'<meta http-equiv="refresh" content="0;url={LOGIN_URL}">', unsafe_allow_html=True)


    if signup_clicked:
        # Redirect user to the signup page
        st.markdown(f'<meta http-equiv="refresh" content="0;url={SIGNUP_URL}">', unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.title("Programas")

# Vista principal: seleccionar o crear un programa
if st.session_state["jwt"] is not None:
    headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}

    # Cols para dos secciones lado a lado
    col1, col2 = st.columns(2)

    # Sección: Mis programas
    with col1:
        st.subheader("Mis programas")
        try:
            resp = requests.get(f"{API_BASE_URL_INTERNAL}/api/programs/mine", headers=headers, timeout=10)
            if resp.status_code == 200:
                programs = resp.json()
                if programs:
                    labels = [f"{p.get('name') or 'Sin nombre'} — {p.get('internal_code') or '-'} (ID {p['id']})" for p in programs]
                    idx = st.selectbox("Selecciona un programa", range(len(labels)), format_func=lambda i: labels[i])
                    selected = programs[idx]

                    st.write("Detalles:")
                    st.write(f"- ID: {selected['id']}")
                    st.write(f"- Nombre: {selected.get('name')}")
                    st.write(f"- Código interno: {selected.get('internal_code')}")
                    st.write(f"- Cliente principal: {selected.get('main_client')}")
                    st.write(f"- Beneficiarios: {selected.get('main_beneficiaries')}")
                    st.write(f"- Carpeta Drive: {selected.get('drive_folder_name')} ({selected.get('drive_folder_id')})")

                    st.button("Abrir programa", help="Acción futura: navegar al detalle del programa")
                else:
                    st.info("No tienes programas aún.")
            else:
                st.error("No se pudieron cargar tus programas.")
        except Exception as e:
            st.error("Error de conexión al cargar programas.")

    # Sección: Crear programa
    with col2:
        st.subheader("Crear programa")
        with st.form("crear_programa"):
            folder_link_or_id = st.text_input("Link o ID de carpeta de Drive", help="Pega el enlace o el ID de la carpeta del programa en Drive")
            internal_code = st.text_input("Código interno", max_chars=100)
            name = st.text_input("Nombre del programa", max_chars=200)
            main_client = st.text_input("Cliente principal", value="")
            main_beneficiaries = st.text_input("Beneficiarios principales", value="")
            start_date = st.date_input("Fecha de inicio", value=None)
            end_date = st.date_input("Fecha de fin", value=None)

            submitted = st.form_submit_button("Crear")
            if submitted:
                if not folder_link_or_id or not internal_code or not name:
                    st.warning("Completa los campos obligatorios: carpeta, código e identidad del programa.")
                else:
                    payload = {
                        "folder_link_or_id": folder_link_or_id,
                        "internal_code": internal_code,
                        "name": name,
                        "main_client": main_client or None,
                        "main_beneficiaries": main_beneficiaries or None,
                        "start_date": start_date.isoformat() if start_date else None,
                        "end_date": end_date.isoformat() if end_date else None,
                    }
                    try:
                        r = requests.post(f"{API_BASE_URL_INTERNAL}/api/programs/", headers=headers, json=payload, timeout=15)
                        if r.status_code == 200:
                            st.success("Programa creado correctamente.")
                            st.rerun()
                        elif r.status_code == 409:
                            # Ya existe programa para esa carpeta: ofrecer solicitar acceso
                            st.session_state["offer_request_access"] = True
                            st.session_state["last_folder_input"] = folder_link_or_id
                            st.info("Ya existe un programa con esa carpeta. Puedes solicitar acceso justo debajo.")
                        elif r.status_code == 400:
                            detail = r.json().get("detail", "Datos inválidos")
                            st.error(f"No se pudo crear: {detail}")
                        else:
                            st.error("Error inesperado al crear el programa.")
                    except Exception:
                        st.error("Error de conexión al crear el programa.")

        # Ofrecer solicitar acceso si detectamos conflicto por carpeta existente
        if st.session_state.get("offer_request_access"):
            with st.container():
                st.caption("Solicitar acceso al programa existente para esta carpeta de Drive")
                st.write(f"Carpeta: {st.session_state.get('last_folder_input')}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Solicitar acceso ahora", key="btn_req_access_folder"):
                        payload = {
                            "folder_link_or_id": st.session_state.get("last_folder_input"),
                            "message": None,
                        }
                        try:
                            rr = requests.post(f"{API_BASE_URL_INTERNAL}/api/programs/request-access", headers=headers, json=payload, timeout=15)
                            if rr.status_code == 200:
                                st.success("Solicitud de acceso enviada.")
                                st.session_state["offer_request_access"] = False
                                st.session_state["last_folder_input"] = None
                            else:
                                # Intentar mostrar detalle de error si viene
                                try:
                                    detail = rr.json().get("detail")
                                except Exception:
                                    detail = None
                                st.warning(detail or "No se pudo enviar la solicitud.")
                        except Exception:
                            st.error("Error de conexión al solicitar acceso.")
                with c2:
                    if st.button("Cancelar", key="btn_cancel_req_access_folder"):
                        st.session_state["offer_request_access"] = False
                        st.session_state["last_folder_input"] = None

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
