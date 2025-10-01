# Frontend - ennui-rag 2.0

Frontend refactorizado de la aplicación ennui-rag 2.0 usando Streamlit.

## Estructura del Proyecto

```
frontend/
├── __init__.py                    # Paquete Python
├── app.py                         # Archivo principal (punto de entrada)
├── config.py                      # Configuración y constantes
├── notifications.py               # Sistema de notificaciones
├── navbar.py                      # Barra de navegación
├── login_screen.py               # Pantalla de login
├── create_program_screen.py      # Pantalla de creación de programa
├── program_config_screen.py      # Pantalla de configuración de programa
├── main_dashboard.py             # Dashboard principal autenticado
├── run_app.py                    # Script para ejecutar la aplicación
└── README.md                     # Este archivo
```

## Instalación

1. Instalar las dependencias:
```bash
pip install streamlit requests python-dotenv
```

2. Configurar las variables de entorno en un archivo `.env`:
```env
BACKEND_URL=http://localhost:8000
BACKEND_URL_INTERNAL=http://localhost:8000
FRONTEND_URL=http://localhost:8501
```

## Ejecución

### Opción 1: Usando el script de ejecución
```bash
cd frontend
python run_app.py
```

### Opción 2: Ejecutar directamente con Streamlit
```bash
cd frontend
streamlit run app.py
```

### Opción 3: Ejecutar con parámetros específicos
```bash
cd frontend
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## Arquitectura

La aplicación está refactorizada en módulos independientes:

- **`app.py`**: Orquestador principal que maneja el flujo de la aplicación
- **`config.py`**: Configuración centralizada (URLs, CSS, constantes)
- **`notifications.py`**: Sistema de notificaciones y toasts
- **`navbar.py`**: Barra de navegación superior
- **`login_screen.py`**: Pantalla de autenticación
- **`create_program_screen.py`**: Formulario de creación de programas
- **`program_config_screen.py`**: Configuración de programas con tabs
- **`main_dashboard.py`**: Dashboard principal con todas las secciones

## Características

- ✅ Arquitectura modular y mantenible
- ✅ Separación clara de responsabilidades
- ✅ Sistema de notificaciones integrado
- ✅ Navegación por breadcrumbs
- ✅ Pantallas especializadas para cada funcionalidad
- ✅ Manejo de estados de sesión
- ✅ Integración con API backend

## Desarrollo

Para agregar nuevas pantallas:

1. Crear un nuevo archivo `nueva_pantalla.py`
2. Implementar la función `render_nueva_pantalla()`
3. Importar en `app.py`
4. Agregar la lógica de navegación en el flujo principal

## Troubleshooting

### Error de imports relativos
Si encuentras el error `ImportError: attempted relative import with no known parent package`, asegúrate de ejecutar la aplicación desde el directorio `frontend/` y no como un módulo Python.

### Error de dependencias
Asegúrate de tener todas las dependencias instaladas:
```bash
pip install -r requirements.txt
```

### Error de variables de entorno
Verifica que el archivo `.env` esté presente y contenga todas las variables necesarias.
