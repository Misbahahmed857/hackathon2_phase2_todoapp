"""Utilities for formatting agent responses"""
from typing import Dict, Any, List


def format_task_list_response(tasks: List[Dict[str, Any]], success: bool = True) -> str:
    """Format the response for a list of tasks"""
    if not success:
        return "Sorry, I couldn't retrieve your tasks at the moment. Please try again."
    
    if not tasks:
        return "You don't have any tasks right now."
    
    task_items = []
    for i, task in enumerate(tasks, 1):
        status = "✓" if task.get('status') == 'completed' else "○"
        task_items.append(f"{i}. {status} {task.get('title', 'Untitled Task')}")
    
    return f"Here are your tasks:\n" + "\n".join(task_items)


def format_add_task_response(task: Dict[str, Any], success: bool = True) -> str:
    """Format the response for adding a task"""
    if not success:
        return "Sorry, I couldn't add your task at the moment. Please try again."
    
    return f"I've added the task '{task.get('title', 'Untitled Task')}' for you."


def format_update_task_response(task: Dict[str, Any], success: bool = True) -> str:
    """Format the response for updating a task"""
    if not success:
        return "Sorry, I couldn't update your task at the moment. Please try again."
    
    return f"I've updated your task to '{task.get('title', 'Untitled Task')}'."


def format_complete_task_response(task: Dict[str, Any], success: bool = True) -> str:
    """Format the response for completing a task"""
    if not success:
        return "Sorry, I couldn't mark your task as completed at the moment. Please try again."
    
    return f"Great! I've marked '{task.get('title', 'Untitled Task')}' as completed."


def format_delete_task_response(task_id: int, success: bool = True) -> str:
    """Format the response for deleting a task"""
    if not success:
        return "Sorry, I couldn't delete your task at the moment. Please try again."
    
    return f"I've removed the task for you."


def format_error_response(error_msg: str) -> str:
    """Format a general error response"""
    return f"Sorry, I encountered an issue: {error_msg}. Could you please rephrase your request?"


def format_confirmation_response(action: str) -> str:
    """Format a general confirmation response"""
    return f"OK, I've {action} for you."