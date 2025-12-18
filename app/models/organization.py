"""Organization model for trade unions."""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Organization(Base):
    """Organization (trade union) model."""

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    sector = Column(String(100))  # e.g., "Santé", "Industrie", etc.
    logo_url = Column(String(500))
    color_scheme = Column(String(7))  # Hex color code, e.g., "#FF0000"
    description = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaigns = relationship("Campaign", back_populates="organization", cascade="all, delete-orphan")
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"
