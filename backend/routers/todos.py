from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select, update
from typing import List
from database import get_async_session
from models.todo import Todo, TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
from models.user import User
from utils.auth import get_current_user


router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get("/", response_model=TodoListResponse)
async def get_todos(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    """
    Get all todos for the current user
    """
    user_id = int(current_user["user_id"])

    try:
        # Query todos that belong to the current user
        result = await session.execute(
            select(Todo).where(Todo.user_id == user_id)
        )
        todos = result.scalars().all()

        # Convert to response objects
        todo_responses = []
        for todo in todos:
            todo_response = TodoResponse(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                status=todo.status,
                user_id=todo.user_id,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
            todo_responses.append(todo_response)

        return TodoListResponse(todos=todo_responses, total_count=len(todo_responses))
    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching todos: {str(e)}")
        # Return empty response instead of crashing
        return TodoListResponse(todos=[], total_count=0)


@router.post("/", response_model=TodoResponse)
async def create_todo(
    todo: TodoCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    """
    Create a new todo for the current user
    """
    user_id = int(current_user["user_id"])

    try:
        # Create new todo associated with the current user
        db_todo = Todo(
            title=todo.title,
            description=todo.description,
            status=todo.status,
            user_id=user_id
        )

        session.add(db_todo)
        await session.commit()
        await session.refresh(db_todo)

        return TodoResponse(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            status=db_todo.status,
            user_id=db_todo.user_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at
        )
    except Exception as e:
        await session.rollback()
        print("Error creating todo:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create todo: {str(e)}"
        )


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    """
    Get a specific todo by ID, ensuring it belongs to the current user
    """
    user_id = int(current_user["user_id"])

    # Query the specific todo that belongs to the current user
    result = await session.execute(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    )
    todo = result.first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to you"
        )

    todo = todo[0]  # Extract todo from tuple

    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        status=todo.status,
        user_id=todo.user_id,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    """
    Update a specific todo by ID, ensuring it belongs to the current user
    """
    user_id = int(current_user["user_id"])

    # Check if the todo exists and belongs to the current user
    result = await session.execute(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    )
    existing_todo = result.first()

    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to you"
        )

    existing_todo = existing_todo[0]  # Extract todo from tuple

    # Update the todo with the provided fields
    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_todo, field, value)

    await session.commit()
    await session.refresh(existing_todo)

    return TodoResponse(
        id=existing_todo.id,
        title=existing_todo.title,
        description=existing_todo.description,
        status=existing_todo.status,
        user_id=existing_todo.user_id,
        created_at=existing_todo.created_at,
        updated_at=existing_todo.updated_at
    )


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    """
    Delete a specific todo by ID, ensuring it belongs to the current user
    """
    user_id = int(current_user["user_id"])

    # Check if the todo exists and belongs to the current user
    result = await session.execute(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    )
    todo_to_delete = result.first()

    if not todo_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to you"
        )

    todo_to_delete = todo_to_delete[0]  # Extract todo from tuple

    await session.delete(todo_to_delete)
    await session.commit()

    return {"message": "Todo deleted successfully"}