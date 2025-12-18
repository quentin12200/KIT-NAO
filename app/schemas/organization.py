"""Pydantic schemas for Organization."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrganizationBase(BaseModel):
    """Base schema for Organization."""
    name: str = Field(..., min_length=1, max_length=255)
    sector: Optional[str] = Field(None, max_length=100)
    logo_url: Optional[str] = Field(None, max_length=500)
    color_scheme: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    """Schema for creating an Organization."""
    pass


class OrganizationUpdate(BaseModel):
    """Schema for updating an Organization."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sector: Optional[str] = Field(None, max_length=100)
    logo_url: Optional[str] = Field(None, max_length=500)
    color_scheme: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = None


class OrganizationResponse(OrganizationBase):
    """Schema for Organization response."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
