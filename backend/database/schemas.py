from pydantic import BaseModel, PositiveFloat, EmailStr, validator, Field
from enum import Enum
from datetime import datetime
from typing import Optional, List
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
