"""
Router de emergencia para limpiar jobs de indexación pegados
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database.database import get_db
from database.models import Program, UserModel, IndexingJob
from apps.jwt import get_current_user_email
from apps.auth import get_current_user

router = APIRouter(prefix="/indexing", tags=["indexing"])


@router.post("/reset-stuck-jobs/{program_id}")
async def reset_stuck_jobs(
    program_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Resetea jobs de indexación que están pegados en estado 'running'
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
    
    # Buscar jobs que están en estado 'running' por más de 30 minutos
    thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)
    
    stuck_jobs = db.query(IndexingJob).filter(
        IndexingJob.program_id == program_id,
        IndexingJob.status == "running",
        IndexingJob.started_at < thirty_minutes_ago
    ).all()
    
    # Marcar jobs como fallidos
    for job in stuck_jobs:
        job.status = "failed"
        job.error_message = "Job reset due to timeout - likely stuck"
        job.completed_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "message": f"Reset {len(stuck_jobs)} stuck jobs",
        "reset_count": len(stuck_jobs),
        "program_id": program_id
    }


@router.get("/jobs-status/{program_id}")
async def get_jobs_status(
    program_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el estado detallado de todos los jobs de un programa
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
    
    # Obtener todos los jobs del programa
    jobs = db.query(IndexingJob).filter(
        IndexingJob.program_id == program_id
    ).order_by(IndexingJob.created_at.desc()).all()
    
    jobs_data = []
    for job in jobs:
        jobs_data.append({
            "id": job.id,
            "status": job.status,
            "job_type": job.job_type,
            "total_files": job.total_files,
            "processed_files": job.processed_files,
            "successful_files": job.successful_files,
            "failed_files": job.failed_files,
            "error_message": job.error_message,
            "created_at": job.created_at.isoformat() if job.created_at else None,
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "duration_minutes": (
                (job.completed_at - job.started_at).total_seconds() / 60 
                if job.started_at and job.completed_at else None
            )
        })
    
    return {
        "program_id": program_id,
        "total_jobs": len(jobs),
        "jobs": jobs_data
    }
