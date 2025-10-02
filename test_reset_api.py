#!/usr/bin/env python3
"""
Script para probar el reset del job 8 usando la API
"""
import requests
import json

# Configuración
API_BASE_URL = "http://localhost:7000"
PROGRAM_ID = 1  # Cambia esto por el ID de tu programa

def test_reset_api():
    """Prueba el endpoint de reset"""
    try:
        # Primero, obtener el estado actual
        print("🔍 Obteniendo estado actual...")
        resp = requests.get(f"{API_BASE_URL}/api/indexing/jobs/{PROGRAM_ID}", timeout=10)
        
        if resp.status_code == 200:
            jobs = resp.json()
            print(f"Jobs encontrados: {len(jobs)}")
            for job in jobs[:3]:
                print(f"  - Job {job.get('id')}: Status={job.get('status')}, Total={job.get('total_files')}, Processed={job.get('processed_files')}")
        else:
            print(f"❌ Error al obtener jobs: {resp.status_code}")
            return
        
        # Intentar resetear jobs pegados
        print("\n🔧 Reseteando jobs pegados...")
        resp = requests.post(f"{API_BASE_URL}/api/indexing/reset-stuck-jobs/{PROGRAM_ID}", timeout=10)
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"✅ {result.get('message', 'Jobs reseteados')}")
            print(f"Jobs reseteados: {result.get('reset_count', 0)}")
        else:
            print(f"❌ Error al resetear: {resp.status_code}")
            print(f"Respuesta: {resp.text}")
        
        # Verificar el estado después del reset
        print("\n🔍 Verificando estado después del reset...")
        resp = requests.get(f"{API_BASE_URL}/api/indexing/jobs/{PROGRAM_ID}", timeout=10)
        
        if resp.status_code == 200:
            jobs = resp.json()
            print(f"Jobs después del reset: {len(jobs)}")
            for job in jobs[:3]:
                print(f"  - Job {job.get('id')}: Status={job.get('status')}, Total={job.get('total_files')}, Processed={job.get('processed_files')}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Asegúrate de que el backend esté corriendo en el puerto 7000")

if __name__ == "__main__":
    print("🚀 Probando reset de jobs pegados...")
    test_reset_api()
    print("✅ Proceso completado")
