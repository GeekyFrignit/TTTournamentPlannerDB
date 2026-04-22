"""
FastAPI dependencies for database and authentication.
Provides reusable dependency injections for routes.
"""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.auth import verify_credentials
from app.database import SessionLocal

# Initialize HTTP Basic Security
security = HTTPBasic()


def get_db():
    """
    Dependency function for FastAPI that yields database sessions.
    Usage in routes: def my_route(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    FastAPI dependency that authenticates using HTTP Basic Auth.
    
    Args:
        credentials: HTTPBasicCredentials extracted from Authorization header
        
    Returns:
        Authenticated username
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Verify the provided credentials
    if not verify_credentials(credentials.username, credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username
