"""Main todo agent implementation using OpenAI's Assistants API"""
import json
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.utils.response_formatter import (
    format_task_list_response,
    format_add_task_response,
    format_update_task_response,
    format_complete_task_response,
    format_delete_task_response,
    format_error_response,
    format_confirmation_response
)
from backend.utils.error_handler import error_handler


class TodoAgent(BaseAgent):
    """Concrete implementation of the todo management agent"""
    
    def __init__(self):
        super().__init__()
        # Create the OpenAI assistant
        self.assistant = self.config.client.beta.assistants.create(
            name="Todo Management Assistant",
            description="An assistant that helps manage your tasks using natural language",
            model=self.config.model,
            tools=self.get_tool_schemas()
        )
    
    def process_request(self, user_message: str, thread_id: str = None) -> Dict[str, Any]:
        """Process a user request and return a response"""
        try:
            # Create or use existing thread
            if thread_id:
                thread = self.config.client.beta.threads.retrieve(thread_id)
            else:
                thread = self.config.client.beta.threads.create()
            
            # Add the user's message to the thread
            self.config.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_message
            )
            
            # Run the assistant
            run = self.config.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id
            )
            
            # Wait for the run to complete and process tool calls
            tool_calls_made = []
            response_text = ""
            
            # Poll for the run status and handle tool calls
            import time
            max_attempts = 50  # Prevent infinite loops
            attempts = 0
            
            while run.status in ["queued", "in_progress"] and attempts < max_attempts:
                time.sleep(0.5)  # Wait a bit before checking again
                run = self.config.client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                attempts += 1
            
            if run.status == "requires_action":
                # Handle tool calls
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []
                
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the appropriate tool based on the name
                    if tool_name == "add_task":
                        result = self.mcp_client.add_task(
                            title=tool_args.get("title"),
                            description=tool_args.get("description")
                        )
                    elif tool_name == "list_tasks":
                        result = self.mcp_client.list_tasks()
                    elif tool_name == "update_task":
                        result = self.mcp_client.update_task(
                            task_id=tool_args.get("id"),
                            title=tool_args.get("title"),
                            description=tool_args.get("description")
                        )
                    elif tool_name == "complete_task":
                        result = self.mcp_client.complete_task(
                            task_id=tool_args.get("id")
                        )
                    elif tool_name == "delete_task":
                        result = self.mcp_client.delete_task(
                            task_id=tool_args.get("id")
                        )
                    else:
                        result = {"success": False, "error": f"Unknown tool: {tool_name}"}
                    
                    # Store the tool call for logging
                    tool_calls_made.append({
                        "name": tool_name,
                        "arguments": tool_args,
                        "result": result,
                        "success": result.get("success", False)
                    })
                    
                    # Add to tool outputs
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(result)
                    })
                
                # Submit tool outputs
                run = self.config.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                
                # Wait for the run to complete after tool outputs
                attempts = 0
                while run.status in ["queued", "in_progress"] and attempts < max_attempts:
                    time.sleep(0.5)
                    run = self.config.client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id
                    )
                    attempts += 1
            
            # Get the messages from the thread
            messages = self.config.client.beta.threads.messages.list(
                thread_id=thread.id,
                order="asc"  # Oldest first
            )
            
            # Extract the assistant's response
            for msg in messages.data:
                if msg.role == "assistant":
                    # Get the text content
                    for content_block in msg.content:
                        if content_block.type == "text":
                            response_text = content_block.text.value
                            break
            
            # Format the final response
            if run.status == "completed":
                return {
                    "response": response_text,
                    "tool_calls": tool_calls_made,
                    "thread_id": thread.id,
                    "success": True
                }
            else:
                # Handle other statuses (failed, cancelled, expired)
                error_msg = f"Run failed with status: {run.status}"
                return {
                    "response": format_error_response(error_msg),
                    "tool_calls": tool_calls_made,
                    "thread_id": thread.id,
                    "success": False,
                    "error": error_msg
                }
                
        except Exception as e:
            return {
                "response": format_error_response(str(e)),
                "tool_calls": [],
                "thread_id": thread_id,
                "success": False,
                "error": str(e)
            }
    
    def get_assistant_id(self) -> str:
        """Get the ID of the assistant"""
        return self.assistant.id
    
    def cleanup(self):
        """Clean up the assistant when no longer needed"""
        try:
            self.config.client.beta.assistants.delete(self.assistant.id)
        except Exception:
            # Log the error but don't fail the operation
            pass