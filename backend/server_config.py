from mcp import Server
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json


class TaskRequest(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None


class TaskIdRequest(BaseModel):
    id: int


class TaskResponse(BaseModel):
    success: bool
    task: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


class TaskListResponse(BaseModel):
    success: bool
    tasks: List[Dict[str, Any]]
    count: int
    message: Optional[str] = None


class DeleteResponse(BaseModel):
    success: bool
    message: Optional[str] = None


# Initialize the MCP server
server = Server("mcp-task-manager")