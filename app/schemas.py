"""
Pydantic schemas for tournament plans API.
Handles request/response validation and serialization.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class TournamentPlanBase(BaseModel):
    """Base schema for tournament plan with common fields."""
    
    name: str = Field(..., max_length=100, description="Tournament plan name")
    welcome_message: Optional[str] = Field(None, description="Welcome message for the tournament")


class TournamentPlanCreate(TournamentPlanBase):
    """Schema for creating a tournament plan.
    
    Icon is handled separately via multipart form upload (File parameter in endpoint).
    """
    pass


class TournamentPlanUpdate(BaseModel):
    """Schema for updating a tournament plan.
    
    All fields are optional to allow partial updates.
    Icon is handled separately via multipart form upload.
    """
    
    name: Optional[str] = Field(None, max_length=100)
    welcome_message: Optional[str] = None


class TournamentPlanResponse(TournamentPlanBase):
    """Schema for tournament plan API responses.
    
    Includes server-managed fields like id, timestamps.
    Icon is returned as base64-encoded string for JSON compatibility.
    """
    
    id: int
    has_icon: bool = Field(..., description="Whether the plan has an icon")
    icon: Optional[str] = Field(None, description="Base64-encoded icon data")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
