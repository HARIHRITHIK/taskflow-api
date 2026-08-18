from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.limiter import limiter
from app.models import Base
from app.database import engine
from app.routers import auth, tasks, system

# Create database tables
Base.metadata.create_all(bind=engine)

# OpenAPI Tag Metadata Specifications
openapi_tags = [
    {
        "name": "Authentication",
        "description": "User account registration, credential authentication, and JWT Bearer token issuance.",
    },
    {
        "name": "Tasks",
        "description": "Full multi-tenant task management with priority scheduling, full-text search, filtering, and soft-delete capabilities.",
    },
    {
        "name": "Operational Probes & System Metrics",
        "description": "Liveness, readiness, version info, and live operational system metrics for platform observability.",
    },
]

# Initialize TaskFlow API Application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
### TaskFlow API — Production-Inspired Work Execution Platform

TaskFlow API is a high-performance REST API platform engineered with a strict 3-tier layered architecture (`Router -> Service -> Repository`), OWASP Argon2id password security, OAuth2 JWT authentication, Alembic database migrations, and rate-limiting.

#### 🚀 Key Features:
* **OAuth2 JWT Authentication** with Argon2id cryptographic hashing.
* **Multi-Tenant User Isolation** ensuring data privacy across accounts.
* **Full CRUD Operations** with priority scheduling, search, filtering, and soft deletion.
* **Enveloped Pagination** (`items`, `total`, `page`, `page_size`, `total_pages`).
* **Operational Probes & Telemetry** (`/health`, `/ready`, `/version`, `/api/v1/system/stats`).
    """,
    version=settings.VERSION,
    openapi_tags=openapi_tags,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Hari Hrithik",
        "url": "https://github.com/HARIHRITHIK/taskflow-api",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Register Rate Limiter State & Exception Handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(system.router)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=settings.API_V1_STR)


@app.get("/", include_in_schema=False)
def root():
    """Root endpoint returning service identity and core navigation links."""
    return {
        "service": settings.PROJECT_NAME,
        "status": "online",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "health_url": "/health",
        "stats_url": f"{settings.API_V1_STR}/system/stats",
    }