"""Utilities for integrating with MCP tools from Spec 2"""
import json
from typing import Dict, Any, Optional
from mcp import Client
from backend.config import settings


class MCPTaskClient:
    """Client for interacting with MCP task management tools"""
    
    def __init__(self):
        # Initialize MCP client with the appropriate configuration
        self.mcp_client = Client()
    
    def add_task(self, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Call the add_task MCP tool"""
        try:
            # Prepare the request payload
            params = {"title": title}
            if description:
                params["description"] = description
            
            # Call the MCP tool
            result = self.mcp_client.call("add_task", params)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_tasks(self) -> Dict[str, Any]:
        """Call the list_tasks MCP tool"""
        try:
            # Call the MCP tool
            result = self.mcp_client.call("list_tasks", {})
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_task(self, task_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None) -> Dict[str, Any]:
        """Call the update_task MCP tool"""
        try:
            # Prepare the request payload
            params = {"id": task_id}
            if title is not None:
                params["title"] = title
            if description is not None:
                params["description"] = description
            
            # Call the MCP tool
            result = self.mcp_client.call("update_task", params)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def complete_task(self, task_id: int) -> Dict[str, Any]:
        """Call the complete_task MCP tool"""
        try:
            # Prepare the request payload
            params = {"id": task_id}
            
            # Call the MCP tool
            result = self.mcp_client.call("complete_task", params)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Call the delete_task MCP tool"""
        try:
            # Prepare the request payload
            params = {"id": task_id}
            
            # Call the MCP tool
            result = self.mcp_client.call("delete_task", params)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}