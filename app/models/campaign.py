"""Campaign model for NAO negotiations."""
from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON
import enum
from app.database import Base


class CampaignStatus(str, enum.Enum):
    """Campaign status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"


class Campaign(Base):
    """NAO Campaign model."""

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    title = Column(String(255), nullable=False)
    establishment_name = Column(String(255), nullable=False)
    sector = Column(String(100))
    employee_count = Column(Integer)
    collective_agreement = Column(String(100))  # e.g., "51", "66"

    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)

    # Store demands as JSON
    demands = Column(JSON)

    # Store additional context as JSON
    context = Column(JSON)

    description = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="campaigns")
    documents = relationship("Document", back_populates="campaign", cascade="all, delete-orphan")
    meetings = relationship("Meeting", back_populates="campaign", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Campaign(id={self.id}, title='{self.title}', status={self.status})>"
