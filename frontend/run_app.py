#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Streamlit
"""
import subprocess
import sys
import os

def main():
    # Cambiar al directorio del frontend
    frontend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(frontend_dir)
    
    # Ejecutar streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAplicación detenida por el usuario")
        sys.exit(0)

if __name__ == "__main__":
    main()
