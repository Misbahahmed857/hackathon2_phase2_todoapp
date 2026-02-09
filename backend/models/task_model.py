from datetime import datetime
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)


class Task(TaskBase, table=True):
    """
    Task entity representing a unit of work with properties like ID, title, 
    description, status (pending/completed), creation timestamp, and completion timestamp
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(default=None)


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    completed_at: Optional[datetime] = Field(default=None)