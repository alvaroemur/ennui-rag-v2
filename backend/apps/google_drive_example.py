"""
Ejemplo de uso del Google Drive Scanner
"""
import asyncio
from google_drive import GoogleDriveScanner, scan_google_drive, get_file_metadata


async def example_usage():
    """Ejemplo de cómo usar el Google Drive Scanner"""
    
    # Token de acceso OAuth2 (obtenido del flujo de autenticación)
    access_token = "your_oauth2_access_token_here"
    
    # Crear instancia del scanner
    scanner = GoogleDriveScanner(access_token)
    
    print("=== Ejemplo de Escaneo de Google Drive ===\n")
    
    # 1. Escanear todo el Drive
    print("1. Escaneando todo el Google Drive...")
    all_files = await scanner.scan_folder_recursive()
    print(f"   Total de archivos encontrados: {len(all_files)}")
    
    # 2. Escanear una carpeta específica
    print("\n2. Escaneando carpeta específica...")
    folder_id = "1ABC123DEF456GHI789"  # Reemplazar con ID real
    folder_files = await scanner.scan_folder_recursive(folder_id)
    print(f"   Archivos en la carpeta: {len(folder_files)}")
    
    # 3. Obtener metadatos de un archivo específico
    print("\n3. Obteniendo metadatos de archivo específico...")
    file_id = "1XYZ789ABC123DEF456"  # Reemplazar con ID real
    file_metadata = await get_file_metadata(access_token, file_id)
    if file_metadata:
        print(f"   Archivo: {file_metadata['name']}")
        print(f"   Tipo: {file_metadata['file_type']}")
        print(f"   Tamaño: {file_metadata['size_formatted']}")
        print(f"   Modificado: {file_metadata['modifiedTime']}")
    
    # 4. Descargar contenido de un archivo
    print("\n4. Descargando contenido de archivo...")
    if file_metadata and file_metadata['downloadable']:
        content = await scanner.get_file_content(file_id)
        if content:
            print(f"   Contenido descargado: {len(content)} bytes")
        else:
            print("   Error descargando contenido")
    
    # 5. Exportar documento de Google
    print("\n5. Exportando documento de Google...")
    if file_metadata and file_metadata['is_google_doc']:
        exported_content = await scanner.export_google_doc(file_id, 'text/plain')
        if exported_content:
            print(f"   Documento exportado: {len(exported_content)} bytes")
            print(f"   Contenido (primeros 200 chars): {exported_content[:200].decode('utf-8')}")
        else:
            print("   Error exportando documento")
    
    # 6. Usar función de conveniencia
    print("\n6. Usando función de conveniencia...")
    files = await scan_google_drive(access_token, include_trashed=False)
    print(f"   Archivos (sin papelera): {len(files)}")
    
    # 7. Mostrar estadísticas de archivos
    print("\n7. Estadísticas de archivos:")
    file_types = {}
    total_size = 0
    
    for file in all_files[:100]:  # Solo primeros 100 para el ejemplo
        file_type = file.get('file_type', 'unknown')
        file_types[file_type] = file_types.get(file_type, 0) + 1
        total_size += int(file.get('size', 0))
    
    print(f"   Total de archivos analizados: {len(all_files[:100])}")
    print(f"   Tamaño total: {scanner._format_file_size(total_size)}")
    print("   Distribución por tipo:")
    for file_type, count in file_types.items():
        print(f"     {file_type}: {count} archivos")


async def example_with_error_handling():
    """Ejemplo con manejo de errores"""
    
    access_token = "invalid_token"  # Token inválido para demostrar manejo de errores
    
    try:
        print("=== Ejemplo con Manejo de Errores ===\n")
        
        # Intentar escanear con token inválido
        files = await scan_google_drive(access_token)
        print(f"Archivos encontrados: {len(files)}")
        
    except Exception as e:
        print(f"Error durante el escaneo: {str(e)}")
        print("Esto es esperado con un token inválido")
    
    # Ejemplo con token válido pero archivo inexistente
    try:
        valid_token = "your_valid_token_here"
        invalid_file_id = "invalid_file_id"
        
        metadata = await get_file_metadata(valid_token, invalid_file_id)
        if metadata is None:
            print("Archivo no encontrado (esto es esperado)")
        
    except Exception as e:
        print(f"Error obteniendo metadatos: {str(e)}")


if __name__ == "__main__":
    print("Ejecutando ejemplos de Google Drive Scanner...")
    print("NOTA: Necesitas un token de acceso OAuth2 válido para que funcionen los ejemplos.")
    print("Reemplaza 'your_oauth2_access_token_here' con tu token real.\n")
    
    # Ejecutar ejemplos
    asyncio.run(example_usage())
    asyncio.run(example_with_error_handling())
