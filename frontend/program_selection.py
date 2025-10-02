"""
Pantalla principal del dashboard autenticado
"""
import streamlit as st
import requests
from config import API_BASE_URL_INTERNAL
from auth_utils import make_authenticated_request


def render_program_selection():
    """Renderiza la pantalla de selección de programas"""
    # Tres columnas: Mis programas | Otros programas | Crear programa
    col1, col2, col3 = st.columns(3)

    # Sección: Mis programas
    with col1:
        render_my_programs_section()

    # Sección: Otros programas
    with col2:
        render_other_programs_section()

    # Sección: Crear programa
    with col3:
        render_create_program_section()

    st.divider()

    # Sección: Gestionar solicitudes
    render_requests_section()


def render_my_programs_section():
    """Renderiza la sección de mis programas"""
    st.subheader("Mis programas")
    try:
        resp = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/api/programs/mine", timeout=10)
        if resp.status_code == 200:
            programs = resp.json()
            if programs:
                with st.container(border=True):
                    labels = [
                        f"{p.get('name') or 'Sin nombre'} — {p.get('internal_code') or '-'} (ID {p['id']})"
                        for p in programs
                    ]
                    idx = st.selectbox("Selecciona un programa", range(len(labels)), format_func=lambda i: labels[i])
                    if st.button("Abrir programa", help="Abrir homepage del programa"):
                        st.session_state["selected_program_id"] = programs[idx]["id"]
                        st.session_state["view"] = "homepage"
                        st.rerun()
            else:
                st.info("No tienes programas aún.")
        else:
            st.error("No se pudieron cargar tus programas.")
    except Exception as e:
        st.error("Error de conexión al cargar programas.")


def render_other_programs_section():
    """Renderiza la sección de otros programas"""
    st.subheader("Otros programas existentes")
    try:
        r = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/api/programs/others", timeout=15)
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
                                pr = make_authenticated_request(
                                    "POST",
                                    f"{API_BASE_URL_INTERNAL}/api/programs/request-access",
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


def render_create_program_section():
    """Renderiza la sección de crear programa"""
    st.subheader("Crear programa")
    if "create_step" not in st.session_state:
        st.session_state["create_step"] = "idle"  # idle | exists | new
        st.session_state["checked_folder"] = None

    if st.session_state["create_step"] == "idle":
        render_folder_check_form()
    elif st.session_state["create_step"] == "exists":
        render_existing_program_message()
    elif st.session_state["create_step"] == "new":
        render_new_program_message()


def render_folder_check_form():
    """Renderiza el formulario de verificación de carpeta"""
    with st.form("check_folder_form"):
        folder_q = st.text_input("Link o ID de carpeta de Drive", help="Se verificará acceso a la carpeta y si ya existe un programa para ella")
        do_check = st.form_submit_button("Verificar")
        if do_check:
            if not folder_q:
                st.warning("Ingresa un link o ID de carpeta.")
            else:
                try:
                    chk = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/api/programs/check-drive", params={"q": folder_q}, timeout=20)
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


def render_existing_program_message():
    """Renderiza el mensaje cuando ya existe un programa para la carpeta"""
    st.info("Ya existe un programa para esta carpeta.")
    st.caption(f"Carpeta: {st.session_state.get('checked_folder_name') or ''} ({st.session_state['checked_folder']})")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Solicitar acceso", key="req_access_existing_folder"):
            try:
                rr = make_authenticated_request(
                    "POST",
                    f"{API_BASE_URL_INTERNAL}/api/programs/request-access",
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


def render_new_program_message():
    """Renderiza el mensaje cuando se puede crear un nuevo programa"""
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


def render_requests_section():
    """Renderiza la sección de gestión de solicitudes"""
    st.subheader("Solicitudes recibidas (soy propietario)")
    try:
        r = make_authenticated_request("GET", f"{API_BASE_URL_INTERNAL}/api/programs/requests", timeout=15)
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
                                    ar = make_authenticated_request("POST", f"{API_BASE_URL_INTERNAL}/api/programs/requests/{pr['id']}/approve", timeout=15)
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
                                    rr = make_authenticated_request("POST", f"{API_BASE_URL_INTERNAL}/api/programs/requests/{pr['id']}/reject", timeout=15)
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
