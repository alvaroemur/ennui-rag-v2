"""
Configuración y constantes de la aplicación
"""
import os
from dotenv import load_dotenv

load_dotenv()

# URLs de la API
API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:7000")
API_BASE_URL_INTERNAL = os.getenv("BACKEND_URL_INTERNAL", "http://backend:7000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")

# URLs de autenticación
LOGIN_URL = API_BASE_URL + "/auth/login"
SIGNUP_URL = API_BASE_URL + "/auth/signup"

# CSS personalizado para la aplicación
CUSTOM_CSS = """
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
    .notif-panel .notif-close { position: absolute; right: 8px; top: 8px; text-decoration: none; color: #6c757d; font-weight: 700; font-size: 16px; padding: 2px 6px; border-radius: 6px; }
    .notif-panel .notif-close:hover { background: rgba(0,0,0,0.05); color: #000; }
    .notif-item { padding: 8px 10px; border-radius: 8px; margin: 6px 0; border-left: 4px solid #ddd; background: #f8f9fa; }
    .notif-item.success { border-left-color: #198754; }
    .notif-item.error { border-left-color: #dc3545; }
    .notif-item.warning { border-left-color: #ffc107; }
    .notif-item.info { border-left-color: #0dcaf0; }
    /* Navbar user display */
    .nav-user { text-align: right; font-weight: 600; font-size: 16px; color: inherit; margin-top: 6px; }
    </style>
    """
