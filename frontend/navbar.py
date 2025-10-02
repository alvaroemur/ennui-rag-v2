"""
Barra de navegación de la aplicación
"""
import streamlit as st
import requests
from typing import Optional, List
from config import API_BASE_URL_INTERNAL, LOGIN_URL, SIGNUP_URL, FRONTEND_URL
from notifications import push_notification


def render_navbar(title: str, breadcrumbs: Optional[List[str]] = None):
    """Renderiza la barra de navegación superior"""
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
            # Check if user is authenticated (session-based or token-based)
            is_authenticated = st.session_state.get("jwt") or st.session_state.get("session_id")
            
            if is_authenticated:
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
                cols = st.columns([4, 1, 1])
                with cols[0]:
                    st.markdown(
                        f"<div class='nav-user'>{st.session_state.get('user_email') or st.session_state.get('name') or 'Usuario'}</div>",
                        unsafe_allow_html=True,
                    )
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
                        from auth_utils import logout
                        logout()
            else:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Log In", key="navbar_login"):
                        st.markdown(f'<meta http-equiv="refresh" content="0;url={LOGIN_URL}">', unsafe_allow_html=True)
                with c2:
                    if st.button("Sign Up", key="navbar_signup"):
                        st.markdown(f'<meta http-equiv="refresh" content="0;url={SIGNUP_URL}">', unsafe_allow_html=True)
