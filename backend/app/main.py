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

# Initialize TaskFlow API Application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-inspired REST API for workflow & task management",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
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
    """Root endpoint returning service identity and core links."""
    return {
        "service": settings.PROJECT_NAME,
        "status": "online",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "health_url": "/health",
        "stats_url": f"{settings.API_V1_STR}/system/stats"
    }