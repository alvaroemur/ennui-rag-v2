"""
Pantalla de creación de programa
"""
import streamlit as st
import requests
import datetime
from config import API_BASE_URL_INTERNAL
from auth_utils import make_authenticated_request


def render_create_program_screen():
    """Renderiza la pantalla de creación de programa"""
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
                    r = make_authenticated_request("POST", f"{API_BASE_URL_INTERNAL}/api/programs/", json=payload, timeout=15)
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
