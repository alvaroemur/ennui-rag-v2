"""
Utilidades de autenticación para manejar tokens JWT
"""
import requests
import streamlit as st
from config import API_BASE_URL_INTERNAL


def refresh_jwt_token():
    """Intenta refrescar el token JWT usando el refresh token"""
    if not st.session_state.get("refresh_token"):
        return False
    
    try:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": st.session_state["refresh_token"]
        }
        response = requests.post(
            f"{API_BASE_URL_INTERNAL}/auth/refresh",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("result") and data.get("access_token"):
                st.session_state["jwt"] = data["access_token"]
                return True
    except Exception:
        pass
    
    return False


def make_authenticated_request(method, url, **kwargs):
    """Hace una petición autenticada y maneja la renovación automática de tokens"""
    headers = kwargs.get("headers", {})
    headers["Authorization"] = f"Bearer {st.session_state['jwt']}"
    kwargs["headers"] = headers
    
    try:
        response = requests.request(method, url, **kwargs)
        
        # Si el token expiró (401), intentar refrescar
        if response.status_code == 401:
            if refresh_jwt_token():
                # Reintentar la petición con el nuevo token
                headers["Authorization"] = f"Bearer {st.session_state['jwt']}"
                kwargs["headers"] = headers
                response = requests.request(method, url, **kwargs)
            else:
                # Si no se puede refrescar, limpiar la sesión
                st.session_state["jwt"] = None
                st.session_state["refresh_token"] = None
                st.session_state["name"] = None
                st.rerun()
        
        return response
    except Exception as e:
        # En caso de error de conexión, devolver una respuesta mock con error
        class MockResponse:
            def __init__(self):
                self.status_code = 500
                self.text = "Connection error"
            
            def json(self):
                return {"detail": "Connection error"}
        
        return MockResponse()

