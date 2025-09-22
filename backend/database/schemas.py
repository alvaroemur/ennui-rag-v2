from pydantic import BaseModel, PositiveFloat, EmailStr, validator, Field
from enum import Enum
from datetime import datetime
from typing import Optional, List


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
