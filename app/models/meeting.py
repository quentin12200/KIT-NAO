"""Meeting model for negotiation meetings tracking."""
from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON
from app.database import Base


class Meeting(Base):
    """Negotiation meeting model."""

    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)

    title = Column(String(255), nullable=False)
    meeting_date = Column(Date, nullable=False)
    location = Column(String(255))

    # Attendees
    union_attendees = Column(Text)  # Comma-separated or JSON
    management_attendees = Column(Text)  # Comma-separated or JSON

    # Meeting summary
    summary = Column(Text)
    union_position = Column(Text)
    management_response = Column(Text)

    # Store detailed responses as JSON
    responses = Column(JSON)

    # Next steps
    next_meeting_date = Column(Date)
    action_items = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaign = relationship("Campaign", back_populates="meetings")

    def __repr__(self):
        return f"<Meeting(id={self.id}, title='{self.title}', date={self.meeting_date})>"
