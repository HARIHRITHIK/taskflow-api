from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.models import TaskPriority
from app.database import get_db
from app.dependencies import get_current_user
from app.services.task_service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Creates a new task assigned to the authenticated user.
    """
    task_service = TaskService(db)
    return task_service.create_task(task_create, current_user.id)


@router.get("/", response_model=schemas.PaginatedTaskResponse)
def read_tasks(
    q: Optional[str] = Query(None, description="Search query matching title, description, or tags"),
    is_completed: Optional[bool] = Query(None, description="Filter by completion status (true/false)"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority level (LOW, MEDIUM, HIGH, URGENT)"),
    sort_by: str = Query("created_at", description="Field to sort by (created_at, due_date, priority, title)"),
    order: str = Query("desc", description="Sort direction ('asc' or 'desc')"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieves paginated tasks owned by the authenticated user with search, filtering, and sorting support.
    """
    task_service = TaskService(db)
    return task_service.get_user_tasks(
        owner_id=current_user.id,
        q=q,
        is_completed=is_completed,
        priority=priority,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=page_size
    )


@router.get("/{task_id}", response_model=schemas.TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieves a single task by ID owned by the authenticated user.
    """
    task_service = TaskService(db)
    return task_service.get_task_by_id(task_id, current_user.id)


@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Updates an existing task owned by the authenticated user.
    """
    task_service = TaskService(db)
    return task_service.update_task(task_id, task_update, current_user.id)


@router.delete("/{task_id}", response_model=schemas.TaskResponse)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Soft-deletes a task owned by the authenticated user.
    """
    task_service = TaskService(db)
    return task_service.delete_task(task_id, current_user.id)