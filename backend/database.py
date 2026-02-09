from typing import List, Optional
from sqlmodel import Session, select, func, create_engine
from datetime import datetime
from backend.models.task_model import Task, TaskUpdate, TaskStatus
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from config import settings
import asyncio


# Create synchronous engine
sync_engine = create_engine(settings.database_url)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(sync_engine)


async def create_db_and_tables_async():
    """Async version to create database tables"""
    from sqlalchemy.ext.asyncio import create_async_engine
    async_engine = create_async_engine(settings.database_url.replace("postgresql://", "postgresql+asyncpg://"))
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    await async_engine.dispose()


def create_task(session: Session, title: str, description: Optional[str] = None) -> Task:
    """Create a new task in the database"""
    task = Task(title=title, description=description, status=TaskStatus.PENDING)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_all_tasks(session: Session) -> List[Task]:
    """Retrieve all tasks from the database"""
    tasks = session.exec(select(Task)).all()
    return tasks


def get_task_by_id(session: Session, task_id: int) -> Optional[Task]:
    """Get a specific task by its ID"""
    task = session.get(Task, task_id)
    return task


def update_task(session: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """Update an existing task in the database"""
    task = session.get(Task, task_id)
    if not task:
        return None
    
    # Update fields that are provided
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def complete_task(session: Session, task_id: int) -> Optional[Task]:
    """Mark a task as completed"""
    task = session.get(Task, task_id)
    if not task:
        return None
    
    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.now()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int) -> bool:
    """Delete a task from the database"""
    task = session.get(Task, task_id)
    if not task:
        return False
    
    session.delete(task)
    session.commit()
    return True