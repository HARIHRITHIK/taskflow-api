import time
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.database import get_db
from app.models import User, Task

router = APIRouter(
    tags=["Operational Probes & System Metrics"]
)

# Start time tracking for uptime metric calculation
START_TIME = time.time()


@router.get("/health", summary="Liveness Probe")
def health_check():
    """
    Liveness probe verifying that the API service container process is running.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/ready", summary="Readiness Probe")
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness probe verifying live database connectivity.
    """
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connectivity check failed: {str(e)}"
        )


@router.get("/version", summary="Version Information")
def version_info():
    """
    Returns API version metadata and service identifier.
    """
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "api_prefix": settings.API_V1_STR
    }


@router.get(f"{settings.API_V1_STR}/system/stats", summary="Operational Metrics Dashboard")
def system_stats(db: Session = Depends(get_db)):
    """
    Returns operational metrics including user count, task count, completion rates, and API uptime.
    """
    total_users = db.query(User).count()
    total_tasks = db.query(Task).filter(Task.is_deleted == False).count()
    completed_tasks = db.query(Task).filter(Task.is_deleted == False, Task.is_completed == True).count()
    pending_tasks = total_tasks - completed_tasks
    uptime_seconds = round(time.time() - START_TIME, 2)

    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "uptime_seconds": uptime_seconds,
        "metrics": {
            "total_users": total_users,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate_percent": round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0.0
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
