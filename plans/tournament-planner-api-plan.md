## Plan: Python REST API with SQLite and Basic Authentication

Building a FastAPI backend server with SQLite database for tournament planning, REST API for CRUD operations on Tournament Plans (name, welcome_message, icon as binary blob), and HTTP Basic Authentication with auto-generated credentials. CORS enabled for Node middleware access.

**Phases: 4 phases**

1. **Phase 1: Project Setup and Configuration**
    - **Objective:** Initialize project structure, dependencies, and configuration files with auto-generated credentials
    - **Files/Functions to Modify/Create:**
        - `.gitignore`
        - `requirements.txt` and `requirements-dev.txt`
        - `.env.example` and `.env`
        - `README.md`
        - Project structure: `app/`, `tests/`, `app/routers/` directories
        - `pytest.ini` for test configuration
        - `generate_credentials.py` utility script
    - **Tests to Write:** N/A (configuration phase)
    - **Steps:**
        1. Create project directory structure (`app/`, `tests/`, `app/routers/`)
        2. Create `.gitignore` with Python, SQLite, and environment file patterns
        3. Create `requirements.txt` with FastAPI, SQLAlchemy, passlib, uvicorn, python-multipart (for file uploads)
        4. Create `requirements-dev.txt` with pytest, httpx, black, flake8
        5. Create `generate_credentials.py` script to generate username (m + 5 random digits) and password
        6. Run script to create `.env` with API_USERNAME, API_PASSWORD, DATABASE_URL
        7. Create `.env.example` with placeholder values
        8. Create initial `README.md` with project description, setup instructions, and credentials info
        9. Create `pytest.ini` for test configuration
        10. Create empty `__init__.py` files in `app/`, `tests/`, and `app/routers/`

2. **Phase 2: Database Foundation and TournamentPlan Model**
    - **Objective:** Set up SQLAlchemy database connection and create TournamentPlan model with binary icon storage
    - **Files/Functions to Modify/Create:**
        - `app/database.py`: `get_db()`, database engine and session configuration
        - `app/models.py`: `TournamentPlan` model class with LargeBinary icon field
        - `tests/conftest.py`: `test_db()`, `test_session()` pytest fixtures
        - `tests/test_database.py`: test database connection and TournamentPlan model
    - **Tests to Write:**
        - `test_database_connection` - verify database engine creation
        - `test_create_tournament_plan_model` - verify TournamentPlan model can be instantiated
        - `test_tournament_plan_model_fields` - verify TournamentPlan has required fields (id, name[String(100)], welcome_message, icon[LargeBinary], created_at, updated_at)
        - `test_tournament_plan_name_mandatory` - verify name field is required
        - `test_database_session` - verify session creation and cleanup
    - **Steps:**
        1. Write tests for database connection and TournamentPlan model (tests will fail)
        2. Create `app/database.py` with SQLAlchemy engine, SessionLocal, and Base
        3. Configure SQLite with WAL mode and foreign keys enabled
        4. Create `app/models.py` with TournamentPlan model (id, name[String(100), nullable=False], welcome_message[Text], icon[LargeBinary], created_at, updated_at)
        5. Create `tests/conftest.py` with database fixtures for testing
        6. Run tests to verify they pass

3. **Phase 3: Basic Authentication System**
    - **Objective:** Implement HTTP Basic Authentication with config-based credentials
    - **Files/Functions to Modify/Create:**
        - `app/config.py`: Load credentials from environment variables
        - `app/auth.py`: `verify_password()`, `get_password_hash()`, `verify_credentials()`
        - `app/dependencies.py`: `get_current_username()` dependency for FastAPI
        - `tests/test_auth.py`: test authentication functions
    - **Tests to Write:**
        - `test_password_hashing` - verify password can be hashed
        - `test_password_verification` - verify correct password validates
        - `test_password_verification_fails` - verify wrong password fails
        - `test_verify_credentials_valid` - verify correct username/password returns true
        - `test_verify_credentials_invalid_username` - verify wrong username returns false
        - `test_verify_credentials_invalid_password` - verify wrong password returns false
        - `test_basic_auth_dependency` - verify FastAPI dependency works with valid credentials
        - `test_basic_auth_dependency_fails` - verify dependency raises 401 with invalid credentials
    - **Steps:**
        1. Write tests for authentication functions (tests will fail)
        2. Create `app/config.py` to load API_USERNAME and API_PASSWORD from environment
        3. Implement `get_password_hash()` and `verify_password()` using passlib bcrypt
        4. Implement `verify_credentials()` to check username and password against config
        5. Create `get_current_username()` dependency in `app/dependencies.py` that extracts Basic Auth header
        6. Run tests to verify authentication works correctly

4. **Phase 4: CRUD API Endpoints for Tournament Plans with CORS**
    - **Objective:** Create complete CRUD endpoints for tournament plans with authentication and CORS for Node middleware
    - **Files/Functions to Modify/Create:**
        - `app/schemas.py`: `TournamentPlanCreate`, `TournamentPlanUpdate`, `TournamentPlanResponse` Pydantic schemas
        - `app/crud.py`: `create_tournament_plan()`, `get_tournament_plans()`, `get_tournament_plan()`, `update_tournament_plan()`, `delete_tournament_plan()`
        - `app/routers/tournament_plans.py`: CRUD endpoints for tournament plans with multipart form support for icon upload
        - `app/main.py`: FastAPI app initialization with CORS middleware and router inclusion
        - `tests/test_tournament_plans.py`: test tournament plan CRUD operations including binary icon handling
    - **Tests to Write:**
        - `test_create_tournament_plan_with_icon` - verify authenticated request can create tournament plan with binary icon
        - `test_create_tournament_plan_without_icon` - verify tournament plan can be created without icon
        - `test_create_tournament_plan_unauthorized` - verify unauthenticated request fails with 401
        - `test_create_tournament_plan_without_name` - verify 422 when name is missing
        - `test_get_all_tournament_plans` - verify authenticated request can list tournament plans
        - `test_get_tournament_plan_by_id` - verify authenticated request can get specific tournament plan with icon
        - `test_get_tournament_plan_not_found` - verify 404 for non-existent tournament plan
        - `test_update_tournament_plan` - verify authenticated request can update tournament plan
        - `test_update_tournament_plan_icon` - verify icon can be updated with new binary data
        - `test_delete_tournament_plan` - verify authenticated request can delete tournament plan
    - **Steps:**
        1. Write tests for tournament plan CRUD endpoints including binary icon handling (tests will fail)
        2. Create TournamentPlan Pydantic schemas in `app/schemas.py` (icon as Optional[bytes] for create/update, base64 string for response)
        3. Create CRUD functions in `app/crud.py` for all tournament plan operations
        4. Create `app/routers/tournament_plans.py` with all CRUD endpoints (POST, GET, PUT, DELETE) supporting file uploads
        5. Apply `get_current_username()` dependency to all endpoints for authentication
        6. Create `app/main.py` with FastAPI app, CORS middleware (allow all origins for now), include tournament_plans router, and create database tables
        7. Run tests to verify all CRUD operations work correctly with authentication
        8. Test manually with uvicorn to ensure API works with Basic Auth headers and CORS headers
