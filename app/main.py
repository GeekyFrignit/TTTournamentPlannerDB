"""
FastAPI application entry point.
Configures the API with CORS, middleware, and routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import tournament_plans


# Create FastAPI application
app = FastAPI(
    title="Tournament Planner API",
    version="1.0.0",
    description="API for managing tournament plans with CRUD operations"
)

# Configure CORS middleware to allow Node.js middleware and other origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Node middleware compatibility
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include tournament plans router
app.include_router(tournament_plans.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup."""
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Tournament Planner API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi_schema": "/openapi.json",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
