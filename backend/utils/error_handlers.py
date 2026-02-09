from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime


class TaskNotFoundError(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


class ValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )


def handle_error(error_msg: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    """Generic error handler"""
    raise HTTPException(status_code=status_code, detail=error_msg)


def validate_task_title(title: str) -> bool:
    """Validate task title"""
    if not title or len(title.strip()) == 0:
        return False
    if len(title) > 255:
        return False
    return True


def validate_task_description(description: Optional[str]) -> bool:
    """Validate task description"""
    if description is None:
        return True
    if len(description) > 1000:
        return False
    return True