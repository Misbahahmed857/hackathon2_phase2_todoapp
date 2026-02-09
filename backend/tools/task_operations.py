from mcp import Server
from backend.database import (
    create_task, get_all_tasks, get_task_by_id, 
    update_task, complete_task, delete_task
)
from backend.models.task_model import TaskUpdate
from backend.utils.error_handlers import validate_task_title, validate_task_description
from backend.server_config import (
    server, TaskRequest, TaskUpdateRequest, TaskIdRequest, 
    TaskResponse, TaskListResponse, DeleteResponse
)
from sqlmodel import create_engine, Session
from backend.config import settings
import json


# Create database engine
engine = create_engine(settings.database_url)


@server.call("add_task")
def add_task_tool(request: TaskRequest) -> TaskResponse:
    """MCP tool to add a new task"""
    # Validate input
    if not validate_task_title(request.title):
        return TaskResponse(
            success=False,
            message="Title is required and must be between 1 and 255 characters"
        )
    
    if not validate_task_description(request.description):
        return TaskResponse(
            success=False,
            message="Description must be between 0 and 1000 characters if provided"
        )
    
    # Create database session
    with Session(engine) as session:
        try:
            # Create the task
            task = create_task(session, request.title, request.description)
            
            # Convert task to dictionary for response
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            }
            
            return TaskResponse(success=True, task=task_dict, message="Task created successfully")
        
        except Exception as e:
            return TaskResponse(success=False, message=f"Error creating task: {str(e)}")


@server.call("list_tasks")
def list_tasks_tool() -> TaskListResponse:
    """MCP tool to list all tasks"""
    with Session(engine) as session:
        try:
            tasks = get_all_tasks(session)
            
            # Convert tasks to dictionaries
            task_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None
                }
                task_list.append(task_dict)
            
            return TaskListResponse(
                success=True, 
                tasks=task_list, 
                count=len(task_list),
                message="Tasks retrieved successfully"
            )
        
        except Exception as e:
            return TaskListResponse(
                success=False, 
                tasks=[], 
                count=0,
                message=f"Error retrieving tasks: {str(e)}"
            )


@server.call("update_task")
def update_task_tool(request: TaskUpdateRequest) -> TaskResponse:
    """MCP tool to update a task"""
    # Validate input
    if request.id <= 0:
        return TaskResponse(
            success=False,
            message="Task ID must be a positive integer"
        )
    
    if request.title is not None and not validate_task_title(request.title):
        return TaskResponse(
            success=False,
            message="Title must be between 1 and 255 characters if provided"
        )
    
    if not validate_task_description(request.description):
        return TaskResponse(
            success=False,
            message="Description must be between 0 and 1000 characters if provided"
        )
    
    with Session(engine) as session:
        try:
            # Check if task exists
            existing_task = get_task_by_id(session, request.id)
            if not existing_task:
                return TaskResponse(
                    success=False,
                    message=f"Task with id {request.id} not found"
                )
            
            # Prepare update data
            task_update = TaskUpdate(
                title=request.title,
                description=request.description
            )
            
            # Update the task
            updated_task = update_task(session, request.id, task_update)
            
            if updated_task:
                # Convert task to dictionary for response
                task_dict = {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "status": updated_task.status.value,
                    "created_at": updated_task.created_at.isoformat(),
                    "completed_at": updated_task.completed_at.isoformat() if updated_task.completed_at else None
                }
                
                return TaskResponse(
                    success=True, 
                    task=task_dict, 
                    message="Task updated successfully"
                )
            else:
                return TaskResponse(
                    success=False,
                    message=f"Failed to update task with id {request.id}"
                )
        
        except Exception as e:
            return TaskResponse(success=False, message=f"Error updating task: {str(e)}")


@server.call("complete_task")
def complete_task_tool(request: TaskIdRequest) -> TaskResponse:
    """MCP tool to mark a task as completed"""
    if request.id <= 0:
        return TaskResponse(
            success=False,
            message="Task ID must be a positive integer"
        )
    
    with Session(engine) as session:
        try:
            # Check if task exists
            existing_task = get_task_by_id(session, request.id)
            if not existing_task:
                return TaskResponse(
                    success=False,
                    message=f"Task with id {request.id} not found"
                )
            
            # Complete the task
            completed_task = complete_task(session, request.id)
            
            if completed_task:
                # Convert task to dictionary for response
                task_dict = {
                    "id": completed_task.id,
                    "title": completed_task.title,
                    "description": completed_task.description,
                    "status": completed_task.status.value,
                    "created_at": completed_task.created_at.isoformat(),
                    "completed_at": completed_task.completed_at.isoformat() if completed_task.completed_at else None
                }
                
                return TaskResponse(
                    success=True, 
                    task=task_dict, 
                    message="Task completed successfully"
                )
            else:
                return TaskResponse(
                    success=False,
                    message=f"Failed to complete task with id {request.id}"
                )
        
        except Exception as e:
            return TaskResponse(success=False, message=f"Error completing task: {str(e)}")


@server.call("delete_task")
def delete_task_tool(request: TaskIdRequest) -> DeleteResponse:
    """MCP tool to delete a task"""
    if request.id <= 0:
        return DeleteResponse(message="Task ID must be a positive integer", success=False)
    
    with Session(engine) as session:
        try:
            # Check if task exists
            existing_task = get_task_by_id(session, request.id)
            if not existing_task:
                return DeleteResponse(
                    success=False,
                    message=f"Task with id {request.id} not found"
                )
            
            # Delete the task
            deleted = delete_task(session, request.id)
            
            if deleted:
                return DeleteResponse(
                    success=True,
                    message=f"Task with id {request.id} deleted successfully"
                )
            else:
                return DeleteResponse(
                    success=False,
                    message=f"Failed to delete task with id {request.id}"
                )
        
        except Exception as e:
            return DeleteResponse(success=False, message=f"Error deleting task: {str(e)}")