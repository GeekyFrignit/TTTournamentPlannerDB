"""
Authentication utilities for password hashing and credential verification.
Uses passlib with bcrypt for secure password handling.
"""
from passlib.context import CryptContext
from app.config import settings

# Initialize password hashing context
# Using bcrypt for production-grade password security
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against its hashed version.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password to verify against
        
    Returns:
        True if password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def verify_credentials(username: str, password: str) -> bool:
    """
    Verify username and password against configured credentials.
    
    Args:
        username: Username to verify
        password: Password to verify
        
    Returns:
        True if both username and password match configured values, False otherwise
    """
    # Check username matches
    if username != settings.API_USERNAME:
        return False
    
    # Use verify_password() with hashed password from config
    if not verify_password(password, settings.API_PASSWORD_HASH):
        return False
    
    return True
