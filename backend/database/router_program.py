from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from database.schemas import ProgramCreate, ProgramResponse, PermissionRequestCreate, PermissionRequestResponse
from database.crud import (
    get_user_by_email,
    get_program_by_folder_id,
    create_program,
    list_programs_for_user,
    create_permission_request,
    list_permission_requests_for_owner,
    decide_permission_request,
)
from apps.jwt import get_current_user_email
from apps.google_drive import extract_folder_id, validate_folder_access

router = APIRouter()


@router.get("/programs/mine", response_model=List[ProgramResponse])
async def my_programs(db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    user = get_user_by_email(db, email=current_email)
    return list_programs_for_user(db, user_id=user.id)


@router.post("/programs/", response_model=ProgramResponse)
async def create_program_route(payload: ProgramCreate, db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    user = get_user_by_email(db, email=current_email)
    folder_id = extract_folder_id(payload.folder_link_or_id)
    if not folder_id:
        raise HTTPException(status_code=400, detail="ID o link de carpeta inválido")

    # Check if program already exists for that folder
    existing = get_program_by_folder_id(db, folder_id)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Este programa ya existe. Solicita acceso para unirte.")

    # Validate access against Google Drive using stored token
    if not user.google_access_token:
        raise HTTPException(status_code=400, detail="Tu cuenta no tiene permiso de Drive. Vuelve a iniciar sesión otorgando permisos de Drive.")

    ok, folder_name = await validate_folder_access(user.google_access_token, folder_id)
    if not ok:
        raise HTTPException(status_code=400, detail="No se puede acceder a la carpeta de Drive o no es una carpeta.")

    program = create_program(
        db,
        creator_user_id=user.id,
        folder_id=folder_id,
        folder_name=folder_name,
        internal_code=payload.internal_code,
        name=payload.name,
        main_client=payload.main_client,
        main_beneficiaries=payload.main_beneficiaries,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )
    if program is None:
        raise HTTPException(status_code=409, detail="Ya existe un programa para esa carpeta.")
    return program


@router.post("/programs/request-access", response_model=PermissionRequestResponse)
async def request_access(payload: PermissionRequestCreate, db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    user = get_user_by_email(db, email=current_email)

    # Resolver program_id si viene folder_link_or_id
    program_id = payload.program_id
    if program_id is None and payload.folder_link_or_id:
        folder_id = extract_folder_id(payload.folder_link_or_id)
        if not folder_id:
            raise HTTPException(status_code=400, detail="ID o link de carpeta inválido")
        existing = get_program_by_folder_id(db, folder_id)
        if existing is None:
            raise HTTPException(status_code=404, detail="No existe un programa para esa carpeta")
        program_id = existing.id

    if program_id is None:
        raise HTTPException(status_code=400, detail="Debes enviar program_id o folder_link_or_id")

    pr = create_permission_request(db, program_id=program_id, requester_user_id=user.id, message=payload.message)
    if pr is None:
        raise HTTPException(status_code=400, detail="Ya tienes acceso o tu solicitud no es válida.")
    return pr


@router.get("/programs/requests", response_model=List[PermissionRequestResponse])
async def list_requests_for_owner(db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    user = get_user_by_email(db, email=current_email)
    return list_permission_requests_for_owner(db, owner_user_id=user.id)


@router.post("/programs/requests/{request_id}/approve", response_model=PermissionRequestResponse)
async def approve_request(request_id: int, db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    user = get_user_by_email(db, email=current_email)
    pr = decide_permission_request(db, request_id=request_id, approver_user_id=user.id, approve=True)
    if pr is None:
        raise HTTPException(status_code=400, detail="No se pudo aprobar la solicitud")
    return pr


@router.post("/programs/requests/{request_id}/reject", response_model=PermissionRequestResponse)
async def reject_request(request_id: int, db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    user = get_user_by_email(db, email=current_email)
    pr = decide_permission_request(db, request_id=request_id, approver_user_id=user.id, approve=False)
    if pr is None:
        raise HTTPException(status_code=400, detail="No se pudo rechazar la solicitud")
    return pr
