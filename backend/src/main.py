"""FastAPI application entry point.

Per spec.md: RESTful API with JSON payloads.
Per FR-022: Consistent response format with proper status codes.
Per FR-023: OpenAPI documentation via Swagger UI.
Per Constitution VIII: Backend is stateless; all session data in JWT cookies.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import create_db_and_tables
from .api.routes.auth import router as auth_router
from .api.routes.tasks import router as tasks_router

# Import models to register them with SQLModel metadata
from .models.user import User  # noqa: F401
from .models.task import Task  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    Per T048: Create database tables on startup.
    """
    # Startup: Create tables if they don't exist
    create_db_and_tables()
    yield
    # Shutdown: Nothing to do


# Create FastAPI application
# Per FR-023, T049: Configure OpenAPI documentation
app = FastAPI(
    title="Todo API",
    description="A full-stack todo application API with user authentication and task management.",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc alternative
    openapi_url="/openapi.json",
)

# Configure CORS
# Per spec.md: Frontend at localhost:3000 needs to access backend at localhost:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,  # Required for cookies
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
# Per T047: Include auth and tasks routers
app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.0.0"}


@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "api": "up",
            "database": "connected",
        },
    }
