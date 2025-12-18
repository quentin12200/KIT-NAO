"""Campaign routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.campaign import Campaign
from app.models.user import User
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignListResponse,
)
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[CampaignListResponse])
async def list_campaigns(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all campaigns for the user's organization."""
    query = db.query(Campaign)

    # Filter by organization if user is not superuser
    if not current_user.is_superuser and current_user.organization_id:
        query = query.filter(Campaign.organization_id == current_user.organization_id)

    campaigns = query.offset(skip).limit(limit).all()
    return campaigns


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new campaign."""
    # Verify user has access to this organization
    if (
        not current_user.is_superuser
        and current_user.organization_id != campaign_data.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create campaigns for this organization",
        )

    new_campaign = Campaign(**campaign_data.dict())
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    return new_campaign


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a campaign by ID."""
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

    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: int,
    campaign_data: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a campaign."""
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
            detail="Not authorized to modify this campaign",
        )

    # Update fields
    update_data = campaign_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)

    db.commit()
    db.refresh(campaign)

    return campaign


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a campaign."""
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
            detail="Not authorized to delete this campaign",
        )

    db.delete(campaign)
    db.commit()

    return None
