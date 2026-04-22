"""
Test database connection and TournamentPlan model.
Following TDD: tests written first, will fail initially.
"""
import pytest
from datetime import datetime
from sqlalchemy import inspect, text
from app.database import engine, SessionLocal, Base
from app.models import TournamentPlan


class TestDatabaseConnection:
    """Test database engine creation and connectivity."""

    def test_database_connection(self):
        """Verify database engine can be created and is accessible."""
        # Test that engine exists and is not None
        assert engine is not None
        
        # Test that we can execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result is not None


class TestTournamentPlanModel:
    """Test TournamentPlan model structure and functionality."""

    def test_create_tournament_plan_model(self, db_session):
        """Verify TournamentPlan model can be instantiated."""
        plan = TournamentPlan(
            name="Test Tournament",
            welcome_message="Welcome!",
            icon=b"icon_data"
        )
        assert plan is not None
        assert isinstance(plan, TournamentPlan)

    def test_tournament_plan_model_fields(self):
        """Verify TournamentPlan has all required fields with correct types."""
        # Get the mapper for the model
        mapper = inspect(TournamentPlan)
        columns = mapper.columns
        
        # Check that all required fields exist
        assert "id" in columns
        assert "name" in columns
        assert "welcome_message" in columns
        assert "icon" in columns
        assert "created_at" in columns
        assert "updated_at" in columns
        
        # Check field types
        assert columns["id"].primary_key is True
        assert columns["name"].nullable is False
        assert columns["welcome_message"].nullable is True
        assert columns["icon"].nullable is True
        assert columns["created_at"].nullable is False
        assert columns["updated_at"].nullable is False

    def test_tournament_plan_name_mandatory(self, db_session):
        """Verify name field is required (NOT NULL constraint)."""
        # Create a plan without a name
        plan = TournamentPlan(
            welcome_message="Welcome!",
            icon=None
        )
        db_session.add(plan)
        
        # Should raise an error when trying to commit
        with pytest.raises(Exception):  # Will be IntegrityError
            db_session.commit()

    def test_database_session(self, db_session):
        """Verify session creation and cleanup works."""
        # Test that session exists and is usable
        assert db_session is not None
        
        # Test that we can create and save a TournamentPlan
        plan = TournamentPlan(
            name="Session Test Tournament",
            welcome_message="Testing session",
            icon=None
        )
        db_session.add(plan)
        db_session.commit()
        
        # Verify it was saved
        assert plan.id is not None
        
        # Test that we can query it back
        retrieved = db_session.query(TournamentPlan).filter(
            TournamentPlan.id == plan.id
        ).first()
        assert retrieved is not None
        assert retrieved.name == "Session Test Tournament"
        assert retrieved.welcome_message == "Testing session"
