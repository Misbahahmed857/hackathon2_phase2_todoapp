import pytest
from sqlmodel import Session, create_engine
from backend.models.task_model import Task, TaskStatus
from backend.database import (
    create_task, get_all_tasks, get_task_by_id, 
    update_task, complete_task, delete_task
)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///./test_task_management.db", echo=True)
    from backend.models.task_model import SQLModel
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_task(session: Session):
    task = create_task(session, "Test Task", "This is a test task")
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.status == TaskStatus.PENDING


def test_get_all_tasks(session: Session):
    # Create a few tasks
    create_task(session, "Task 1", "Description 1")
    create_task(session, "Task 2", "Description 2")
    
    tasks = get_all_tasks(session)
    assert len(tasks) == 2


def test_get_task_by_id(session: Session):
    task = create_task(session, "Test Task", "This is a test task")
    retrieved_task = get_task_by_id(session, task.id)
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"


def test_update_task(session: Session):
    task = create_task(session, "Original Task", "Original description")
    
    from backend.models.task_model import TaskUpdate
    task_update = TaskUpdate(title="Updated Task", description="Updated description")
    updated_task = update_task(session, task.id, task_update)
    
    assert updated_task is not None
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated description"


def test_complete_task(session: Session):
    task = create_task(session, "Test Task", "This is a test task")
    completed_task = complete_task(session, task.id)
    
    assert completed_task is not None
    assert completed_task.status == TaskStatus.COMPLETED


def test_delete_task(session: Session):
    task = create_task(session, "Test Task", "This is a test task")
    deleted = delete_task(session, task.id)
    
    assert deleted is True
    
    # Verify the task is gone
    retrieved_task = get_task_by_id(session, task.id)
    assert retrieved_task is None