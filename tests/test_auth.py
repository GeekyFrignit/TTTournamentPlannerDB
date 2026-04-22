"""
Tests for authentication module.
Following TDD approach - these tests are written before implementation.
"""
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from app.auth import get_password_hash, verify_password, verify_credentials
from app.dependencies import get_current_username
from app.config import settings


@pytest.fixture
def test_credentials():
    """Fixture providing test username and password."""
    return {
        "username": "testuser",
        "password": "testpass123",
    }


@pytest.fixture
def hashed_password(test_credentials):
    """Fixture providing a hashed version of test password."""
    return get_password_hash(test_credentials["password"])


class TestPasswordHashing:
    """Tests for password hashing functionality."""

    def test_password_hashing(self, test_credentials):
        """Test that password can be hashed."""
        password = test_credentials["password"]
        hashed = get_password_hash(password)
        
        # Hash should not be the plain password
        assert hashed != password
        # Hash should be a string
        assert isinstance(hashed, str)
        # Hash should not be empty
        assert len(hashed) > 0

    def test_password_verification(self, test_credentials, hashed_password):
        """Test that correct password validates against hash."""
        password = test_credentials["password"]
        
        assert verify_password(password, hashed_password) is True

    def test_password_verification_fails(self, hashed_password):
        """Test that wrong password fails verification."""
        wrong_password = "wrongpassword"
        
        assert verify_password(wrong_password, hashed_password) is False


class TestCredentialVerification:
    """Tests for credential verification functionality."""

    def test_verify_credentials_valid(self):
        """Test that correct username/password returns True."""
        # Using credentials from .env - API_PASSWORD plain text needs to match hash
        # The .env file has: API_PASSWORD=TrVOH5xHv8eIMr6b (plain text)
        result = verify_credentials(
            username=settings.API_USERNAME,
            password="TrVOH5xHv8eIMr6b",
        )
        
        assert result is True

    def test_verify_credentials_invalid_username(self):
        """Test that wrong username returns False."""
        result = verify_credentials(
            username="wronguser",
            password="TrVOH5xHv8eIMr6b",
        )
        
        assert result is False

    def test_verify_credentials_invalid_password(self):
        """Test that wrong password returns False."""
        result = verify_credentials(
            username=settings.API_USERNAME,
            password="wrongpassword",
        )
        
        assert result is False


class TestBasicAuthDependency:
    """Tests for FastAPI Basic Auth dependency."""

    def test_basic_auth_dependency_valid(self):
        """Test that valid credentials pass through dependency."""
        credentials = HTTPBasicCredentials(
            username=settings.API_USERNAME,
            password="TrVOH5xHv8eIMr6b",
        )
        
        result = get_current_username(credentials)
        
        assert result == settings.API_USERNAME

    def test_basic_auth_dependency_fails_invalid_credentials(self):
        """Test that invalid credentials raise 401 HTTPException."""
        credentials = HTTPBasicCredentials(
            username="wronguser",
            password="wrongpass",
        )
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_username(credentials)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid credentials"
        assert "WWW-Authenticate" in exc_info.value.headers
