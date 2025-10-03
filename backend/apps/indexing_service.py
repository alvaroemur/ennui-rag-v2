"""
Servicio de indexación de Google Drive para programas - VERSIÓN CON JOB QUEUE
"""
import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from database.models import Program, IndexedFile, IndexingJob, UserModel
from database.database import get_db
from apps.google_drive import GoogleDriveScanner, get_file_metadata
from apps.jwt import get_current_user_email

logger = logging.getLogger(__name__)


class IndexingService:
    """Servicio para indexar archivos de Google Drive"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_indexing_job(
        self, 
        program_id: int, 
        user_id: int,
        folder_id: Optional[str] = None,
        job_type: str = "full_scan",
        priority: int = 0,
        access_token: Optional[str] = None,
        include_trashed: bool = False,
        scheduled_at: Optional[datetime] = None
    ) -> IndexingJob:
        """
        Crea un trabajo de indexación en la cola de trabajos
        
        Args:
            program_id: ID del programa
            user_id: ID del usuario que inicia el trabajo
            folder_id: ID de carpeta específica (opcional)
            job_type: Tipo de trabajo (full_scan, incremental, specific_folder)
            priority: Prioridad del trabajo (mayor número = mayor prioridad)
            access_token: Token de acceso de Google (opcional, se obtiene del usuario si no se proporciona)
            include_trashed: Incluir archivos en papelera
            scheduled_at: Cuándo procesar el trabajo (opcional, inmediato si no se especifica)
        
        Returns:
            IndexingJob creado
        """
        # Preparar parámetros del trabajo
        job_parameters = {
            "include_trashed": include_trashed
        }
        
        if access_token:
            job_parameters["access_token"] = access_token
        
        # Crear trabajo de indexación
        indexing_job = IndexingJob(
            program_id=program_id,
            user_id=user_id,
            job_type=job_type,
            folder_id=folder_id,
            status="pending",
            priority=priority,
            scheduled_at=scheduled_at,
            job_parameters=json.dumps(job_parameters)
        )
        
        self.db.add(indexing_job)
        self.db.commit()
        self.db.refresh(indexing_job)
        
        # Get current queue status for logging
        queue_status = self.get_queue_status()
        
        logger.info(f"📝 Created indexing job {indexing_job.id} for program {program_id} (type: {job_type}, priority: {priority})")
        logger.info(f"📊 Queue status after job creation - Pending: {queue_status['pending_jobs']}, Running: {queue_status['running_jobs']}, Completed: {queue_status['completed_jobs']}, Failed: {queue_status['failed_jobs']}")
        
        return indexing_job
    
    async def _process_indexing_job(
        self, 
        job_id: int, 
        access_token: str, 
        include_trashed: bool = False
    ):
        """
        Procesa un trabajo de indexación en background
        
        Args:
            job_id: ID del trabajo de indexación
            access_token: Token de acceso de Google Drive
            include_trashed: Incluir archivos en papelera
        """
        try:
            # Obtener trabajo de la base de datos
            job = self.db.query(IndexingJob).filter(IndexingJob.id == job_id).first()
            if not job:
                logger.error(f"Indexing job {job_id} not found")
                return
            
            # Actualizar estado a "running"
            job.status = "running"
            job.started_at = datetime.utcnow()
            self.db.commit()
            
            # Obtener programa
            program = self.db.query(Program).filter(Program.id == job.program_id).first()
            if not program:
                job.status = "failed"
                job.error_message = "Program not found"
                self.db.commit()
                return
            
            # Escanear Google Drive
            scanner = GoogleDriveScanner(access_token)
            folder_id = job.folder_id or program.drive_folder_id
            
            logger.info(f"Starting scan for program {program.id}, folder {folder_id}")
            files = await scanner.scan_folder_recursive(folder_id, include_trashed)
            
            # Actualizar contadores
            job.total_files = len(files)
            job.processed_files = 0
            job.successful_files = 0
            job.failed_files = 0
            self.db.commit()
            
            # Procesar cada archivo
            for file_data in files:
                try:
                    await self._process_file(job, program, file_data, scanner)
                    job.successful_files += 1
                except Exception as e:
                    logger.error(f"Error processing file {file_data.get('id')}: {str(e)}")
                    job.failed_files += 1
                    
                    # Crear registro de archivo fallido
                    self._create_failed_file_record(job, file_data, str(e))
                
                job.processed_files += 1
                
                # Actualizar progreso cada 10 archivos
                if job.processed_files % 10 == 0:
                    self.db.commit()
            
            # Marcar trabajo como completado
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Indexing job {job_id} completed. Processed: {job.processed_files}, "
                       f"Successful: {job.successful_files}, Failed: {job.failed_files}")
            
        except Exception as e:
            logger.error(f"Error in indexing job {job_id}: {str(e)}")
            job = self.db.query(IndexingJob).filter(IndexingJob.id == job_id).first()
            if job:
                job.status = "failed"
                job.error_message = str(e)
                job.completed_at = datetime.utcnow()
                self.db.commit()
    
    async def _process_file(
        self, 
        job: IndexingJob, 
        program: Program, 
        file_data: Dict, 
        scanner: GoogleDriveScanner
    ):
        """
        Procesa un archivo individual
        
        Args:
            job: Trabajo de indexación
            program: Programa
            file_data: Datos del archivo de Google Drive
            scanner: Scanner de Google Drive
        """
        file_id = file_data.get("id")
        if not file_id:
            return
        
        # Verificar si el archivo ya existe
        existing_file = self.db.query(IndexedFile).filter(
            and_(
                IndexedFile.drive_folder_id == program.drive_folder_id,
                IndexedFile.drive_file_id == file_id
            )
        ).first()
        
        # Obtener contenido del archivo con gestión de memoria optimizada
        content_text = None
        
        # Get file information
        file_name = file_data.get("name", "unknown")
        file_size = file_data.get("size", 0)
        file_size_mb = file_size / (1024 * 1024)
        mime_type = file_data.get("mimeType", "")
        modified_time = file_data.get("modifiedTime", "")
        
        # Use modified time as content hash (changes when file content changes)
        content_hash = hashlib.md5(modified_time.encode()).hexdigest() if modified_time else None
        
        # Only process content text for files under 100MB (videos and large files get metadata only)
        should_process_content = file_size_mb < 100  # Under 100MB
        
        if not should_process_content:
            logger.info(f"📏 Skipping content download for large file {file_id} ({file_name}): {file_size_mb:.1f}MB >= 100MB limit (metadata only)")
        else:
            try:
                if file_data.get("is_google_doc"):
                    # Exportar documento de Google
                    logger.debug(f"📄 Exporting Google Doc: {file_id}")
                    content_bytes = await scanner.export_google_doc(file_id, "text/plain")
                elif file_data.get("downloadable"):
                    # Descargar archivo normal
                    logger.debug(f"📥 Downloading file: {file_id}")
                    content_bytes = await scanner.get_file_content(file_id)
                else:
                    content_bytes = None
                
                if content_bytes:
                    # Log content size for monitoring
                    content_size_mb = len(content_bytes) / (1024 * 1024)
                    logger.debug(f"📊 File content size: {content_size_mb:.1f}MB for {file_id}")
                    
                    # Decode content with memory management
                    content_text = content_bytes.decode('utf-8', errors='ignore')
                    
                    # Clear content_bytes to free memory immediately
                    del content_bytes
                    
                    # Sanitizar contenido: remover caracteres NUL y otros caracteres problemáticos
                    content_text = self._sanitize_content(content_text)
                    
                    # Recalculate hash from actual content for text files
                    content_hash = hashlib.md5(content_text.encode()).hexdigest()
                    
                    logger.debug(f"✅ Content processed for {file_id}: {len(content_text)} chars, hash: {content_hash[:8]}...")
            
            except Exception as e:
                logger.warning(f"Could not extract content from file {file_id}: {str(e)}")
                # Ensure content variables are None on error
                content_text = None
                # Keep the modified time hash as fallback
                content_hash = hashlib.md5(modified_time.encode()).hexdigest() if modified_time else None
        
        # Crear o actualizar registro de archivo
        if existing_file:
            # Actualizar archivo existente
            existing_file.drive_file_name = self._sanitize_content(file_data.get("name", ""))
            existing_file.file_type = self._sanitize_content(file_data.get("file_type", ""))
            existing_file.file_size = file_data.get("size", 0)
            existing_file.web_view_link = self._sanitize_content(file_data.get("web_view_link", ""))
            existing_file.description = self._sanitize_content(file_data.get("description", ""))
            existing_file.parents = json.dumps(file_data.get("parents", [])) if file_data.get("parents") else None
            existing_file.owners = json.dumps(file_data.get("owners", [])) if file_data.get("owners") else None
            existing_file.last_modifying_user = json.dumps(file_data.get("last_modifying_user", {})) if file_data.get("last_modifying_user") else None
            existing_file.md5_checksum = file_data.get("md5_checksum")
            existing_file.is_google_doc = file_data.get("is_google_doc", False)
            existing_file.is_downloadable = file_data.get("downloadable", True)
            existing_file.content_text = content_text
            existing_file.indexing_status = "completed"
            existing_file.last_indexed_at = datetime.utcnow()
            existing_file.drive_created_time = self._parse_datetime(file_data.get("created_time"))
            existing_file.drive_modified_time = self._parse_datetime(file_data.get("modified_time"))
        else:
            # Crear nuevo archivo
            indexed_file = IndexedFile(
                drive_folder_id=program.drive_folder_id,
                drive_file_id=file_id,
                drive_file_name=self._sanitize_content(file_data.get("name", "")),
                file_type=self._sanitize_content(file_data.get("file_type", "")),
                file_size=file_data.get("size", 0),
                web_view_link=self._sanitize_content(file_data.get("web_view_link", "")),
                description=self._sanitize_content(file_data.get("description", "")),
                parents=json.dumps(file_data.get("parents", [])) if file_data.get("parents") else None,
                owners=json.dumps(file_data.get("owners", [])) if file_data.get("owners") else None,
                last_modifying_user=json.dumps(file_data.get("last_modifying_user", {})) if file_data.get("last_modifying_user") else None,
                md5_checksum=file_data.get("md5_checksum"),
                content_text=content_text,
                is_google_doc=file_data.get("is_google_doc", False),
                is_downloadable=file_data.get("downloadable", True),
                indexing_status="completed",
                last_indexed_at=datetime.utcnow(),
                drive_created_time=self._parse_datetime(file_data.get("created_time")),
                drive_modified_time=self._parse_datetime(file_data.get("modified_time"))
            )
            self.db.add(indexed_file)
    
    def _create_failed_file_record(
        self, 
        job: IndexingJob, 
        file_data: Dict, 
        error_message: str
    ):
        """
        Crea un registro de archivo que falló al procesar
        
        Args:
            job: Trabajo de indexación
            file_data: Datos del archivo
            error_message: Mensaje de error
        """
        file_id = file_data.get("id", "")
        
        # Check if file already exists
        existing_file = self.db.query(IndexedFile).filter(
            and_(
                IndexedFile.program_id == job.program_id,
                IndexedFile.drive_file_id == file_id
            )
        ).first()
        
        if existing_file:
            # Update existing file with error status
            existing_file.indexing_status = "failed"
            existing_file.indexing_error = self._sanitize_content(error_message)
            existing_file.last_indexed_at = datetime.utcnow()
            logger.debug(f"Updated existing file {file_id} with error status")
        else:
            # Create new failed file record
            indexed_file = IndexedFile(
                program_id=job.program_id,
                drive_file_id=self._sanitize_content(file_id),
                drive_file_name=self._sanitize_content(file_data.get("name", "")),
                mime_type=self._sanitize_content(file_data.get("mimeType", "")),
                file_type=self._sanitize_content(file_data.get("file_type", "")),
                file_size=file_data.get("size", 0),
                web_view_link=self._sanitize_content(file_data.get("webViewLink", "")),
                is_google_doc=file_data.get("is_google_doc", False),
                is_downloadable=file_data.get("downloadable", True),
                indexing_status="failed",
                indexing_error=self._sanitize_content(error_message),
                last_indexed_at=datetime.utcnow(),
                drive_created_time=self._parse_datetime(file_data.get("createdTime")),
                drive_modified_time=self._parse_datetime(file_data.get("modifiedTime"))
            )
            self.db.add(indexed_file)
            logger.debug(f"Created new failed file record for {file_id}")
    
    def _sanitize_content(self, content: str) -> str:
        """
        Sanitiza el contenido de texto removiendo caracteres problemáticos
        
        Args:
            content: Contenido de texto a sanitizar
        
        Returns:
            Contenido sanitizado
        """
        if not content:
            return content
        
        # Remover caracteres NUL (0x00) y otros caracteres de control problemáticos
        # Mantener solo caracteres imprimibles y espacios
        sanitized = ''.join(char for char in content if ord(char) >= 32 or char in '\n\r\t')
        
        # Remover caracteres NUL específicamente (por si acaso)
        sanitized = sanitized.replace('\x00', '')
        
        # Limitar el tamaño del contenido para evitar problemas de base de datos
        max_length = 1000000  # 1MB de texto
        if len(sanitized) > max_length:
            # Asegurar que el texto truncado + mensaje no exceda el límite
            truncate_length = max_length - len("\n\n[CONTENT TRUNCATED]")
            sanitized = sanitized[:truncate_length] + "\n\n[CONTENT TRUNCATED]"
        
        return sanitized
    
    def _parse_datetime(self, datetime_str: Optional[str]) -> Optional[datetime]:
        """
        Parsea string de datetime de Google Drive
        
        Args:
            datetime_str: String de datetime de Google Drive
        
        Returns:
            datetime object o None
        """
        if not datetime_str:
            return None
        
        try:
            # Formato: 2023-12-01T10:30:00.000Z
            return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        except Exception:
            return None
    
    def get_indexing_status(self, job_id: int) -> Optional[Dict]:
        """
        Obtiene el estado de un trabajo de indexación
        
        Args:
            job_id: ID del trabajo
        
        Returns:
            Diccionario con el estado del trabajo
        """
        job = self.db.query(IndexingJob).filter(IndexingJob.id == job_id).first()
        if not job:
            return None
        
        return {
            "job_id": job.id,
            "status": job.status,
            "progress": {
                "total_files": job.total_files,
                "processed_files": job.processed_files,
                "successful_files": job.successful_files,
                "failed_files": job.failed_files
            },
            "error_message": job.error_message,
            "started_at": job.started_at,
            "completed_at": job.completed_at
        }
    
    def search_files(
        self, 
        drive_folder_id: str, 
        query: str, 
        file_types: Optional[List[str]] = None,
        limit: int = 50
    ) -> Tuple[List[IndexedFile], int]:
        """
        Busca archivos indexados en un programa
        
        Args:
            drive_folder_id: ID de la carpeta principal del programa
            query: Consulta de búsqueda
            file_types: Tipos de archivo a filtrar
            limit: Límite de resultados
        
        Returns:
            Tupla con lista de archivos y total de resultados
        """
        # Construir consulta base
        base_query = self.db.query(IndexedFile).filter(
            and_(
                IndexedFile.drive_folder_id == drive_folder_id,
                IndexedFile.indexing_status == "completed",
                or_(
                    IndexedFile.drive_file_name.ilike(f"%{query}%"),
                    IndexedFile.content_text.ilike(f"%{query}%")
                )
            )
        )
        
        # Filtrar por tipos de archivo
        if file_types:
            base_query = base_query.filter(IndexedFile.file_type.in_(file_types))
        
        # Obtener total de resultados
        total_count = base_query.count()
        
        # Obtener resultados paginados
        files = base_query.limit(limit).all()
        
        return files, total_count
    
    def get_program_files(
        self, 
        drive_folder_id: str, 
        file_types: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[IndexedFile]:
        """
        Obtiene todos los archivos indexados de un programa
        
        Args:
            drive_folder_id: ID de la carpeta principal del programa
            file_types: Tipos de archivo a filtrar
            limit: Límite de resultados
        
        Returns:
            Lista de archivos indexados
        """
        query = self.db.query(IndexedFile).filter(
            and_(
                IndexedFile.drive_folder_id == drive_folder_id,
                IndexedFile.indexing_status == "completed"
            )
        )
        
        if file_types:
            query = query.filter(IndexedFile.file_type.in_(file_types))
        
        return query.limit(limit).all()
    
    def get_indexing_jobs(self, program_id: int, limit: int = 20) -> List[IndexingJob]:
        """
        Obtiene los trabajos de indexación de un programa
        
        Args:
            program_id: ID del programa
            limit: Límite de resultados
        
        Returns:
            Lista de trabajos de indexación
        """
        return self.db.query(IndexingJob).filter(
            IndexingJob.program_id == program_id
        ).order_by(IndexingJob.created_at.desc()).limit(limit).all()


    def get_queue_status(self) -> Dict:
        """
        Obtiene el estado de la cola de trabajos
        
        Returns:
            Diccionario con estadísticas de la cola
        """
        # Contar trabajos por estado
        pending_count = self.db.query(IndexingJob).filter(IndexingJob.status == "pending").count()
        running_count = self.db.query(IndexingJob).filter(IndexingJob.status == "running").count()
        completed_count = self.db.query(IndexingJob).filter(IndexingJob.status == "completed").count()
        failed_count = self.db.query(IndexingJob).filter(IndexingJob.status == "failed").count()
        
        # Obtener trabajos más antiguos pendientes
        oldest_pending = self.db.query(IndexingJob).filter(
            IndexingJob.status == "pending"
        ).order_by(IndexingJob.created_at.asc()).first()
        
        return {
            "pending_jobs": pending_count,
            "running_jobs": running_count,
            "completed_jobs": completed_count,
            "failed_jobs": failed_count,
            "oldest_pending_job": {
                "id": oldest_pending.id if oldest_pending else None,
                "created_at": oldest_pending.created_at if oldest_pending else None,
                "job_type": oldest_pending.job_type if oldest_pending else None
            } if oldest_pending else None
        }