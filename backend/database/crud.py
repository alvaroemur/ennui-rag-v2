from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timezone
from typing import Optional
from database.schemas import (
    UserCreate,
    UserUpdate,
    PostCreate,
    PostUpdate,
    PostResponse,
    ProgramCreate,
    SessionCreate,
    SessionResponse,
    SessionValidationResponse,
)
from database.models import  UserModel, PostModel, Program, ProgramAccess, PermissionRequest, UserSession
import uuid


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_users(db: Session):
    return db.query(UserModel).all()

def get_recent_users(db: Session, limit: int = 5):
    return db.query(UserModel).order_by(UserModel.id.desc()).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def upsert_user_tokens(db: Session, *, email: str, name: str, access_token: Optional[str], refresh_token: Optional[str], token_expiry: Optional[datetime]):
    user = get_user_by_email(db, email)
    if not user:
        user = UserModel(name=name, email=email)
        db.add(user)
        db.flush()
    # Update tokens if provided
    if access_token is not None:
        user.google_access_token = access_token
    if refresh_token is not None:
        user.google_refresh_token = refresh_token
    if token_expiry is not None:
        user.google_token_expiry = token_expiry
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if db_user is None:
        return None

    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email

    db.commit()
    return db_user

def get_posts(db: Session):
    return db.query(PostModel).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(PostModel).filter(PostModel.id == post_id).first()

def get_posts_by_user_id(db: Session, user_id: int):
    return db.query(PostModel).filter(PostModel.user_id == user_id).all()

def get_posts_by_user_email(db: Session, email: str):
    return db.query(PostModel).filter(PostModel.user_email == email).all()

def get_recent_posts_by_user_email(db: Session, email: str, limit: int):
    return db.query(PostModel).filter(PostModel.user_email == email).order_by(PostModel.created_at.desc()).limit(limit).all()

