from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

# --- Task Schemas ---

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    tasks: List[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)