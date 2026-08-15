from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from app.models import TaskPriority


# --- Task Schemas ---

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, json_schema_extra={"example": "Complete code review"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Review pull request for TaskFlow API service layer"})
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, json_schema_extra={"example": TaskPriority.MEDIUM.value})
    due_date: Optional[datetime] = Field(None, json_schema_extra={"example": "2026-08-30T18:00:00Z"})
    tags: Optional[str] = Field(None, json_schema_extra={"example": "backend,security"})
    is_completed: bool = Field(default=False)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedTaskResponse(BaseModel):
    """Enveloped paginated task list metadata response."""
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# --- User Schemas ---

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "johndoe"})
    email: EmailStr = Field(..., json_schema_extra={"example": "johndoe@example.com"})


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, json_schema_extra={"example": "SecurePass123!"})


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)