"""
Ejemplo de uso del sistema de indexación de Google Drive
"""
import asyncio
import requests
import json
from typing import Dict, Any

# Configuración del servidor
BASE_URL = "http://localhost:8000"  # Ajustar según tu configuración
API_BASE = f"{BASE_URL}/api"

# Headers para las peticiones (necesitarás un token JWT válido)
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"  # Reemplazar con token real
}


async def example_indexing_workflow():
    """Ejemplo completo del flujo de indexación"""
    
    print("=== Ejemplo de Indexación de Google Drive ===\n")
    
    # 1. Crear un programa (si no existe)
    print("1. Creando programa...")
    program_data = {
        "folder_link_or_id": "https://drive.google.com/drive/folders/1ABC123DEF456GHI789",
        "internal_code": "PROG-001",
        "name": "Programa de Ejemplo",
        "main_client": "Cliente Ejemplo",
        "main_beneficiaries": "Beneficiarios Ejemplo"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/programs/",
            headers=HEADERS,
            json=program_data
        )
        if response.status_code == 201:
            program = response.json()
            program_id = program["id"]
            print(f"   Programa creado con ID: {program_id}")
        else:
            print(f"   Error creando programa: {response.text}")
            return
    except Exception as e:
        print(f"   Error: {str(e)}")
        return
    
    # 2. Iniciar indexación
    print("\n2. Iniciando indexación...")
    scan_request = {
        "program_id": program_id,
        "folder_id": None,  # Usar la carpeta del programa
        "include_trashed": False,
        "job_type": "full_scan"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/indexing/scan",
            headers=HEADERS,
            json=scan_request
        )
        if response.status_code == 200:
            scan_result = response.json()
            job_id = scan_result["job_id"]
            print(f"   Trabajo de indexación iniciado con ID: {job_id}")
        else:
            print(f"   Error iniciando indexación: {response.text}")
            return
    except Exception as e:
        print(f"   Error: {str(e)}")
        return
    
    # 3. Monitorear progreso
    print("\n3. Monitoreando progreso...")
    max_attempts = 60  # 5 minutos máximo
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get(
                f"{API_BASE}/indexing/status/{job_id}",
                headers=HEADERS
            )
            if response.status_code == 200:
                status = response.json()
                progress = status["progress"]
                
                print(f"   Estado: {status['status']}")
                print(f"   Progreso: {progress['processed_files']}/{progress['total_files']} archivos")
                print(f"   Exitosos: {progress['successful_files']}, Fallidos: {progress['failed_files']}")
                
                if status["status"] in ["completed", "failed"]:
                    break
                
                if status["error_message"]:
                    print(f"   Error: {status['error_message']}")
                    break
            else:
                print(f"   Error obteniendo estado: {response.text}")
                break
                
        except Exception as e:
            print(f"   Error: {str(e)}")
            break
        
        await asyncio.sleep(5)  # Esperar 5 segundos
        attempt += 1
    
    # 4. Obtener estadísticas
    print("\n4. Obteniendo estadísticas...")
    try:
        response = requests.get(
            f"{API_BASE}/indexing/files/{program_id}/stats",
            headers=HEADERS
        )
        if response.status_code == 200:
            stats = response.json()
            print(f"   Total de archivos: {stats['total_files']}")
            print(f"   Archivos completados: {stats['completed_files']}")
            print(f"   Archivos fallidos: {stats['failed_files']}")
            print(f"   Tamaño total: {stats['total_size_bytes']} bytes")
            print("   Tipos de archivo:")
            for file_type, count in stats['file_types'].items():
                print(f"     {file_type}: {count}")
        else:
            print(f"   Error obteniendo estadísticas: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # 5. Buscar archivos
    print("\n5. Buscando archivos...")
    search_request = {
        "program_id": program_id,
        "query": "ejemplo",
        "limit": 10
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/indexing/search",
            headers=HEADERS,
            json=search_request
        )
        if response.status_code == 200:
            search_result = response.json()
            print(f"   Encontrados {search_result['total_count']} archivos con 'ejemplo'")
            print("   Primeros resultados:")
            for file in search_result['files'][:5]:
                print(f"     - {file['drive_file_name']} ({file['file_type']})")
        else:
            print(f"   Error buscando archivos: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # 6. Obtener archivos del programa
    print("\n6. Obteniendo archivos del programa...")
    try:
        response = requests.get(
            f"{API_BASE}/indexing/files/{program_id}?limit=20",
            headers=HEADERS
        )
        if response.status_code == 200:
            files = response.json()
            print(f"   Total de archivos obtenidos: {len(files)}")
            print("   Primeros archivos:")
            for file in files[:10]:
                print(f"     - {file['drive_file_name']} ({file['file_type']}) - {file['indexing_status']}")
        else:
            print(f"   Error obteniendo archivos: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    print("\n=== Ejemplo completado ===")


async def example_incremental_indexing():
    """Ejemplo de indexación incremental"""
    
    print("\n=== Ejemplo de Indexación Incremental ===\n")
    
    # Asumiendo que ya tienes un programa con ID 1
    program_id = 1
    
    # 1. Iniciar indexación incremental
    print("1. Iniciando indexación incremental...")
    scan_request = {
        "program_id": program_id,
        "folder_id": None,
        "include_trashed": False,
        "job_type": "incremental"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/indexing/scan",
            headers=HEADERS,
            json=scan_request
        )
        if response.status_code == 200:
            scan_result = response.json()
            job_id = scan_result["job_id"]
            print(f"   Trabajo de indexación incremental iniciado con ID: {job_id}")
        else:
            print(f"   Error iniciando indexación incremental: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")


async def example_file_search():
    """Ejemplo de búsqueda de archivos"""
    
    print("\n=== Ejemplo de Búsqueda de Archivos ===\n")
    
    program_id = 1
    
    # 1. Búsqueda por texto
    print("1. Búsqueda por texto...")
    search_request = {
        "program_id": program_id,
        "query": "informe",
        "file_types": ["pdf", "google_doc"],
        "limit": 20
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/indexing/search",
            headers=HEADERS,
            json=search_request
        )
        if response.status_code == 200:
            search_result = response.json()
            print(f"   Encontrados {search_result['total_count']} archivos con 'informe'")
            for file in search_result['files'][:5]:
                print(f"     - {file['drive_file_name']} ({file['file_type']})")
        else:
            print(f"   Error en búsqueda: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # 2. Búsqueda por tipo de archivo
    print("\n2. Búsqueda por tipo de archivo...")
    try:
        response = requests.get(
            f"{API_BASE}/indexing/files/{program_id}?file_types=pdf,docx&limit=10",
            headers=HEADERS
        )
        if response.status_code == 200:
            files = response.json()
            print(f"   Encontrados {len(files)} archivos PDF y DOCX")
            for file in files[:5]:
                print(f"     - {file['drive_file_name']} ({file['file_type']})")
        else:
            print(f"   Error obteniendo archivos: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")


if __name__ == "__main__":
    print("Ejecutando ejemplos de indexación...")
    print("NOTA: Asegúrate de tener un token JWT válido y que el servidor esté ejecutándose.")
    print("Reemplaza 'YOUR_JWT_TOKEN_HERE' con tu token real.\n")
    
    # Ejecutar ejemplos
    asyncio.run(example_indexing_workflow())
    asyncio.run(example_incremental_indexing())
    asyncio.run(example_file_search())
