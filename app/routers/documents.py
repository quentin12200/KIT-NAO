"""Document routes."""
import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.campaign import Campaign
from app.models.document import Document, DocumentType, DocumentFormat
from app.models.user import User
from app.schemas.document import DocumentGenerate, DocumentResponse, DocumentListResponse
from app.utils.auth import get_current_active_user
from app.services.generator import (
    generate_letter_ouverture,
    generate_revendications,
    generate_tract,
)
from app.config import settings

router = APIRouter()


@router.post("/campaigns/{campaign_id}/generate", response_model=List[DocumentResponse])
async def generate_documents(
    campaign_id: int,
    doc_request: DocumentGenerate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Generate documents for a campaign."""
    # Get campaign
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
        )

    # Check access
    if (
        not current_user.is_superuser
        and current_user.organization_id != campaign.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this campaign",
        )

    # Create output directory
    output_dir = os.path.join(settings.UPLOAD_DIR, f"campaign_{campaign_id}")
    os.makedirs(output_dir, exist_ok=True)

    # Prepare campaign data as dict
    campaign_data = {
        "id": campaign.id,
        "title": campaign.title,
        "establishment_name": campaign.establishment_name,
        "sector": campaign.sector,
        "employee_count": campaign.employee_count,
        "collective_agreement": campaign.collective_agreement,
        "demands": campaign.demands or {},
        "organization_name": "CGT",  # TODO: Get from organization relationship
    }

    generated_docs = []

    # Generate requested documents
    for doc_type in doc_request.document_types:
        file_name = f"{doc_type.value}.{doc_request.format.value}"
        file_path = os.path.join(output_dir, file_name)

        # Generate based on type
        if doc_type == DocumentType.LETTER_OUVERTURE:
            generate_letter_ouverture(campaign_data, file_path)
        elif doc_type == DocumentType.REVENDICATIONS:
            generate_revendications(campaign_data, file_path)
        elif doc_type == DocumentType.TRACT:
            generate_tract(campaign_data, file_path)
        else:
            # Placeholder for other document types
            continue

        # Save document record to database
        doc_record = Document(
            campaign_id=campaign_id,
            type=doc_type,
            format=doc_request.format,
            title=f"{doc_type.value.replace('_', ' ').title()}",
            file_path=file_path,
        )
        db.add(doc_record)
        generated_docs.append(doc_record)

    db.commit()

    return generated_docs


@router.get("/campaigns/{campaign_id}/documents", response_model=List[DocumentListResponse])
async def list_campaign_documents(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all documents for a campaign."""
    # Get campaign
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
        )

    # Check access
    if (
        not current_user.is_superuser
        and current_user.organization_id != campaign.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this campaign",
        )

    documents = db.query(Document).filter(Document.campaign_id == campaign_id).all()
    return documents


@router.get("/{document_id}/download")
async def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Download a document."""
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Get campaign for access check
    campaign = db.query(Campaign).filter(Campaign.id == document.campaign_id).first()
    if (
        not current_user.is_superuser
        and current_user.organization_id != campaign.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to download this document",
        )

    # Check if file exists
    if not document.file_path or not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document file not found"
        )

    # Return file
    return FileResponse(
        document.file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(document.file_path),
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a document."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Get campaign for access check
    campaign = db.query(Campaign).filter(Campaign.id == document.campaign_id).first()
    if (
        not current_user.is_superuser
        and current_user.organization_id != campaign.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this document",
        )

    # Delete file if exists
    if document.file_path and os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.delete(document)
    db.commit()

    return None
