"""
FastAPI router for tournament plans CRUD operations.
Provides REST API endpoints for managing tournament plans.
"""
from typing import List, Optional
import base64
from fastapi import APIRouter, Depends, HTTPException, Form, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.schemas import TournamentPlanCreate, TournamentPlanResponse, TournamentPlanUpdate
from app.crud import (
    create_tournament_plan,
    get_tournament_plans,
    get_tournament_plan,
    update_tournament_plan,
    delete_tournament_plan
)
from app.dependencies import get_db, get_current_username

router = APIRouter(prefix="/tournament-plans", tags=["tournament-plans"])


def plan_to_response(plan, include_icon: bool = True) -> TournamentPlanResponse:
    """Convert database model to response schema with icon handling."""
    icon_str = None
    if include_icon and plan.icon:
        icon_str = base64.b64encode(plan.icon).decode()
    
    return TournamentPlanResponse(
        id=plan.id,
        name=plan.name,
        welcome_message=plan.welcome_message,
        has_icon=plan.icon is not None,
        icon=icon_str,
        created_at=plan.created_at,
        updated_at=plan.updated_at
    )


@router.post("", status_code=201, response_model=TournamentPlanResponse)
def create_plan(
    name: str = Form(...),
    welcome_message: Optional[str] = Form(None),
    icon: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
) -> TournamentPlanResponse:
    """
    Create a new tournament plan.
    
    - **name**: Tournament plan name (required, max 100 chars)
    - **welcome_message**: Welcome message (optional)
    - **icon**: Binary icon file (optional)
    
    Requires authentication via HTTP Basic Auth.
    Returns 201 Created with the new tournament plan.
    """
    # Read icon data if provided
    icon_data = None
    if icon:
        icon_data = icon.file.read()
    
    plan = create_tournament_plan(
        db=db,
        name=name,
        welcome_message=welcome_message,
        icon=icon_data
    )
    return plan_to_response(plan)


@router.get("", response_model=List[TournamentPlanResponse])
def list_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
) -> List[TournamentPlanResponse]:
    """
    List all tournament plans with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 1000)
    
    Requires authentication via HTTP Basic Auth.
    Returns list of tournament plans.
    """
    plans = get_tournament_plans(db=db, skip=skip, limit=limit)
    return [plan_to_response(plan, include_icon=False) for plan in plans]


@router.get("/{plan_id}", response_model=TournamentPlanResponse)
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
) -> TournamentPlanResponse:
    """
    Get a specific tournament plan by ID.
    
    - **plan_id**: Tournament plan ID
    
    Requires authentication via HTTP Basic Auth.
    Returns 404 if tournament plan not found.
    """
    plan = get_tournament_plan(db=db, plan_id=plan_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="Tournament plan not found")
    
    return plan_to_response(plan, include_icon=True)


@router.put("/{plan_id}", response_model=TournamentPlanResponse)
def update_plan(
    plan_id: int,
    name: Optional[str] = Form(None),
    welcome_message: Optional[str] = Form(None),
    icon: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
) -> TournamentPlanResponse:
    """
    Update a tournament plan.
    
    - **plan_id**: Tournament plan ID
    - **name**: New name (optional)
    - **welcome_message**: New welcome message (optional)
    - **icon**: New icon file (optional)
    
    Only provided fields are updated (partial updates supported).
    Requires authentication via HTTP Basic Auth.
    Returns 404 if tournament plan not found.
    """
    # Read icon data if provided
    icon_data = None
    if icon:
        icon_data = icon.file.read()
    
    plan = update_tournament_plan(
        db=db,
        plan_id=plan_id,
        name=name,
        welcome_message=welcome_message,
        icon=icon_data
    )
    
    if not plan:
        raise HTTPException(status_code=404, detail="Tournament plan not found")
    
    return plan_to_response(plan, include_icon=True)


@router.delete("/{plan_id}", status_code=204)
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
):
    """
    Delete a tournament plan.
    
    - **plan_id**: Tournament plan ID
    
    Requires authentication via HTTP Basic Auth.
    Returns 204 No Content on success.
    Returns 404 if tournament plan not found.
    """
    success = delete_tournament_plan(db=db, plan_id=plan_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Tournament plan not found")
