"""Base agent class for the todo management agent"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from backend.agents.config import AgentConfig
from backend.utils.mcp_client import MCPTaskClient
from backend.utils.response_formatter import (
    format_task_list_response, 
    format_add_task_response,
    format_update_task_response,
    format_complete_task_response,
    format_delete_task_response,
    format_error_response
)


class BaseAgent(ABC):
    """Abstract base class for agents"""
    
    def __init__(self):
        self.config = AgentConfig()
        self.mcp_client = MCPTaskClient()
    
    @abstractmethod
    def process_request(self, user_message: str) -> Dict[str, Any]:
        """Process a user request and return a response"""
        pass
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return the list of tool schemas available to the agent"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Creates a new task with the provided title and description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "The description of the task"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieves all tasks in the system",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Updates an existing task with the provided details",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "The ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "The new title of the task (optional)"
                            },
                            "description": {
                                "type": "string",
                                "description": "The new description of the task (optional)"
                            }
                        },
                        "required": ["id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Marks a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "The ID of the task to complete"
                            }
                        },
                        "required": ["id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Removes a task from the system",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["id"]
                    }
                }
            }
        ]