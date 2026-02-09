# Quickstart Guide: AI Agent & Tool-Oriented Behavior

**Feature**: AI Agent & Tool-Oriented Behavior
**Created**: 2026-02-08
**Related Plan**: specs/3-ai-agent-tool-behavior/plan/impl-plan.md

## Prerequisites

- Python 3.9 or higher
- pip package manager
- OpenAI API key
- Access to MCP tools from Spec 2

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install openai python-dotenv
```

### 4. Environment Configuration
Create a `.env` file with your API keys and configuration:
```env
OPENAI_API_KEY=your_openai_api_key_here
MCP_TOOL_ENDPOINT=your_mcp_tool_endpoint_here
```

### 5. Initialize the Agent
```bash
# Run the agent initialization script
python -m scripts.initialize_agent
```

### 6. Run the Agent Service
```bash
python -m agents.todo_agent
```

The agent will be available to process natural language requests and interact with the MCP tools.

## Usage Examples

### Creating a Task
```bash
User: "Add a task to buy groceries"
Agent: "I've added the task 'buy groceries' for you."
```

### Listing Tasks
```bash
User: "Show me my tasks"
Agent: "Here are your tasks: 1. buy groceries, 2. finish report"
```

### Updating a Task
```bash
User: "Change the grocery task to buy milk and bread"
Agent: "I've updated your task to 'buy milk and bread'."
```

### Completing a Task
```bash
User: "I finished buying groceries"
Agent: "Great! I've marked 'buy groceries' as completed."
```

### Deleting a Task
```bash
User: "Remove the expired task"
Agent: "I've removed the expired task for you."
```

### Tool Chaining
```bash
User: "Show me all tasks and delete the oldest one"
Agent: "Here are your tasks: 1. buy groceries, 2. finish report. I've deleted the oldest task: 'buy groceries'."
```

## Development

### Running Tests
```bash
pytest tests/agents/
```

### Code Formatting
```bash
black .
```

### Linting
```bash
flake8 .
```