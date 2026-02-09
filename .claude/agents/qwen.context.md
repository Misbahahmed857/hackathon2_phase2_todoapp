# Agent Context: AI Agent & Tool-Oriented Behavior

## Project Context
- Project: AI-Powered Todo Chatbot using MCP, OpenAI Agents SDK, and Stateless Architecture
- Current Feature: AI Agent & Tool-Oriented Behavior (Spec 3)
- Previous Feature: MCP Task Management Server (Spec 2)
- Next Feature: Stateless Chat API & Persistence (Spec 4)

## AI Agent & Tool-Oriented Behavior Details
- Purpose: Interpret natural language and invoke MCP tools correctly
- Architecture: OpenAI Agent using OpenAI Agents SDK for natural language processing
- Integration: Connects to MCP tools from Spec 2 (add_task, list_tasks, update_task, complete_task, delete_task)
- Behavior: Maps user intent to correct MCP tool(s), supports tool chaining, provides friendly confirmation and error responses

## Technical Specifications
- Language: Python 3.9+
- AI Framework: OpenAI Agents SDK
- Tool Integration: MCP tools from Spec 2
- State Management: Stateless (no session memory between requests)
- Response Style: Friendly, conversational tone with clear information

## Key Components
- Natural Language Processing: Handled by OpenAI Agent's LLM
- Tool Mapping: Function schemas that correspond to MCP tools
- Tool Chaining: Multiple tool calls within a single agent run when needed
- Response Generation: Friendly, informative responses based on tool results
- Error Handling: Graceful error reporting with suggestions when possible

## Important Constraints
- No manual coding outside Claude Code execution
- Agent must use only OpenAI Agents SDK for reasoning
- Must maintain stateless operation with no internal state
- Must integrate seamlessly with Spec 2 MCP tools
- Must be compatible with Spec 4 Chat API

## Integration Points
- Consumes MCP tools from Spec 2
- Will be integrated with Chat API in Spec 4
- Uses the same database as Spec 2 for task persistence