"""Error handling and logging infrastructure for the agent"""
import logging
from typing import Dict, Any
from functools import wraps


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_agent_errors(func):
    """Decorator to handle errors in agent functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "An error occurred while processing your request. Please try again."
            }
    return wrapper


class AgentErrorHandler:
    """Class for handling various types of errors in the agent"""
    
    @staticmethod
    def handle_tool_call_error(tool_name: str, error: Exception) -> Dict[str, Any]:
        """Handle errors that occur during tool calls"""
        logger.error(f"Error calling tool {tool_name}: {str(error)}")
        return {
            "success": False,
            "tool_name": tool_name,
            "error": str(error),
            "message": f"Sorry, I couldn't perform the {tool_name} operation. Please try again."
        }
    
    @staticmethod
    def handle_invalid_input_error(input_data: str) -> Dict[str, Any]:
        """Handle errors due to invalid input"""
        logger.warning(f"Invalid input received: {input_data}")
        return {
            "success": False,
            "error": "Invalid input",
            "message": "I didn't understand your request. Could you please rephrase it?"
        }
    
    @staticmethod
    def handle_missing_parameter_error(param_name: str, tool_name: str) -> Dict[str, Any]:
        """Handle errors due to missing parameters"""
        logger.warning(f"Missing parameter {param_name} for tool {tool_name}")
        return {
            "success": False,
            "error": f"Missing parameter: {param_name}",
            "message": f"The {tool_name} operation requires a {param_name}. Please provide it."
        }
    
    @staticmethod
    def handle_resource_not_found(resource_type: str, identifier: str) -> Dict[str, Any]:
        """Handle errors when a requested resource is not found"""
        logger.info(f"{resource_type} with identifier {identifier} not found")
        return {
            "success": False,
            "error": f"{resource_type} not found",
            "message": f"I couldn't find the {resource_type} you're looking for."
        }


# Global error handler instance
error_handler = AgentErrorHandler()