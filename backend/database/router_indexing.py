"""
Router para el sistema de indexación de Google Drive - VERSIÓN CORREGIDA
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from database.database import get_db
from database.models import Program, UserModel, IndexingJob, IndexedFile
from database.schemas import (
    DriveScanRequest, DriveScanResponse, IndexingStatusResponse,
    FileSearchRequest, FileSearchResponse, IndexedFileResponse,
    IndexingJobResponse
)
from apps.indexing_service import IndexingService, process_indexing_job_background
from apps.jwt import get_current_user_email
from apps.auth import get_current_user

router = APIRouter(prefix="/indexing", tags=["indexing"])


@router.post("/scan", response_model=DriveScanResponse)
async def start_drive_scan(
    request: DriveScanRequest,
    background_tasks: BackgroundTasks,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Inicia el escaneo e indexación de una carpeta de Google Drive
    """
    # Verificar que el programa existe y el usuario tiene acceso
    program = db.query(Program).filter(Program.id == request.program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Verificar permisos de acceso al programa
    has_access = False
    for access in program.access:
        if access.user_id == current_user.id and access.active:
            has_access = True
            break
    
    if not has_access:
        raise HTTPException(status_code=403, detail="No access to this program")
    
    # Verificar que el usuario tiene token de Google Drive
    if not current_user.google_access_token:
        raise HTTPException(
            status_code=400, 
            detail="Google Drive access token required. Please authenticate with Google Drive first."
        )
    
    # Crear servicio de indexación
    indexing_service = IndexingService(db)
    
    # Determinar folder_id
    folder_id = request.folder_id or program.drive_folder_id
    if not folder_id:
        raise HTTPException(
            status_code=400, 
            detail="No folder ID specified. Please provide a folder_id or ensure the program has a drive_folder_id."
        )
    
    # Iniciar trabajo de indexación
    try:
        # Crear el job (sin procesar aún)
        job = indexing_service.create_indexing_job(
            program_id=request.program_id,
            user_id=current_user.id,
            folder_id=folder_id,
            job_type=request.job_type
        )
        
        # Agregar tarea en background usando FastAPI BackgroundTasks
        background_tasks.add_task(
            process_indexing_job_background,
            job.id,
            current_user.google_access_token,
            request.include_trashed
        )
        
        return DriveScanResponse(
            job_id=job.id,
            message=f"Indexing job started for program {request.program_id}",
            status="started"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start indexing job: {str(e)}")


@router.get("/status/{job_id}", response_model=IndexingStatusResponse)
async def get_indexing_status(
    job_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el estado de un trabajo de indexación
    """
    # Verificar que el trabajo existe y el usuario tiene acceso
    job = db.query(IndexingJob).filter(IndexingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Indexing job not found")
    
    # Verificar permisos de acceso al programa
    program = db.query(Program).filter(Program.id == job.program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    has_access = False
    for access in program.access:
        if access.user_id == current_user.id and access.active:
            has_access = True
            break
    
    if not has_access:
        raise HTTPException(status_code=403, detail="No access to this program")
    
    # Obtener estado del trabajo
    indexing_service = IndexingService(db)
    status = indexing_service.get_indexing_status(job_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Indexing job not found")
    
    return IndexingStatusResponse(
        job_id=status["job_id"],
        status=status["status"],
        progress=status["progress"],
        error_message=status["error_message"],
        started_at=status["started_at"],
        completed_at=status["completed_at"]
    )


@router.get("/jobs/{program_id}", response_model=List[IndexingJobResponse])
async def get_indexing_jobs(
    program_id: int,
    limit: int = 20,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene los trabajos de indexación de un programa
    """
    # Verificar que el programa existe y el usuario tiene acceso
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Verificar permisos de acceso al programa
    has_access = False
    for access in program.access:
        if access.user_id == current_user.id and access.active:
            has_access = True
            break
    
    if not has_access:
        raise HTTPException(status_code=403, detail="No access to this program")
    
    # Obtener trabajos de indexación
    indexing_service = IndexingService(db)
    jobs = indexing_service.get_indexing_jobs(program_id, limit)
    
    return jobs


@router.post("/search", response_model=FileSearchResponse)
async def search_files(
    request: FileSearchRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Busca archivos indexados en un programa
    """
    # Verificar que el programa existe y el usuario tiene acceso
    program = db.query(Program).filter(Program.id == request.program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Verificar permisos de acceso al programa
    has_access = False
    for access in program.access:
        if access.user_id == current_user.id and access.active:
            has_access = True
            break
    
    if not has_access:
        raise HTTPException(status_code=403, detail="No access to this program")
    
    # Buscar archivos
    indexing_service = IndexingService(db)
    files, total_count = indexing_service.search_files(
        program_id=request.program_id,
        query=request.query,
        file_types=request.file_types,
        limit=request.limit
    )
    
    return FileSearchResponse(
        files=files,
        total_count=total_count,
        query=request.query
    )


@router.get("/files/{program_id}", response_model=List[IndexedFileResponse])
async def get_program_files(
    program_id: int,
    file_types: Optional[str] = None,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los archivos indexados de un programa
    """
    # Verificar que el programa existe y el usuario tiene acceso
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Verificar permisos de acceso al programa
    has_access = False
    for access in program.access:
        if access.user_id == current_user.id and access.active:
            has_access = True
            break
    
    if not has_access:
        raise HTTPException(status_code=403, detail="No access to this program")
    
    # Obtener archivos
    indexing_service = IndexingService(db)
    file_types_list = file_types.split(",") if file_types else None
    files = indexing_service.get_program_files(
        program_id=program_id,
        file_types=file_types_list,
        limit=limit
    )
    
    return files


@router.get("/files/{program_id}/stats")
async def get_file_stats(
    program_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene estadísticas de archivos indexados de un programa
    """
    # Verificar que el programa existe y el usuario tiene acceso
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Verificar permisos de acceso al programa
    has_access = False
    for access in program.access:
        if access.user_id == current_user.id and access.active:
            has_access = True
            break
    
    if not has_access:
        raise HTTPException(status_code=403, detail="No access to this program")
    
    # Obtener estadísticas
    total_files = db.query(IndexedFile).filter(IndexedFile.program_id == program_id).count()
    completed_files = db.query(IndexedFile).filter(
        IndexedFile.program_id == program_id,
        IndexedFile.indexing_status == "completed"
    ).count()
    failed_files = db.query(IndexedFile).filter(
        IndexedFile.program_id == program_id,
        IndexedFile.indexing_status == "failed"
    ).count()
    
    # Estadísticas por tipo de archivo
    file_types = db.query(IndexedFile.file_type, func.count(IndexedFile.id)).filter(
        IndexedFile.program_id == program_id,
        IndexedFile.indexing_status == "completed"
    ).group_by(IndexedFile.file_type).all()
    
    # Tamaño total
    total_size = db.query(func.sum(IndexedFile.file_size)).filter(
        IndexedFile.program_id == program_id,
        IndexedFile.indexing_status == "completed"
    ).scalar() or 0
    
    return {
        "total_files": total_files,
        "completed_files": completed_files,
        "failed_files": failed_files,
        "total_size_bytes": total_size,
        "file_types": dict(file_types),
        "last_updated": program.updated_at
    }


@router.delete("/files/{program_id}")
async def clear_indexed_files(
    program_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina todos los archivos indexados de un programa
    """
    # Verificar que el programa existe y el usuario tiene acceso
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Verificar permisos de acceso al programa (solo owner puede limpiar)
    has_access = False
    for access in program.access:
        if access.user_id == current_user.id and access.active and access.role == "owner":
            has_access = True
            break
    
    if not has_access:
        raise HTTPException(status_code=403, detail="Only program owners can clear indexed files")
    
    # Eliminar archivos indexados
    deleted_count = db.query(IndexedFile).filter(IndexedFile.program_id == program_id).delete()
    db.commit()
    
    return {
        "message": f"Deleted {deleted_count} indexed files",
        "deleted_count": deleted_count
    }