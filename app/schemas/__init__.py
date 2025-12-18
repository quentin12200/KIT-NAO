"""Schemas package."""
from app.schemas.organization import (
    OrganizationBase,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
)
from app.schemas.campaign import (
    CampaignBase,
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignListResponse,
)
from app.schemas.document import (
    DocumentGenerate,
    DocumentResponse,
    DocumentListResponse,
)
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
)
from app.schemas.auth import Token, TokenData

__all__ = [
    "OrganizationBase",
    "OrganizationCreate",
    "OrganizationUpdate",
    "OrganizationResponse",
    "CampaignBase",
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignResponse",
    "CampaignListResponse",
    "DocumentGenerate",
    "DocumentResponse",
    "DocumentListResponse",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
]
