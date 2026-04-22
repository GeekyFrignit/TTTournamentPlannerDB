"""
Pytest configuration and fixtures for database testing.
"""
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from fastapi.testclient import TestClient
from base64 import b64encode
from app.database import Base
from app.models import TournamentPlan  # Import to register model with Base
from app.config import settings


# Test database URL
TEST_DATABASE_URL = "sqlite:///./test_tournament_planner.db"


@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool  # Use NullPool for SQLite testing to avoid connection pooling
    )
    return engine


@pytest.fixture(scope="function")
def test_db(test_engine):
    """
    Create all tables, yield engine, then drop tables and cleanup.
    This ensures a clean database for each test.
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    yield test_engine
    
    # Drop all tables after test
    Base.metadata.drop_all(bind=test_engine)
    
    # Dispose of all connections to release file locks
    test_engine.dispose()
    
    # Remove test database file
    if os.path.exists("./test_tournament_planner.db"):
        try:
            os.remove("./test_tournament_planner.db")
        except PermissionError:
            # File might be locked, try again with a small delay
            import time
            time.sleep(0.1)
            try:
                os.remove("./test_tournament_planner.db")
            except PermissionError:
                pass  # Ignore if still locked


@pytest.fixture(scope="function")
def db_session(test_db):
    """
    Provide a database session for tests with automatic rollback.
    Each test gets a fresh session and data is rolled back after.
    """
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    
    # Create new session
    session = SessionLocal()
    
    try:
        yield session
    finally:
        # Rollback any uncommitted changes
        session.rollback()
        # Close the session
        session.close()


@pytest.fixture(scope="function")
def client(test_db, monkeypatch):
    """
    Create a TestClient for FastAPI app with test database.
    Uses dependency override to use test database.
    """
    # Import here to avoid circular imports
    from app.main import app
    from app import dependencies
    from sqlalchemy.orm import sessionmaker
    
    # Create all tables before tests
    Base.metadata.create_all(bind=test_db)
    
    # Create session factory for test database
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    
    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Override the get_db dependency using the function from dependencies module
    app.dependency_overrides[dependencies.get_db] = override_get_db
    
    client = TestClient(app)
    yield client
    
    # Clear overrides after test
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_headers():
    """
    Provide valid HTTP Basic Auth headers for API authentication.
    """
    username = settings.API_USERNAME
    password = "TrVOH5xHv8eIMr6b"  # Plain text password from .env
    
    credentials = b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {credentials}"}


@pytest.fixture(scope="function")
def invalid_auth_headers():
    """
    Provide invalid HTTP Basic Auth headers for testing 401 errors.
    """
    credentials = b64encode(b"invalid:wrongpassword").decode()
    return {"Authorization": f"Basic {credentials}"}


@pytest.fixture(scope="function")
def sample_tournament_plan(db_session):
    """
    Create a sample tournament plan with icon for testing.
    """
    plan = TournamentPlan(
        name="Sample Tournament Plan",
        welcome_message="Welcome to the sample tournament!",
        icon=b"sample_icon_binary_data"
    )
    db_session.add(plan)
    db_session.commit()
    db_session.refresh(plan)
    return plan


@pytest.fixture(scope="function")
def sample_tournament_plans(db_session):
    """
    Create multiple sample tournament plans for testing listing functionality.
    """
    plans = [
        TournamentPlan(
            name="Tournament One",
            welcome_message="Welcome to tournament one!",
            icon=b"icon_one_data"
        ),
        TournamentPlan(
            name="Tournament Two",
            welcome_message="Welcome to tournament two!",
            icon=b"icon_two_data"
        ),
        TournamentPlan(
            name="Tournament Three",
            welcome_message="Welcome to tournament three!",
            icon=None
        ),
    ]
    for plan in plans:
        db_session.add(plan)
    db_session.commit()
    for plan in plans:
        db_session.refresh(plan)
    return plans
