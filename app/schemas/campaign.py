"""Pydantic schemas for Campaign."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date, datetime
from app.models.campaign import CampaignStatus


class CampaignBase(BaseModel):
    """Base schema for Campaign."""
    title: str = Field(..., min_length=1, max_length=255)
    establishment_name: str = Field(..., min_length=1, max_length=255)
    sector: Optional[str] = Field(None, max_length=100)
    employee_count: Optional[int] = Field(None, ge=1)
    collective_agreement: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[CampaignStatus] = CampaignStatus.DRAFT
    demands: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class CampaignCreate(CampaignBase):
    """Schema for creating a Campaign."""
    organization_id: int


class CampaignUpdate(BaseModel):
    """Schema for updating a Campaign."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    establishment_name: Optional[str] = Field(None, min_length=1, max_length=255)
    sector: Optional[str] = Field(None, max_length=100)
    employee_count: Optional[int] = Field(None, ge=1)
    collective_agreement: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[CampaignStatus] = None
    demands: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class CampaignResponse(CampaignBase):
    """Schema for Campaign response."""
    id: int
    organization_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CampaignListResponse(BaseModel):
    """Schema for Campaign list response."""
    id: int
    title: str
    establishment_name: str
    status: CampaignStatus
    start_date: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True
