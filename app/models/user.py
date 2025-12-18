"""User model for authentication and authorization."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    CONTRIBUTOR = "contributor"
    READER = "reader"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))

    role = Column(Enum(UserRole), default=UserRole.READER)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relationships
    organization = relationship("Organization", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role={self.role})>"
