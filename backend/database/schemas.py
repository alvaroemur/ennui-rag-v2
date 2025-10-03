from pydantic import BaseModel, PositiveFloat, EmailStr, validator, Field
from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict
import json


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    content: str
    created_at: datetime

class PostCreate(BaseModel):
    content: str

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


# Program schemas
class ProgramCreate(BaseModel):
    folder_link_or_id: str
    internal_code: str
    name: str
    main_client: Optional[str] = None
    main_beneficiaries: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProgramResponse(BaseModel):
    id: int
    drive_folder_id: str
    drive_folder_name: Optional[str]
    internal_code: str
    name: str
    main_client: Optional[str]
    main_beneficiaries: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    class Config:
        orm_mode = True


class PermissionRequestCreate(BaseModel):
    program_id: Optional[int] = None
    folder_link_or_id: Optional[str] = None
    message: Optional[str] = None


class PermissionRequestResponse(BaseModel):
    id: int
    program_id: int
    requester_user_id: int
    status: str
    message: Optional[str]
    created_at: datetime
    decided_at: Optional[datetime]
    decided_by_user_id: Optional[int]

    class Config:
        orm_mode = True


class DriveCheckResponse(BaseModel):
    folder_id: str
    ok: bool
    folder_name: Optional[str]
    exists_program: bool
    program: Optional[ProgramResponse] = None


# Program Configuration Schemas

class ProgramPhaseBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    order_index: int = 0

class ProgramPhaseCreate(ProgramPhaseBase):
    pass

class ProgramPhaseUpdate(ProgramPhaseBase):
    pass

