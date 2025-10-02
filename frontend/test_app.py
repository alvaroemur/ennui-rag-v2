"""
Script de prueba para verificar que la app funciona correctamente
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todos los imports funcionen correctamente"""
    try:
        print("Probando imports...")
        
        # Importar módulos principales
        import streamlit as st
        print("✅ streamlit importado correctamente")
        
        from config import CUSTOM_CSS, API_BASE_URL_INTERNAL
        print("✅ config importado correctamente")
        
        from auth_utils import get_auth_headers
        print("✅ auth_utils importado correctamente")
        
        from repository_retrieval import render_retrieval_screen
        print("✅ repository_retrieval importado correctamente")
        
        from app import st
        print("✅ app importado correctamente")
        
        print("\n🎉 Todos los imports funcionan correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en imports: {str(e)}")
        return False

def test_functions():
    """Prueba que las funciones principales funcionen"""
    try:
        print("\nProbando funciones...")
        
        from auth_utils import get_auth_headers
        from repository_retrieval import format_file_size, format_datetime
        
        # Probar get_auth_headers (sin session state)
        headers = get_auth_headers()
        print(f"✅ get_auth_headers: {headers}")
        
        # Probar format_file_size
        size1 = format_file_size(1024)
        size2 = format_file_size(1048576)
        print(f"✅ format_file_size: 1024 bytes = {size1}")
        print(f"✅ format_file_size: 1048576 bytes = {size2}")
        
        # Probar format_datetime
        dt1 = format_datetime("2023-12-01T10:30:00Z")
        dt2 = format_datetime(None)
        print(f"✅ format_datetime: {dt1}")
        print(f"✅ format_datetime: {dt2}")
        
        print("\n🎉 Todas las funciones funcionan correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en funciones: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Prueba de la Aplicación ===\n")
    
    success = True
    success &= test_imports()
    success &= test_functions()
    
    if success:
        print("\n🎉 ¡La aplicación está lista para usar!")
        print("\nPara ejecutar la app:")
        print("streamlit run app.py")
    else:
        print("\n❌ Hay errores que necesitan ser corregidos")
        sys.exit(1)
