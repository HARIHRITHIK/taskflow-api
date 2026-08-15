import math
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Task, TaskPriority
from app.schemas import TaskCreate, TaskUpdate, PaginatedTaskResponse
from app.repositories.task_repository import TaskRepository


class TaskService:
    """Service encapsulating task business logic, filtering, and user isolation enforcement."""

    def __init__(self, db: Session):
        self.task_repo = TaskRepository(db)

    def create_task(self, task_create: TaskCreate, owner_id: int) -> Task:
        """Creates a new task assigned to the specified owner."""
        return self.task_repo.create(task_create, owner_id)

    def get_user_tasks(
        self,
        owner_id: int,
        q: Optional[str] = None,
        is_completed: Optional[bool] = None,
        priority: Optional[TaskPriority] = None,
        sort_by: str = "created_at",
        order: str = "desc",
        page: int = 1,
        page_size: int = 10
    ) -> PaginatedTaskResponse:
        """Retrieves paginated, filtered, and sorted tasks wrapped in a metadata response schema."""
        priority_str = priority.value if priority else None

        tasks, total_count = self.task_repo.get_all(
            owner_id=owner_id,
            q=q,
            is_completed=is_completed,
            priority=priority_str,
            sort_by=sort_by,
            order=order,
            page=page,
            page_size=page_size
        )

        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0

        return PaginatedTaskResponse(
            items=tasks,
            total=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    def get_task_by_id(self, task_id: int, owner_id: int) -> Task:
        """Retrieves a single task by ID, enforcing user isolation."""
        task = self.task_repo.get_by_id(task_id, owner_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task

    def update_task(self, task_id: int, task_update: TaskUpdate, owner_id: int) -> Task:
        """Updates an existing task after verifying ownership."""
        task = self.get_task_by_id(task_id, owner_id)
        update_data = task_update.model_dump(exclude_unset=True)
        return self.task_repo.update(task, update_data)

    def delete_task(self, task_id: int, owner_id: int) -> Task:
        """Soft-deletes a task after verifying ownership."""
        task = self.get_task_by_id(task_id, owner_id)
        return self.task_repo.soft_delete(task)
