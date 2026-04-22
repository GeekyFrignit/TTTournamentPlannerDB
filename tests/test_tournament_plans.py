"""
Tests for tournament plans CRUD API endpoints.
Following TDD: tests written first, will fail initially.
"""
import pytest
import base64
from io import BytesIO
from fastapi.testclient import TestClient
from app.config import settings


class TestTournamentPlansCreate:
    """Tests for tournament plan creation."""

    def test_create_tournament_plan_with_icon(self, client, auth_headers):
        """Verify authenticated request can create tournament plan with binary icon."""
        icon_data = b"fake_icon_binary_data"
        
        response = client.post(
            "/api/v1/tournament-plans",
            data={
                "name": "Test Tournament",
                "welcome_message": "Welcome to our tournament!"
            },
            files={"icon": ("icon.png", icon_data, "image/png")},
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Test Tournament"
        assert data["welcome_message"] == "Welcome to our tournament!"
        assert data["has_icon"] is True
        assert data["created_at"] is not None
        assert data["updated_at"] is not None

    def test_create_tournament_plan_without_icon(self, client, auth_headers):
        """Verify tournament plan can be created without icon."""
        response = client.post(
            "/api/v1/tournament-plans",
            data={
                "name": "Tournament Without Icon",
                "welcome_message": "No icon here"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Tournament Without Icon"
        assert data["welcome_message"] == "No icon here"
        assert data["has_icon"] is False

    def test_create_tournament_plan_unauthorized(self, client):
        """Verify unauthenticated request fails with 401."""
        response = client.post(
            "/api/v1/tournament-plans",
            data={
                "name": "Unauthorized Tournament",
                "welcome_message": "Should fail"
            }
        )
        
        assert response.status_code == 401

    def test_create_tournament_plan_without_name(self, client, auth_headers):
        """Verify 422 when name is missing."""
        response = client.post(
            "/api/v1/tournament-plans",
            data={
                "welcome_message": "No name provided"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 422


class TestTournamentPlansRead:
    """Tests for reading tournament plans."""

    def test_get_all_tournament_plans(self, client, auth_headers, sample_tournament_plans):
        """Verify authenticated request can list tournament plans."""
        response = client.get(
            "/api/v1/tournament-plans",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3  # Created in fixture

    def test_get_tournament_plan_by_id(self, client, auth_headers, sample_tournament_plan):
        """Verify authenticated request can get specific tournament plan with icon."""
        plan_id = sample_tournament_plan.id
        
        response = client.get(
            f"/api/v1/tournament-plans/{plan_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == plan_id
        assert data["name"] == sample_tournament_plan.name
        assert data["has_icon"] is True
        # Icon should be included as base64 if present
        assert data["icon"] is not None

    def test_get_tournament_plan_not_found(self, client, auth_headers):
        """Verify 404 for non-existent tournament plan."""
        response = client.get(
            "/api/v1/tournament-plans/9999",
            headers=auth_headers
        )
        
        assert response.status_code == 404


class TestTournamentPlansUpdate:
    """Tests for updating tournament plans."""

    def test_update_tournament_plan(self, client, auth_headers, sample_tournament_plan):
        """Verify authenticated request can update tournament plan."""
        plan_id = sample_tournament_plan.id
        
        response = client.put(
            f"/api/v1/tournament-plans/{plan_id}",
            data={
                "name": "Updated Tournament Name",
                "welcome_message": "Updated welcome message"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == plan_id
        assert data["name"] == "Updated Tournament Name"
        assert data["welcome_message"] == "Updated welcome message"

    def test_update_tournament_plan_icon(self, client, auth_headers, sample_tournament_plan):
        """Verify icon can be updated with new binary data."""
        plan_id = sample_tournament_plan.id
        new_icon_data = b"new_icon_binary_data_here"
        
        response = client.put(
            f"/api/v1/tournament-plans/{plan_id}",
            data={"name": "Same Name"},
            files={"icon": ("new_icon.png", new_icon_data, "image/png")},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["has_icon"] is True
        # Verify we can retrieve the updated icon
        assert data["icon"] is not None


class TestTournamentPlansDelete:
    """Tests for deleting tournament plans."""

    def test_delete_tournament_plan(self, client, auth_headers, sample_tournament_plan):
        """Verify authenticated request can delete tournament plan."""
        plan_id = sample_tournament_plan.id
        
        response = client.delete(
            f"/api/v1/tournament-plans/{plan_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify it's deleted - subsequent GET should return 404
        get_response = client.get(
            f"/api/v1/tournament-plans/{plan_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404
