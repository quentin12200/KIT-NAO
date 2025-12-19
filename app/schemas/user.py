"""Pydantic schemas for User."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """Base schema for User."""
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)
    role: Optional[UserRole] = UserRole.READER
    organization_id: Optional[int] = None


class UserCreate(UserBase):
    """Schema for creating a User."""
    password: str = Field(..., min_length=8, max_length=72)


class UserUpdate(BaseModel):
    """Schema for updating a User."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)
    role: Optional[UserRole] = None
    organization_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for User response."""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str
