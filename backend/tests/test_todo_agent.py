"""Test suite for the Todo Agent"""
import pytest
from unittest.mock import Mock, patch
from backend.agents.todo_agent import TodoAgent
from backend.utils.response_formatter import format_add_task_response


class TestTodoAgent:
    """Test cases for the TodoAgent class"""
    
    @classmethod
    def setup_class(cls):
        """Set up the test class with a mock agent"""
        # We'll mock the OpenAI client to avoid actual API calls
        cls.agent = TodoAgent()
    
    def test_process_request_add_task(self):
        """Test processing a request to add a task"""
        # Mock the OpenAI client to avoid actual API calls
        with patch.object(self.agent.config.client.beta.threads, 'create') as mock_thread_create, \
             patch.object(self.agent.config.client.beta.threads.messages, 'create') as mock_message_create, \
             patch.object(self.agent.config.client.beta.threads.runs, 'create') as mock_run_create, \
             patch.object(self.agent.config.client.beta.threads.runs, 'retrieve') as mock_run_retrieve, \
             patch.object(self.agent.config.client.beta.threads.messages, 'list') as mock_messages_list:
            
            # Set up mock return values
            mock_thread = Mock()
            mock_thread.id = "test_thread_id"
            mock_thread_create.return_value = mock_thread
            
            mock_run = Mock()
            mock_run.status = "completed"
            mock_run.id = "test_run_id"
            mock_run_create.return_value = mock_run
            mock_run_retrieve.return_value = mock_run
            
            # Mock messages list
            mock_msg_content = Mock()
            mock_msg_content.type = "text"
            mock_msg_content.text.value = "I've added your task."
            
            mock_msg = Mock()
            mock_msg.role = "assistant"
            mock_msg.content = [mock_msg_content]
            
            mock_messages_list.return_value = Mock()
            mock_messages_list.return_value.data = [mock_msg]
            
            # Test the agent
            result = self.agent.process_request("Add a task to buy groceries")
            
            # Assertions
            assert result["success"] is True
            assert "buy groceries" in result["response"].lower()
            assert result["thread_id"] == "test_thread_id"
    
    def test_process_request_list_tasks(self):
        """Test processing a request to list tasks"""
        with patch.object(self.agent.config.client.beta.threads, 'create') as mock_thread_create, \
             patch.object(self.agent.config.client.beta.threads.messages, 'create') as mock_message_create, \
             patch.object(self.agent.config.client.beta.threads.runs, 'create') as mock_run_create, \
             patch.object(self.agent.config.client.beta.threads.runs, 'retrieve') as mock_run_retrieve, \
             patch.object(self.agent.config.client.beta.threads.messages, 'list') as mock_messages_list:
            
            # Set up mock return values
            mock_thread = Mock()
            mock_thread.id = "test_thread_id"
            mock_thread_create.return_value = mock_thread
            
            mock_run = Mock()
            mock_run.status = "completed"
            mock_run.id = "test_run_id"
            mock_run_create.return_value = mock_run
            mock_run_retrieve.return_value = mock_run
            
            # Mock messages list
            mock_msg_content = Mock()
            mock_msg_content.type = "text"
            mock_msg_content.text.value = "Here are your tasks."
            
            mock_msg = Mock()
            mock_msg.role = "assistant"
            mock_msg.content = [mock_msg_content]
            
            mock_messages_list.return_value = Mock()
            mock_messages_list.return_value.data = [mock_msg]
            
            # Test the agent
            result = self.agent.process_request("Show me my tasks")
            
            # Assertions
            assert result["success"] is True
            assert "tasks" in result["response"].lower()
            assert result["thread_id"] == "test_thread_id"
    
    def test_process_request_error_handling(self):
        """Test error handling in the agent"""
        with patch.object(self.agent.config.client.beta.threads, 'create') as mock_thread_create:
            # Force an exception to test error handling
            mock_thread_create.side_effect = Exception("API Error")
            
            result = self.agent.process_request("Add a task to buy groceries")
            
            # Assertions
            assert result["success"] is False
            assert "error" in result
            assert "API Error" in result["error"]
    
    def test_get_tool_schemas(self):
        """Test that the agent returns the correct tool schemas"""
        schemas = self.agent.get_tool_schemas()
        
        # Check that we have the expected tools
        tool_names = [schema["function"]["name"] for schema in schemas]
        
        expected_tools = ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]
        for tool in expected_tools:
            assert tool in tool_names
        
        # Check that add_task has the correct schema
        add_task_schema = next((s for s in schemas if s["function"]["name"] == "add_task"), None)
        assert add_task_schema is not None
        assert "title" in add_task_schema["function"]["parameters"]["required"]