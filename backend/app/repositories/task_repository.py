import math
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import or_, desc, asc
from sqlalchemy.orm import Session
from app.models import Task, TaskPriority
from app.schemas import TaskCreate


class TaskRepository:
    """Repository encapsulating database queries and transactions for the Task model."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, task_create: TaskCreate, owner_id: int) -> Task:
        """Creates and persists a new task record assigned to a user."""
        task_data = task_create.model_dump()
        if isinstance(task_data.get("priority"), TaskPriority):
            task_data["priority"] = task_data["priority"].value

        db_task = Task(**task_data, owner_id=owner_id)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_by_id(self, task_id: int, owner_id: int, include_deleted: bool = False) -> Optional[Task]:
        """Retrieves a single task by ID scoped to a specific owner."""
        query = self.db.query(Task).filter(
            Task.id == task_id,
            Task.owner_id == owner_id
        )
        if not include_deleted:
            query = query.filter(Task.is_deleted == False)
        return query.first()

    def get_all(
        self,
        owner_id: int,
        q: Optional[str] = None,
        is_completed: Optional[bool] = None,
        priority: Optional[str] = None,
        sort_by: str = "created_at",
        order: str = "desc",
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Task], int]:
        """
        Retrieves paginated tasks with search, filtering, and sorting support.
        Returns a tuple of (task_list, total_count).
        """
        query = self.db.query(Task).filter(
            Task.owner_id == owner_id,
            Task.is_deleted == False
        )

        # 1. Full-text search on title, description, or tags
        if q:
            search_pattern = f"%{q}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_pattern),
                    Task.description.ilike(search_pattern),
                    Task.tags.ilike(search_pattern)
                )
            )

        # 2. Filter by completion status
        if is_completed is not None:
            query = query.filter(Task.is_completed == is_completed)

        # 3. Filter by priority level
        if priority:
            query = query.filter(Task.priority == priority)

        # Total count before applying pagination limits
        total_count = query.count()

        # 4. Apply sorting
        sort_column = getattr(Task, sort_by, Task.created_at)
        if order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # 5. Apply pagination offset and limit
        offset = (page - 1) * page_size
        tasks = query.offset(offset).limit(page_size).all()

        return tasks, total_count

    def update(self, task: Task, update_data: Dict[str, Any]) -> Task:
        """Updates attributes of an existing task."""
        for key, value in update_data.items():
            if isinstance(value, TaskPriority):
                value = value.value
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def soft_delete(self, task: Task) -> Task:
        """Marks a task record as soft-deleted."""
        task.is_deleted = True
        self.db.commit()
        self.db.refresh(task)
        return task
