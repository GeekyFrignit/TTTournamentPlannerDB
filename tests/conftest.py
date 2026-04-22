"""
Pytest configuration and fixtures for database testing.
"""
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.database import Base


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
