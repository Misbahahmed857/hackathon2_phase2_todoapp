import os
from typing import Optional
from openai import OpenAI


class AgentConfig:
    """Configuration class for the OpenAI Agent"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Model to use for the agent
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        
        # Timeout settings
        self.timeout = int(os.getenv("AGENT_TIMEOUT", "30"))
        
        # Maximum number of tool calls allowed in a single run
        self.max_tool_calls = int(os.getenv("MAX_TOOL_CALLS", "5"))