from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
import enum

class Priority(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int = Field(..., gt=0)
    priority: Priority = Priority.medium

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    duration_minutes: Optional[int] = Field(None, gt=0)
    priority: Optional[Priority]
    completed: Optional[bool]

class Task(TaskBase):
    id: int
    scheduled_start: Optional[datetime]
    scheduled_end: Optional[datetime]
    completed: bool

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: Optional[str]

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Stats(BaseModel):
    completion_rate: float
    missed_tasks: int
    streak: int
