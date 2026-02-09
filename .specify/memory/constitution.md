<!-- SYNC IMPACT REPORT:
     Version change: N/A -> 1.0.0
     Modified principles: N/A (new constitution)
     Added sections: All sections
     Removed sections: N/A
     Templates requiring updates: N/A
     Follow-up TODOs: None
-->
# AI-Powered Todo Chatbot Constitution

## Core Principles

### Agentic-first development
All functionality must be produced strictly through the Agentic Dev Stack workflow: spec → plan → tasks → implementation via Claude Code. Manual coding, ad-hoc fixes, or direct file edits are not allowed.

### Separation of concerns
MCP tools, agent reasoning, and API orchestration must be clearly separated and implemented in independent specs.

### Stateless architecture
The server must not hold any in-memory or session-based state. All state (tasks, conversations, messages) must be persisted in the database.

### Tool-driven intelligence
The AI agent must interact with the system exclusively via MCP tools for all task-related operations.

### Natural language correctness
User intent must be accurately interpreted and mapped to the correct MCP tool behavior.

## Key Standards

### Specification fidelity
- Every implemented feature must be defined in a corresponding spec
- No implementation is allowed outside the scope of the specs

### MCP compliance
- The MCP server must use the Official MCP SDK
- All task operations must be exposed as MCP tools
- MCP tools must be stateless and database-backed

### Agent behavior correctness
- The agent must select tools based on user intent, not hardcoded rules
- Tool chaining must be used when required (e.g., list → delete)
- All task mutations must be confirmed with friendly, human-readable responses

### Persistence & reliability
- Conversations must resume correctly after server restarts
- Message history must be reconstructed from the database for each request

### Error handling
- Task not found, invalid input, and empty states must be handled gracefully
- Errors must not break conversation flow or crash the agent

## Constraints

### Specifications
- Exactly **three (3) specs** are allowed:
  - **Spec 2:** MCP Task Management Server
  - **Spec 3:** AI Agent & Tool-Oriented Behavior
  - **Spec 4:** Stateless Chat API & Persistence

### Implementation rules
- No manual code edits outside Claude Code execution
- No hidden state, in-memory caches, or global variables

### Technology stack (fixed)
- Backend: Python + FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Frontend: OpenAI ChatKit
- Authentication: Better Auth

## Success Criteria

- Users can manage todos entirely through natural language
- The AI agent correctly invokes MCP tools for all task operations
- The backend remains stateless across all requests
- Conversations persist and resume correctly after restarts
- MCP tool calls are traceable and returned in API responses
- The system functions correctly after redeployment
- The architecture demonstrates scalability, clarity, and agentic correctness

## Governance

This constitution governs all development activities for the AI-Powered Todo Chatbot project. All team members must adhere to these principles and standards. Amendments to this constitution require explicit approval from project leadership and must be documented with clear rationale.

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08