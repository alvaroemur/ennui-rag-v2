# Estructura del Frontend - ennui-rag 2.0

## Estructura Final (Plana)

```
frontend/
├── app.py                         # Archivo principal (punto de entrada)
├── run_app.py                    # Script para ejecutar la aplicación
├── requirements.txt               # Dependencias
├── Dockerfile                    # Configuración Docker
├── README.md                     # Documentación
├── config.py                     # Configuración y constantes
├── auth_utils.py                 # Utilidades de autenticación JWT
├── notifications.py              # Sistema de notificaciones
├── navbar.py                     # Barra de navegación
├── login_screen.py              # Pantalla de login
├── create_program_screen.py     # Pantalla de creación de programa
├── program_config.py            # Pantalla de configuración de programa
├── program_tracking.py          # Pantalla de seguimiento del programa
├── program_mel.py               # Dashboard del programa (MEL)
└── main_dashboard.py            # Dashboard principal autenticado
```

## Imports

Todos los imports son absolutos desde la raíz del directorio frontend:

```python
from config import CUSTOM_CSS
from auth_utils import make_authenticated_request, refresh_jwt_token
from notifications import initialize_notifications, render_notifications_panel, render_toast
from navbar import render_navbar
from login_screen import render_login_screen, handle_login_redirect
from create_program_screen import render_create_program_screen
from program_config import render_program_config_screen
from program_tracking import render_program_tracking
from program_mel import render_dashboard_screen
```

## Ejecución

### Desarrollo Local
```bash
cd frontend
streamlit run app.py
# o
python run_app.py
```

### Docker
```bash
cd frontend
docker build -t ennui-rag-frontend .
docker run -p 8501:8501 ennui-rag-frontend
```

## Notas

- Estructura plana para evitar problemas de imports en Docker
- Todos los archivos en la raíz del directorio frontend
- Imports absolutos simples
- Compatible con desarrollo local y Docker
