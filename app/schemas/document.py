"""Pydantic schemas for Document."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.document import DocumentType, DocumentFormat


class DocumentGenerate(BaseModel):
    """Schema for generating documents."""
    document_types: list[DocumentType] = Field(
        ...,
        description="List of document types to generate"
    )
    format: DocumentFormat = DocumentFormat.DOCX


class DocumentResponse(BaseModel):
    """Schema for Document response."""
    id: int
    campaign_id: int
    type: DocumentType
    format: DocumentFormat
    title: str
    file_path: Optional[str] = None
    generated_at: datetime
    downloaded_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Schema for Document list response."""
    id: int
    type: DocumentType
    format: DocumentFormat
    title: str
    generated_at: datetime

    class Config:
        from_attributes = True
