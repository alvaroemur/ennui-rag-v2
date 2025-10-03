from fastapi import Depends, HTTPException, Request
from fastapi import FastAPI
from database.database import engine, get_db
import database.models as models
from database.router_user import router as user_router
from database.router_post import router as post_router
from database.router_program import router as program_router
from database.router_indexing import router as indexing_router
from apps.jwt import get_current_user_email
from apps.auth import get_current_user
from apps.indexing_service import IndexingService
from apps.job_queue_processor import get_processor, start_processor, stop_processor, is_processor_running, get_processor_status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

# Pydantic models
class ProcessFolderRequest(BaseModel):
    folder_id: str

# Session-based authentication function
def get_current_user_from_session(request: Request, db: Session = Depends(get_db)) -> models.UserModel:
    """
    Get current user from session cookie or URL parameter
    """
    # Try to get session_id from cookie first, then from URL parameter
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = request.query_params.get("session_id")
    
    if not session_id:
        raise HTTPException(status_code=401, detail="No session found")
    
    # Find active session
    session = db.query(models.UserSession).filter(
        models.UserSession.session_id == session_id,
        models.UserSession.is_active == True,
        models.UserSession.expires_at > datetime.utcnow()
    ).first()
    
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    # Get user
    user = db.query(models.UserModel).filter(models.UserModel.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Update last accessed time
    session.last_accessed = datetime.utcnow()
    db.commit()
    
    return user

api_app = FastAPI()

# Include routers
api_app.include_router(router=user_router)
api_app.include_router(router=post_router)
api_app.include_router(router=program_router)
api_app.include_router(router=indexing_router)


@api_app.get('/')
def test():
    return {'message': 'unprotected api_app endpoint'}


@api_app.get('/protected')
def test2(current_email: str = Depends(get_current_user_email)):
    print(f'Current email: {current_email}')
    return {'message': 'protected api_app endpoint'}


@api_app.post("/indexing/reset-stuck-jobs/{program_id}")
async def reset_stuck_jobs(
    program_id: int,
    current_user: models.UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Resetea jobs de indexación que están pegados en estado 'running'
    """
    # Verificar que el programa existe y el usuario tiene acceso
    program = db.query(models.Program).filter(models.Program.id == program_id).first()
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
    
    # Buscar jobs que están en estado 'running' (todos, no solo los de más de 5 minutos)
    stuck_jobs = db.query(models.IndexingJob).filter(
        models.IndexingJob.program_id == program_id,
        models.IndexingJob.status == "running"
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


@api_app.post("/test/process-folder")
async def test_process_folder(
    request_data: ProcessFolderRequest,
    current_user: models.UserModel = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """
    Test endpoint to start processing a specific Google Drive folder
    Requires session-based authentication via session_id cookie
    Now uses database job queue instead of BackgroundTasks
    """
    folder_id = request_data.folder_id
    
    try:
        # First, we need to find or create a program with this folder ID
        program = db.query(models.Program).filter(
            models.Program.drive_folder_id == folder_id
        ).first()
        
        if not program:
            # Create a program for this folder
            program = models.Program(
                drive_folder_id=folder_id,
                drive_folder_name=f"Folder {folder_id}",
                internal_code=f"FOLDER_{folder_id[:8]}",
                name=f"Processing Folder {folder_id}",
                main_client="Unknown",
                main_beneficiaries="Unknown",
                created_by_user_id=current_user.id
            )
            db.add(program)
            db.commit()
            db.refresh(program)
            
            # Create program access for the user
            program_access = models.ProgramAccess(
                program_id=program.id,
                user_id=current_user.id,
                role="owner",
                active=True
            )
            db.add(program_access)
            db.commit()
        
        # Get Google access token from user's stored tokens
        access_token = current_user.google_access_token
        if not access_token:
            raise HTTPException(
                status_code=400, 
                detail="No Google access token found. Please authenticate with Google first."
            )
        
        # Create indexing service and job
        indexing_service = IndexingService(db)
        job = indexing_service.create_indexing_job(
            program_id=program.id,
            user_id=current_user.id,
            folder_id=folder_id,
            job_type="specific_folder",
            priority=1,  # Higher priority for test jobs
            access_token=access_token,
            include_trashed=False
        )
        
        # Get final queue status
        queue_status = indexing_service.get_queue_status()
        
        logger.info(f"🚀 Test folder processing job created - Job ID: {job.id}, Folder: {folder_id}, Program: {program.name} (ID: {program.id})")
        logger.info(f"📊 Final queue status - Pending: {queue_status['pending_jobs']}, Running: {queue_status['running_jobs']}, Completed: {queue_status['completed_jobs']}, Failed: {queue_status['failed_jobs']}")
        
        return {
            "message": f"Added folder processing job to queue: {folder_id}",
            "job_id": job.id,
            "program_id": program.id,
            "user_id": current_user.id,
            "status": "queued",
            "folder_id": folder_id,
            "queue_position": queue_status["pending_jobs"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding folder processing job: {str(e)}")


@api_app.get("/job-queue/status")
async def get_job_queue_status(
    current_user: models.UserModel = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """
    Get job queue status and processor information
    """
    try:
        indexing_service = IndexingService(db)
        queue_status = indexing_service.get_queue_status()
        processor_status = get_processor_status()
        
        logger.info(f"📊 Queue status requested by user {current_user.id} - Pending: {queue_status['pending_jobs']}, Running: {queue_status['running_jobs']}, Completed: {queue_status['completed_jobs']}, Failed: {queue_status['failed_jobs']}")
        logger.info(f"🔧 Processor status - Running: {is_processor_running()}, Process ID: {processor_status.get('process_id', 'N/A')}")
        
        return {
            "queue": queue_status,
            "processor": processor_status,
            "is_processor_running": is_processor_running()
        }
    except Exception as e:
        logger.error(f"❌ Error getting queue status for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting queue status: {str(e)}")


@api_app.post("/job-queue/start-processor")
async def start_job_processor(
    current_user: models.UserModel = Depends(get_current_user_from_session)
):
    """
    Start the job processor (admin only)
    """
    try:
        if is_processor_running():
            return {"message": "Processor is already running", "status": "running"}
        
        logger.info("🚀 Manually starting job processor...")
        start_processor()
        logger.info("✅ Job processor started manually")
        return {"message": "Job processor started", "status": "started"}
    except Exception as e:
        logger.error(f"❌ Error starting processor manually: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting processor: {str(e)}")


@api_app.post("/job-queue/stop-processor")
async def stop_job_processor(
    current_user: models.UserModel = Depends(get_current_user_from_session)
):
    """
    Stop the job processor (admin only)
    """
    try:
        if not is_processor_running():
            return {"message": "Processor is not running", "status": "stopped"}
        
        stop_processor()
        return {"message": "Job processor stopped", "status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping processor: {str(e)}")


@api_app.get("/job-queue/jobs/{program_id}")
async def get_program_jobs(
    program_id: int,
    limit: int = 20,
    current_user: models.UserModel = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """
    Get indexing jobs for a specific program
    """
    try:
        # Verify user has access to program
        program = db.query(models.Program).filter(models.Program.id == program_id).first()
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
        
        # Check access
        has_access = False
        for access in program.access:
            if access.user_id == current_user.id and access.active:
                has_access = True
                break
        
        if not has_access:
            raise HTTPException(status_code=403, detail="No access to this program")
        
        indexing_service = IndexingService(db)
        jobs = indexing_service.get_indexing_jobs(program_id, limit)
        
        return {
            "program_id": program_id,
            "jobs": [
                {
                    "id": job.id,
                    "job_type": job.job_type,
                    "status": job.status,
                    "priority": job.priority,
                    "created_at": job.created_at,
                    "started_at": job.started_at,
                    "completed_at": job.completed_at,
                    "progress": {
                        "total_files": job.total_files,
                        "processed_files": job.processed_files,
                        "successful_files": job.successful_files,
                        "failed_files": job.failed_files
                    },
                    "error_message": job.error_message
                }
                for job in jobs
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting program jobs: {str(e)}")


@api_app.post("/job-queue/jobs/{job_id}/cancel")
async def cancel_job(
    job_id: int,
    current_user: models.UserModel = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """
    Cancel a pending or running job
    """
    try:
        job = db.query(models.IndexingJob).filter(models.IndexingJob.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Verify user has access to the program
        program = db.query(models.Program).filter(models.Program.id == job.program_id).first()
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
        
        has_access = False
        for access in program.access:
            if access.user_id == current_user.id and access.active:
                has_access = True
                break
        
        if not has_access:
            raise HTTPException(status_code=403, detail="No access to this program")
        
        # Only cancel pending or running jobs
        if job.status not in ["pending", "running"]:
            raise HTTPException(status_code=400, detail=f"Cannot cancel job with status: {job.status}")
        
        job.status = "cancelled"
        job.completed_at = datetime.utcnow()
        job.error_message = "Cancelled by user"
        db.commit()
        
        return {"message": f"Job {job_id} cancelled", "job_id": job_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling job: {str(e)}")
