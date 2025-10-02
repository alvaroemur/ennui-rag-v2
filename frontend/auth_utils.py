"""
Utilidades de autenticación para manejar tokens JWT y sesiones
"""
import requests
import streamlit as st
from config import API_BASE_URL_INTERNAL


def validate_session():
    """Valida una sesión del servidor y actualiza los tokens si es válida"""
    if not st.session_state.get("session_id"):
        return False

    try:
        payload = {
            "session_id": st.session_state["session_id"]
        }
        response = requests.post(
            f"{API_BASE_URL_INTERNAL}/auth/validate-session",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("valid"):
                # Actualizar tokens en session state
                st.session_state["jwt"] = data.get("access_token")
                return True
            else:
                # Sesión inválida, limpiar
                st.session_state["session_id"] = None
                st.session_state["jwt"] = None
                st.session_state["name"] = None
                return False
        else:
            # Error de servidor, no limpiar sesión inmediatamente
            print(f"Session validation failed with status {response.status_code}")
            return False
    except Exception as e:
        # En caso de error de conexión, no limpiar sesión inmediatamente
        # Solo limpiar si es un error específico de autenticación
        print(f"Session validation error: {e}")
        return False
    
    return False


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


def logout():
    """Cierra la sesión del usuario"""
    if st.session_state.get("session_id"):
        try:
            payload = {
                "session_id": st.session_state["session_id"]
            }
            requests.post(
                f"{API_BASE_URL_INTERNAL}/auth/logout",
                json=payload,
                timeout=10
            )
        except Exception:
            pass
    
    # Limpiar session state
    st.session_state["session_id"] = None
    st.session_state["jwt"] = None
    st.session_state["refresh_token"] = None
    st.session_state["name"] = None
    st.rerun()


def make_authenticated_request(method, url, **kwargs):
    """Hace una petición autenticada y maneja la renovación automática de tokens"""
    headers = kwargs.get("headers", {})
    
    # Para session-based auth, validar sesión primero si no tenemos JWT
    if st.session_state.get("session_id") and not st.session_state.get("jwt"):
        if not validate_session():
            # Sesión inválida, redirigir a login
            st.session_state["session_id"] = None
            st.session_state["jwt"] = None
            st.session_state["name"] = None
            st.rerun()
    
    # Usar JWT token para autenticación
    if st.session_state.get("jwt"):
        headers["Authorization"] = f"Bearer {st.session_state['jwt']}"
        kwargs["headers"] = headers
    
    try:
        response = requests.request(method, url, **kwargs)
        
        # Si el token expiró (401), intentar refrescar
        if response.status_code == 401:
            if st.session_state.get("session_id"):
                # Para session-based auth, validar sesión
                if validate_session():
                    # Reintentar la petición con el nuevo token
                    headers["Authorization"] = f"Bearer {st.session_state['jwt']}"
                    kwargs["headers"] = headers
                    response = requests.request(method, url, **kwargs)
                else:
                    # Sesión inválida, limpiar
                    logout()
            elif st.session_state.get("refresh_token"):
                # Para token-based auth, intentar refresh
                if refresh_jwt_token():
                    # Reintentar la petición con el nuevo token
                    headers["Authorization"] = f"Bearer {st.session_state['jwt']}"
                    kwargs["headers"] = headers
                    response = requests.request(method, url, **kwargs)
                else:
                    # No se puede refrescar, limpiar la sesión
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

