# Data Model: Task Entity for MCP Task Management Server

**Feature**: MCP Task Management Server
**Created**: 2026-02-08
**Related Plan**: specs/1-mcp-task-management/plan/impl-plan.md

## Task Entity

### Fields

- **id**
  - Type: Integer
  - Constraints: Primary Key, Auto-increment
  - Description: Unique identifier for each task
  
- **title**
  - Type: String(255)
  - Constraints: Required, Length 1-255 characters
  - Description: Brief title or summary of the task
  
- **description**
  - Type: String(1000)
  - Constraints: Optional, Length 0-1000 characters
  - Description: Detailed description of the task requirements
  
- **status**
  - Type: Enum (String)
  - Values: "pending", "completed"
  - Constraints: Required, Default: "pending"
  - Description: Current status of the task
  
- **created_at**
  - Type: DateTime
  - Constraints: Required, Auto-generated on creation
  - Description: Timestamp when the task was created
  
- **completed_at**
  - Type: DateTime
  - Constraints: Optional, Set when status becomes "completed"
  - Description: Timestamp when the task was marked as completed

### Validation Rules

1. **Title Validation**
   - Required field
   - Must be between 1 and 255 characters
   - Cannot be empty or whitespace only

2. **Description Validation**
   - Optional field
   - If provided, must be between 1 and 1000 characters

3. **Status Validation**
   - Required field
   - Must be one of: "pending", "completed"
   - Case-sensitive comparison

4. **Timestamp Validation**
   - created_at is automatically set on record creation
   - completed_at is set when status changes to "completed"
   - completed_at is cleared when status changes from "completed" to "pending"

### State Transitions

- **Pending to Completed**: When a task is marked as completed
  - Status changes from "pending" to "completed"
  - completed_at is set to current timestamp
  
- **Completed to Pending**: When a completed task is reopened
  - Status changes from "completed" to "pending"
  - completed_at is set to NULL

### Indexes

- Primary Index: id (automatically created)
- Status Index: status (for efficient filtering by status)

### Relationships

- No relationships with other entities required for this simple task management system