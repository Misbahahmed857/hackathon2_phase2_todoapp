# Quickstart Guide: MCP Task Management Server

**Feature**: MCP Task Management Server
**Created**: 2026-02-08
**Related Plan**: specs/1-mcp-task-management/plan/impl-plan.md

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Access to Neon Serverless PostgreSQL database
- Official MCP SDK

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
pip install fastapi uvicorn sqlmodel python-multipart psycopg2-binary
pip install <official-mcp-sdk-package>
```

### 4. Environment Configuration
Create a `.env` file with your database connection details:
```env
DATABASE_URL=postgresql+psycopg2://username:password@host:port/database_name
```

### 5. Initialize Database
```bash
# Run database migrations or initialization script
python -m scripts.init_db
```

### 6. Run the Application
```bash
uvicorn main:app --reload
```

The MCP tools will be available at the configured endpoints.

## Usage Examples

### Adding a Task
```bash
curl -X POST http://localhost:8000/add_task \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample Task", "description": "This is a sample task"}'
```

### Listing Tasks
```bash
curl -X GET http://localhost:8000/list_tasks
```

### Updating a Task
```bash
curl -X PUT http://localhost:8000/update_task \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "title": "Updated Task Title"}'
```

### Completing a Task
```bash
curl -X POST http://localhost:8000/complete_task \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

### Deleting a Task
```bash
curl -X DELETE http://localhost:8000/delete_task \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
```

### Linting
```bash
flake8 .
```