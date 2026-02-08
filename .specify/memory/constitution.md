<!-- SYNC IMPACT REPORT
Version change: N/A (initial version) → 1.0.0
Modified principles: N/A
Added sections: All principles and sections added
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application (Hackathon Phase II) Constitution

## Core Principles

### Spec-driven development
All work must be derived strictly from formal specifications. No implementation occurs without a corresponding requirement in the specification document. This ensures traceability, reduces ambiguity, and maintains clear project scope.

### Agentic Dev Stack compliance
Must follow the Spec → Plan → Tasks → Implement workflow strictly. All development activities must originate from and trace back to the established development pipeline to maintain consistency and predictability.

### Security-first design
Security considerations (authentication, authorization, user data isolation) must be designed and implemented as foundational elements, not added as afterthoughts. All user data must be protected with proper authentication and authorization mechanisms.

### Deterministic behavior
All system behavior must be unambiguously defined with no implicit logic. Every feature must have explicitly defined inputs, outputs, and error conditions to ensure predictable operation.

### Zero manual coding
All code changes must be performed through Claude Code and Spec-Kit Plus tools. Manual coding is prohibited to ensure consistency and maintain traceability to specifications.

## Key Standards

- Every feature must trace back to an explicit requirement in the specification
- All API behavior must be defined in the specification before implementation begins
- Authentication must be enforced on every protected endpoint using JWT tokens
- User data must be strictly isolated by authenticated user ID to prevent cross-user access
- Frontend, backend, and database behavior must remain consistent across all components
- Errors must return correct HTTP status codes (401, 403, 404, 422, 500) to ensure proper error handling

## Constraints

- Technology stack is fixed and non-negotiable:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth (JWT-based)
- No manual code edits; all changes must be made via Claude Code
- JWT authentication required for all API routes
- Shared JWT secret must be used consistently across frontend and backend
- All data operations must enforce ownership checks to ensure proper user data isolation
- RESTful API design must be followed strictly to maintain API consistency

## Security Rules

- All API requests require a valid JWT token in the Authorization header
- Requests without a valid token must return 401 Unauthorized status code
- JWT tokens must be verified using the shared secret with proper signature validation
- User identity must be derived ONLY from the JWT payload, never from URL parameters or request bodies
- URL user_id parameters must match the authenticated user ID from the JWT token
- Cross-user data access is strictly forbidden and must be prevented by ownership checks

## Success Criteria

- All 5 Basic Level features work correctly in the web application interface
- Multi-user support with complete data isolation between users
- Persistent storage using Neon PostgreSQL with proper data integrity
- Secure signup and signin using Better Auth with proper session management
- JWT-based authentication fully integrated across frontend and backend
- Backend correctly filters data by authenticated user ID for all operations
- Frontend consistently attaches JWT to API requests in Authorization header
- Project fully follows Agentic Dev Stack workflow from spec to implementation
- All functionality remains reviewable via specs, plans, and development prompts

## Governance

This constitution governs all development activities for the Todo Full-Stack Web Application project. All development must comply with these principles and constraints. Any deviation requires formal amendment to this constitution through documented approval. Development progress is tracked through specifications, implementation plans, task breakdowns, and prompt records to ensure accountability and traceability.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
