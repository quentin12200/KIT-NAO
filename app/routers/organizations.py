"""Organization routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.organization import Organization
from app.models.user import User, UserRole
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
)
from app.utils.auth import get_current_active_user

router = APIRouter()


def check_admin_or_superuser(current_user: User):
    """Check if user is admin or superuser."""
    if not (current_user.is_superuser or current_user.role == UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Admin or superuser role required.",
        )


@router.get("/", response_model=List[OrganizationResponse])
async def list_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all organizations."""
    if current_user.is_superuser:
        # Superuser sees all organizations
        organizations = db.query(Organization).offset(skip).limit(limit).all()
    elif current_user.organization_id:
        # Regular user sees only their organization
        organizations = (
            db.query(Organization)
            .filter(Organization.id == current_user.organization_id)
            .all()
        )
    else:
        organizations = []

    return organizations


@router.post(
    "/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED
)
async def create_organization(
    org_data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new organization (superuser only)."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can create organizations",
        )

    # Check if organization already exists
    existing_org = (
        db.query(Organization).filter(Organization.name == org_data.name).first()
    )
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this name already exists",
        )

    new_org = Organization(**org_data.dict())
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    return new_org


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get an organization by ID."""
    organization = (
        db.query(Organization).filter(Organization.id == organization_id).first()
    )

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )

    # Check access
    if (
        not current_user.is_superuser
        and current_user.organization_id != organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization",
        )

    return organization


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: int,
    org_data: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update an organization."""
    organization = (
        db.query(Organization).filter(Organization.id == organization_id).first()
    )

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )

    # Only admins of the organization or superusers can update
    if not current_user.is_superuser:
        if (
            current_user.organization_id != organization_id
            or current_user.role != UserRole.ADMIN
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this organization",
            )

    # Update fields
    update_data = org_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(organization, field, value)

    db.commit()
    db.refresh(organization)

    return organization


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an organization (superuser only)."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can delete organizations",
        )

    organization = (
        db.query(Organization).filter(Organization.id == organization_id).first()
    )

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )

    db.delete(organization)
    db.commit()

    return None
