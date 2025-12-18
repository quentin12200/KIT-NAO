"""Document model for generated NAO documents."""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class DocumentType(str, enum.Enum):
    """Document type enumeration."""
    LETTER_OUVERTURE = "lettre_ouverture"
    REVENDICATIONS = "revendications"
    MOTION_CSE = "motion_cse"
    TRACT = "tract"
    COMMUNIQUE_PRESSE = "communique_presse"
    PETITION = "petition"
    REPONSE_DIRECTION = "reponse_direction"
    ARGUMENTAIRES = "argumentaires"
    PLAN_ACTION = "plan_action"
    GUIDE_MOBILISATION = "guide_mobilisation"


class DocumentFormat(str, enum.Enum):
    """Document format enumeration."""
    DOCX = "docx"
    PDF = "pdf"
    HTML = "html"
    MARKDOWN = "markdown"


class Document(Base):
    """Generated document model."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)

    type = Column(Enum(DocumentType), nullable=False)
    format = Column(Enum(DocumentFormat), default=DocumentFormat.DOCX)
    title = Column(String(255), nullable=False)

    # Store content or file path
    content = Column(Text)  # For HTML/Markdown
    file_path = Column(String(500))  # For DOCX/PDF

    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    downloaded_at = Column(DateTime(timezone=True))

    # Relationships
    campaign = relationship("Campaign", back_populates="documents")

    def __repr__(self):
        return f"<Document(id={self.id}, type={self.type}, format={self.format})>"
