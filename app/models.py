"""
SQLAlchemy ORM models for the tournament planner.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, LargeBinary, DateTime
from app.database import Base


def utc_now():
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class TournamentPlan(Base):
    """
    TournamentPlan model for storing tournament configuration and metadata.
    """
    __tablename__ = "tournament_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    welcome_message = Column(Text, nullable=True)
    icon = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    
    def __repr__(self):
        return f"<TournamentPlan(id={self.id}, name={self.name})>"
