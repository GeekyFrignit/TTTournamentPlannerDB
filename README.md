# Tournament Planner API

A Python REST API built with FastAPI and SQLite for managing tournament planning data with HTTP Basic Authentication and CORS support.

## Features

- **REST API**: Full CRUD operations for tournament plans
- **SQLite Database**: Lightweight, file-based database with WAL mode for consistency
- **Basic Authentication**: HTTP Basic Auth with auto-generated credentials
- **CORS Support**: Enabled for Node.js middleware access
- **Binary Icon Storage**: Support for storing tournament icons as binary blobs
- **Interactive API Documentation**: Auto-generated with Swagger UI at `/docs`

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd TTTournamentPlannerDB
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/macOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install development dependencies (optional):
```bash
pip install -r requirements-dev.txt
```

## Configuration

### Generate API Credentials

The project uses auto-generated credentials stored in the `.env` file. To generate new credentials:

```bash
python generate_credentials.py
```

This will create a `.env` file with:
- `API_USERNAME`: A randomly generated username (format: m followed by 5 digits)
- `API_PASSWORD`: A randomly generated 16-character password
- `API_PASSWORD_HASH`: Bcrypt hash of the password (for verification)
- `DATABASE_URL`: SQLite database connection string

**Important**: Keep the `.env` file secure and do not commit it to version control. Use `.env.example` as a template.

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

All API endpoints require HTTP Basic Authentication. Include credentials in request headers:

```bash
curl -u "m12345:your_password" http://localhost:8000/api/tournament-plans
```

Or with Python requests:

```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    'http://localhost:8000/api/tournament-plans',
    auth=HTTPBasicAuth('m12345', 'your_password')
)
```

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app
```

Run tests in verbose mode:

```bash
pytest -v
```

## Code Quality

Format code with Black:

```bash
black .
```

Check code quality with Flake8:

```bash
flake8 app tests
```

## Project Structure

```
TTTournamentPlannerDB/
├── app/                     # Main application package
│   ├── __init__.py
│   ├── main.py             # FastAPI application entry point
│   ├── database.py         # Database configuration and session management
│   ├── models.py           # SQLAlchemy models
│   └── routers/            # API route handlers
│       └── __init__.py
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures
│   └── test_*.py           # Test modules
├── .env                     # Environment variables (auto-generated, not in git)
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore patterns
├── generate_credentials.py # Credential generation utility
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md               # This file
```

## Environment Variables

The application uses the following environment variables (defined in `.env`):

- `API_USERNAME`: Basic auth username
- `API_PASSWORD`: Basic auth password (plain text)
- `API_PASSWORD_HASH`: Bcrypt hash of the password
- `DATABASE_URL`: SQLite database connection string

## Database

The application uses SQLite for data persistence. The database file (`tournament_planner.db`) will be created automatically in the project root when the application starts.

Database features:
- WAL (Write-Ahead Logging) mode for concurrent access
- Foreign key constraints enabled
- Automatic schema creation on startup

## API Endpoints

### Tournament Plans

- `GET /api/tournament-plans` - Get all tournament plans
- `GET /api/tournament-plans/{id}` - Get a specific tournament plan
- `POST /api/tournament-plans` - Create a new tournament plan
- `PUT /api/tournament-plans/{id}` - Update a tournament plan
- `DELETE /api/tournament-plans/{id}` - Delete a tournament plan

All endpoints require HTTP Basic Authentication.

## Development

### Code Standards

- Python 3.10+
- PEP 8 compliant (enforced by Flake8)
- Code formatted with Black
- Type hints recommended

### Running Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-restart on code changes.

## Troubleshooting

### Database Errors
If you encounter database issues, delete `tournament_planner.db` and any `.db-shm` or `.db-wal` files and restart the application to recreate the database schema.

### Import Errors
Ensure you've activated the virtual environment and installed all dependencies from `requirements.txt`.

### Port Already in Use
If port 8000 is already in use, specify a different port:

```bash
uvicorn app.main:app --reload --port 8001
```

## License

See LICENSE file for details.