def create_post(db: Session, post: PostCreate):
    db_post = PostModel(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return db_post


# Program CRUD
def get_program_by_folder_id(db: Session, folder_id: str):
    return db.query(Program).filter(Program.drive_folder_id == folder_id).first()


def create_program(db: Session, *, creator_user_id: int, folder_id: str, folder_name: Optional[str],
                   internal_code: str, name: str, main_client: Optional[str],
                   main_beneficiaries: Optional[str], start_date: Optional[datetime], end_date: Optional[datetime]):
    # Ensure uniqueness by drive_folder_id at DB level; also check in code to return clearer errors
    if get_program_by_folder_id(db, folder_id):
        return None

    program = Program(
        drive_folder_id=folder_id,
        drive_folder_name=folder_name,
        internal_code=internal_code,
        name=name,
        main_client=main_client,
        main_beneficiaries=main_beneficiaries,
        start_date=start_date,
        end_date=end_date,
        created_by_user_id=creator_user_id,
    )
    db.add(program)
    db.flush()

    # Grant owner access to creator
    access = ProgramAccess(program_id=program.id, user_id=creator_user_id, role="owner", active=True)
    db.add(access)
    db.commit()
    db.refresh(program)
    return program


def list_programs_for_user(db: Session, *, user_id: int):
    return (
        db.query(Program)
        .join(ProgramAccess, ProgramAccess.program_id == Program.id)
        .filter(ProgramAccess.user_id == user_id, ProgramAccess.active.is_(True))
        .all()
    )

def list_other_programs_for_user(db: Session, *, user_id: int):
    return (
        db.query(Program)
        .outerjoin(
            ProgramAccess,
            and_(ProgramAccess.program_id == Program.id,
                 ProgramAccess.user_id == user_id,
                 ProgramAccess.active.is_(True))
        )
        .outerjoin(
            PermissionRequest,
            and_(PermissionRequest.program_id == Program.id,
                 PermissionRequest.requester_user_id == user_id)
        )
        .filter(ProgramAccess.id.is_(None))
        .filter(PermissionRequest.id.is_(None))
        .all()
    )


def get_program_by_id(db: Session, *, program_id: int, user_id: int):
    """Get a program by ID if user has access to it"""
    return (
        db.query(Program)
        .join(ProgramAccess, ProgramAccess.program_id == Program.id)
        .filter(Program.id == program_id)
        .filter(ProgramAccess.user_id == user_id)
        .filter(ProgramAccess.active.is_(True))
        .first()
    )


def create_permission_request(db: Session, *, program_id: int, requester_user_id: int, message: Optional[str]):
    # If already has access, do nothing
    existing_access = (
        db.query(ProgramAccess)
        .filter(ProgramAccess.program_id == program_id, ProgramAccess.user_id == requester_user_id)
        .first()
    )
    if existing_access:
        return None
    pr = PermissionRequest(program_id=program_id, requester_user_id=requester_user_id, message=message, status="pending")
    db.add(pr)
    db.commit()
    db.refresh(pr)
    return pr


def list_permission_requests_for_owner(db: Session, *, owner_user_id: int):
    # Requests for programs where this user is an owner
    return (
        db.query(PermissionRequest)
        .join(Program, Program.id == PermissionRequest.program_id)
        .join(ProgramAccess, (ProgramAccess.program_id == Program.id) & (ProgramAccess.user_id == owner_user_id))
        .filter(ProgramAccess.role == "owner")
        .filter(PermissionRequest.status == "pending")
        .all()
    )


def decide_permission_request(db: Session, *, request_id: int, approver_user_id: int, approve: bool):
    pr = db.query(PermissionRequest).filter(PermissionRequest.id == request_id).first()
    if not pr or pr.status != "pending":
        return None
    pr.status = "approved" if approve else "rejected"
    pr.decided_at = datetime.now(timezone.utc)
    pr.decided_by_user_id = approver_user_id
    # Grant access if approved
    if approve:
        existing_access = (
            db.query(ProgramAccess)
            .filter(ProgramAccess.program_id == pr.program_id, ProgramAccess.user_id == pr.requester_user_id)
            .first()
        )
        if not existing_access:
            db.add(ProgramAccess(program_id=pr.program_id, user_id=pr.requester_user_id, role="viewer", active=True))
    db.commit()
    db.refresh(pr)
    return pr

def update_post(db: Session, post_id: int, post: PostUpdate):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()

    if db_post is None:
        return None

    if post.content is not None:
        db_post.content = post.content

    db.commit()
    return db_post


# Session CRUD operations
def create_user_session(db: Session, *, user_id: int, session_data: SessionCreate) -> UserSession:
    """Create a new user session"""
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    # Create session
    session = UserSession(
        session_id=session_id,
        user_id=user_id,
        access_token=session_data.access_token,
        refresh_token=session_data.refresh_token,
        user_agent=session_data.user_agent,
        ip_address=session_data.ip_address,
        expires_at=session_data.expires_at,
        is_active=True
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session_by_id(db: Session, session_id: str) -> Optional[UserSession]:
    """Get session by session ID"""
    return db.query(UserSession).filter(
        UserSession.session_id == session_id,
        UserSession.is_active == True
    ).first()


def validate_session(db: Session, session_id: str) -> SessionValidationResponse:
    """Validate a session and return validation result"""
    session = get_session_by_id(db, session_id)
    
    if not session:
        return SessionValidationResponse(
            valid=False,
            message="Session not found or inactive"
        )
    
    # Check if session is expired
    if datetime.now(timezone.utc) > session.expires_at:
        # Mark session as inactive
        session.is_active = False
        db.commit()
        return SessionValidationResponse(
            valid=False,
            message="Session expired"
        )
    
    # Update last accessed time
    session.last_accessed = datetime.now(timezone.utc)
    db.commit()
    
    # Get user email
    user = get_user(db, session.user_id)
    user_email = user.email if user else None
    
    return SessionValidationResponse(
        valid=True,
        user_email=user_email,
        access_token=session.access_token
    )


def refresh_session_tokens(db: Session, session_id: str, *, 
                         new_access_token: str, new_refresh_token: str) -> bool:
    """Update session tokens"""
    session = get_session_by_id(db, session_id)
    if not session:
        return False
    
    session.access_token = new_access_token
    session.refresh_token = new_refresh_token
    session.last_accessed = datetime.now(timezone.utc)
    db.commit()
    return True


def deactivate_session(db: Session, session_id: str) -> bool:
    """Deactivate a session (logout)"""
    session = get_session_by_id(db, session_id)
    if not session:
        return False
    
    session.is_active = False
    db.commit()
    return True


def deactivate_user_sessions(db: Session, user_id: int) -> int:
    """Deactivate all sessions for a user"""
    sessions = db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == True
    ).all()
    
    for session in sessions:
        session.is_active = False
    
    db.commit()
    return len(sessions)


def cleanup_expired_sessions(db: Session) -> int:
    """Clean up expired sessions"""
    expired_sessions = db.query(UserSession).filter(
        UserSession.expires_at < datetime.now(timezone.utc),
        UserSession.is_active == True
    ).all()
    
    for session in expired_sessions:
        session.is_active = False
    
    db.commit()
    return len(expired_sessions)
