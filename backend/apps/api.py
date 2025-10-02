from fastapi import Depends, HTTPException
from fastapi import FastAPI
from database.database import engine, get_db
import database.models as models
from database.router_user import router as user_router
from database.router_post import router as post_router
from database.router_program import router as program_router
from database.router_indexing import router as indexing_router
from apps.jwt import get_current_user_email
from apps.auth import get_current_user
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

models.Base.metadata.create_all(bind=engine)

api_app = FastAPI()
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
