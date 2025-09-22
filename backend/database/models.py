from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    # Google OAuth tokens (optional)
    google_access_token = Column(String, nullable=True)
    google_refresh_token = Column(String, nullable=True)
    google_token_expiry = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    program_access = relationship("ProgramAccess", back_populates="user")
    created_programs = relationship("Program", back_populates="created_by_user")

class PostModel(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)
    user_name = Column(String, index=True)
    user_email = Column(String, index=True)
    user_id = Column(Integer, index=True)


class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True, index=True)

    # Google Drive linkage
    drive_folder_id = Column(String, unique=True, index=True)
    drive_folder_name = Column(String, nullable=True)

    # Business fields
    internal_code = Column(String, index=True)
    name = Column(String, index=True)
    main_client = Column(String, nullable=True)
    main_beneficiaries = Column(String, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)

    # Audit
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    created_by_user = relationship("UserModel", back_populates="created_programs")
    access = relationship("ProgramAccess", back_populates="program", cascade="all, delete-orphan")
    permission_requests = relationship("PermissionRequest", back_populates="program", cascade="all, delete-orphan")


class ProgramAccess(Base):
    __tablename__ = "program_access"
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, default="owner", index=True)  # owner | editor | viewer
    active = Column(Boolean, default=True)

    program = relationship("Program", back_populates="access")
    user = relationship("UserModel", back_populates="program_access")

    __table_args__ = (
        UniqueConstraint("program_id", "user_id", name="uq_program_user"),
    )


class PermissionRequest(Base):
    __tablename__ = "permission_requests"
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), index=True)
    requester_user_id = Column(Integer, ForeignKey("users.id"), index=True)
    status = Column(String, default="pending", index=True)  # pending | approved | rejected
    message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    decided_at = Column(DateTime(timezone=True), nullable=True)
    decided_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    program = relationship("Program", back_populates="permission_requests")