class ProgramPhaseResponse(ProgramPhaseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ProgramScopeBase(BaseModel):
    general_objective: Optional[str] = None
    specific_objectives: Optional[List[str]] = None

class ProgramScopeCreate(ProgramScopeBase):
    phases: Optional[List[ProgramPhaseCreate]] = []

class ProgramScopeUpdate(ProgramScopeBase):
    phases: Optional[List[ProgramPhaseUpdate]] = []

class ProgramScopeResponse(ProgramScopeBase):
    id: int
    program_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    phases: List[ProgramPhaseResponse] = []

    class Config:
        orm_mode = True


class TheoryOfChangeProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_quantity: int = 0
    order_index: int = 0

class TheoryOfChangeProductCreate(TheoryOfChangeProductBase):
    pass

class TheoryOfChangeProductUpdate(TheoryOfChangeProductBase):
    pass

class TheoryOfChangeProductResponse(TheoryOfChangeProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class TheoryOfChangeResultBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_percentage: float = Field(0.0, ge=0.0, le=100.0)
    timeframe: Optional[str] = None
    order_index: int = 0

class TheoryOfChangeResultCreate(TheoryOfChangeResultBase):
    pass

class TheoryOfChangeResultUpdate(TheoryOfChangeResultBase):
    pass

class TheoryOfChangeResultResponse(TheoryOfChangeResultBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class TheoryOfChangeImpactBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_percentage: float = Field(0.0, ge=0.0, le=100.0)
    timeframe: Optional[str] = None
    order_index: int = 0

class TheoryOfChangeImpactCreate(TheoryOfChangeImpactBase):
    pass

class TheoryOfChangeImpactUpdate(TheoryOfChangeImpactBase):
    pass

class TheoryOfChangeImpactResponse(TheoryOfChangeImpactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class TheoryOfChangeBase(BaseModel):
    pass

class TheoryOfChangeCreate(TheoryOfChangeBase):
    products: Optional[List[TheoryOfChangeProductCreate]] = []
    results: Optional[List[TheoryOfChangeResultCreate]] = []
    impacts: Optional[List[TheoryOfChangeImpactCreate]] = []

class TheoryOfChangeUpdate(TheoryOfChangeBase):
    products: Optional[List[TheoryOfChangeProductUpdate]] = []
    results: Optional[List[TheoryOfChangeResultUpdate]] = []
    impacts: Optional[List[TheoryOfChangeImpactUpdate]] = []

class TheoryOfChangeResponse(TheoryOfChangeBase):
    id: int
    program_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    products: List[TheoryOfChangeProductResponse] = []
    results: List[TheoryOfChangeResultResponse] = []
    impacts: List[TheoryOfChangeImpactResponse] = []

    class Config:
        orm_mode = True


class ProgramConfigurationResponse(BaseModel):
    """Complete program configuration including all related data"""
    program: ProgramResponse
    scope: Optional[ProgramScopeResponse] = None
    theory_of_change: Optional[TheoryOfChangeResponse] = None

    class Config:
        orm_mode = True


# Session schemas
class SessionCreate(BaseModel):
    access_token: str
    refresh_token: str
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    expires_at: datetime


class SessionResponse(BaseModel):
    session_id: str
    user_id: int
    access_token: str
    refresh_token: str
    user_agent: Optional[str]
    ip_address: Optional[str]
    created_at: datetime
    last_accessed: datetime
    expires_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class SessionValidationResponse(BaseModel):
    valid: bool
    user_email: Optional[str] = None
    access_token: Optional[str] = None
    message: Optional[str] = None


# Indexed File Schemas
class IndexedFileBase(BaseModel):
    drive_file_id: str
    drive_file_name: str
    file_type: str
    file_size: int = 0
    web_view_link: Optional[str] = None
    description: Optional[str] = None
    parents: Optional[str] = None  # JSON string
    owners: Optional[str] = None  # JSON string
    last_modifying_user: Optional[str] = None  # JSON string
    md5_checksum: Optional[str] = None
    is_google_doc: bool = False
    is_downloadable: bool = True

class IndexedFileCreate(IndexedFileBase):
    drive_folder_id: str
    content_text: Optional[str] = None
    summary_120w: Optional[str] = None
    keywords: Optional[str] = None  # JSON string
    topics: Optional[str] = None  # JSON string
    sentiment: Optional[str] = None
    language: Optional[str] = None
    document_type: Optional[str] = None

class IndexedFileUpdate(BaseModel):
    content_text: Optional[str] = None
    summary_120w: Optional[str] = None
    keywords: Optional[str] = None
    topics: Optional[str] = None
    sentiment: Optional[str] = None
    language: Optional[str] = None
    document_type: Optional[str] = None
    indexing_status: Optional[str] = None
    indexing_error: Optional[str] = None
    last_indexed_at: Optional[datetime] = None

class IndexedFileResponse(IndexedFileBase):
    id: int
    drive_folder_id: str
    content_text: Optional[str] = None
    summary_120w: Optional[str] = None
    keywords: Optional[str] = None
    topics: Optional[str] = None
    sentiment: Optional[str] = None
    language: Optional[str] = None
    document_type: Optional[str] = None
    indexing_status: str
    indexing_error: Optional[str] = None
    last_indexed_at: Optional[datetime] = None
    drive_created_time: Optional[datetime] = None
    drive_modified_time: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Indexing Job Schemas
class IndexingJobBase(BaseModel):
    job_type: str
    folder_id: Optional[str] = None

class IndexingJobCreate(IndexingJobBase):
    pass

class IndexingJobUpdate(BaseModel):
    status: Optional[str] = None
    total_files: Optional[int] = None
    processed_files: Optional[int] = None
    successful_files: Optional[int] = None
    failed_files: Optional[int] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class IndexingJobResponse(IndexingJobBase):
    id: int
    program_id: int
    user_id: int
    status: str
    total_files: int
    processed_files: int
    successful_files: int
    failed_files: int
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Google Drive Retrieval Schemas
class DriveScanRequest(BaseModel):
    program_id: int
    folder_id: Optional[str] = None
    include_trashed: bool = False
    job_type: str = "full_scan"  # full_scan, incremental, specific_folder

class DriveScanResponse(BaseModel):
    job_id: int
    message: str
    status: str

class IndexingStatusResponse(BaseModel):
    job_id: int
    status: str
    progress: Dict[str, int]  # total_files, processed_files, successful_files, failed_files
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class FileSearchRequest(BaseModel):
    program_id: int
    query: str
    file_types: Optional[List[str]] = None
    limit: int = 50

class FileSearchResponse(BaseModel):
    files: List[IndexedFileResponse]
    total_count: int
    query: str
