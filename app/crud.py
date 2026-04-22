"""
CRUD (Create, Read, Update, Delete) operations for tournament plans.
Database operations layer between API routes and SQLAlchemy models.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import TournamentPlan


def create_tournament_plan(
    db: Session,
    name: str,
    welcome_message: Optional[str] = None,
    icon: Optional[bytes] = None
) -> TournamentPlan:
    """
    Create a new tournament plan in the database.
    
    Args:
        db: Database session
        name: Tournament plan name
        welcome_message: Optional welcome message
        icon: Optional binary icon data
        
    Returns:
        Created TournamentPlan instance
    """
    plan = TournamentPlan(
        name=name,
        welcome_message=welcome_message,
        icon=icon
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_tournament_plans(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[TournamentPlan]:
    """
    Retrieve all tournament plans with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of TournamentPlan instances
    """
    return db.query(TournamentPlan).offset(skip).limit(limit).all()


def get_tournament_plan(
    db: Session,
    plan_id: int
) -> Optional[TournamentPlan]:
    """
    Retrieve a specific tournament plan by ID.
    
    Args:
        db: Database session
        plan_id: Tournament plan ID
        
    Returns:
        TournamentPlan instance if found, None otherwise
    """
    return db.query(TournamentPlan).filter(TournamentPlan.id == plan_id).first()


def update_tournament_plan(
    db: Session,
    plan_id: int,
    name: Optional[str] = None,
    welcome_message: Optional[str] = None,
    icon: Optional[bytes] = None
) -> Optional[TournamentPlan]:
    """
    Update a tournament plan.
    
    Only updates fields that are provided (not None).
    
    Args:
        db: Database session
        plan_id: Tournament plan ID
        name: New name (optional)
        welcome_message: New welcome message (optional)
        icon: New icon data (optional, use special marker to clear icon)
        
    Returns:
        Updated TournamentPlan instance if found, None otherwise
    """
    plan = db.query(TournamentPlan).filter(TournamentPlan.id == plan_id).first()
    
    if not plan:
        return None
    
    if name is not None:
        plan.name = name
    
    if welcome_message is not None:
        plan.welcome_message = welcome_message
    
    if icon is not None:
        plan.icon = icon
    
    db.commit()
    db.refresh(plan)
    return plan


def delete_tournament_plan(
    db: Session,
    plan_id: int
) -> bool:
    """
    Delete a tournament plan.
    
    Args:
        db: Database session
        plan_id: Tournament plan ID
        
    Returns:
        True if deleted successfully, False if not found
    """
    plan = db.query(TournamentPlan).filter(TournamentPlan.id == plan_id).first()
    
    if not plan:
        return False
    
    db.delete(plan)
    db.commit()
    return True
