#!/usr/bin/env python3
"""
Script para resetear el job 8 manualmente
"""
import os
import sys
import psycopg2
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydatabase',
    'user': 'user',
    'password': 'password'
}

def reset_job_8():
    """Resetea el job 8 manualmente"""
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Verificar el estado actual del job 8
        cursor.execute("""
            SELECT id, status, total_files, processed_files, started_at, created_at
            FROM indexing_jobs 
            WHERE id = 8
        """)
        
        job = cursor.fetchone()
        if job:
            print(f"Job 8 actual: ID={job[0]}, Status={job[1]}, Total={job[2]}, Processed={job[3]}")
            print(f"Started: {job[4]}, Created: {job[5]}")
        else:
            print("Job 8 no encontrado")
            return
        
        # Resetear el job 8
        cursor.execute("""
            UPDATE indexing_jobs 
            SET status = 'failed', 
                error_message = 'Manual reset - job was stuck', 
                completed_at = NOW()
            WHERE id = 8 AND status = 'running'
        """)
        
        rows_affected = cursor.rowcount
        conn.commit()
        
        if rows_affected > 0:
            print(f"✅ Job 8 reseteado exitosamente ({rows_affected} fila actualizada)")
        else:
            print("ℹ️ Job 8 no estaba en estado 'running' o ya fue reseteado")
        
        # Verificar el estado después del reset
        cursor.execute("""
            SELECT id, status, total_files, processed_files, error_message
            FROM indexing_jobs 
            WHERE id = 8
        """)
        
        job_after = cursor.fetchone()
        if job_after:
            print(f"Job 8 después del reset: ID={job_after[0]}, Status={job_after[1]}, Error={job_after[4]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Asegúrate de que PostgreSQL esté corriendo y las credenciales sean correctas")

if __name__ == "__main__":
    print("🔧 Reseteando Job 8...")
    reset_job_8()
    print("✅ Proceso completado")
