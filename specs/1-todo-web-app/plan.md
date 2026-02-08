# Architectural Plan: Todo Full-Stack Web Application (Hackathon Phase II)

## Overview
This document outlines the architectural plan for transforming a console-based todo app into a secure, multi-user web application with authentication, authorization, and data isolation as specified in the feature specification.

## Architecture Components

### Frontend Architecture (Next.js 16+)
- **Framework**: Next.js 16+ with App Router
- **Routing**: Utilize app directory structure for clean route organization
- **Authentication**: Better Auth client integration for handling authentication state
- **API Communication**: Client-side API calls with JWT token attachment
- **State Management**: React hooks for local state management
- **UI Framework**: Tailwind CSS for responsive styling
- **Deployment**: Vercel for optimized Next.js hosting

### Backend Architecture (Python FastAPI)
- **Framework**: FastAPI for high-performance API with automatic documentation
- **Authentication**: JWT token validation middleware
- **Database ORM**: SQLModel for database modeling and operations
- **Database Connection**: Async SQLAlchemy engine for Neon Serverless PostgreSQL
- **API Structure**: RESTful endpoints with proper authentication middleware
- **Error Handling**: Custom exception handlers with proper HTTP status codes
- **Validation**: Pydantic models for request/response validation

### Database Architecture (Neon Serverless PostgreSQL)
- **Provider**: Neon Serverless PostgreSQL for auto-scaling database
- **Modeling**: SQLModel for defining database tables and relationships
- **Connection**: Async connection pooling for efficient database access
- **Migration**: Alembic for database schema migrations
- **Data Isolation**: User ID-based filtering for data isolation

### Authentication Architecture (Better Auth)
- **Implementation**: Better Auth for complete authentication solution
- **JWT Tokens**: Session-based authentication with JWT tokens
- **Token Flow**:
  1. User authenticates via Better Auth on frontend
  2. Better Auth issues JWT token
  3. Frontend stores and sends token with API requests
  4. Backend verifies token signature using shared secret
  5. Backend extracts user identity from JWT payload
  6. Backend enforces user data isolation

## System Design

### Authentication Flow
1. **User Registration/Login**:
   - User accesses frontend authentication pages
   - Better Auth handles registration/login flow
   - Upon successful authentication, JWT token is issued
   - Frontend securely stores the token

2. **Protected API Access**:
   - Frontend includes JWT in Authorization header for protected endpoints
   - Backend middleware intercepts requests to protected endpoints
   - JWT is validated using shared secret
   - User identity is extracted from JWT payload
   - Request proceeds with authenticated user context

3. **Data Isolation**:
   - All data access operations include user ID from JWT
   - Backend enforces user data access controls
   - Cross-user data access is prevented by ownership checks

### API Design
- **RESTful Endpoints**: Standard HTTP methods (GET, POST, PUT, DELETE)
- **Authentication**: JWT token in Authorization header for protected endpoints
- **Status Codes**: Proper HTTP status codes (200, 201, 400, 401, 403, 404, 422, 500)
- **Error Format**: Consistent error response structure
- **Input Validation**: Pydantic models for request validation

### Database Design
- **Tables**: Users table with email, password hash, and timestamps
- **Tables**: Todos table with title, description, status, and user_id foreign key
- **Relationships**: One-to-many relationship between users and todos
- **Indexing**: Index on user_id for efficient filtering
- **Constraints**: Unique email constraint on users

## Security Measures

### Authentication Security
- JWT tokens with appropriate expiration times
- Secure token storage and transmission
- Proper validation of JWT signatures
- Password hashing with bcrypt

### Data Security
- User data isolation at the database level
- Input validation and sanitization
- Parameterized queries to prevent SQL injection
- Proper access controls on all endpoints

### API Security
- Authentication required for all protected endpoints
- Proper error handling without information leakage
- CORS configuration appropriate for deployment

## Deployment Architecture
- **Frontend**: Deployed on Vercel with custom domain
- **Backend**: Deployed on Python-compatible platform (Railway, Render)
- **Database**: Neon Serverless PostgreSQL cloud database
- **Environment Variables**: Secure configuration of secrets and settings

## Integration Points

### Frontend ↔ Backend
- RESTful API endpoints with JSON communication
- JWT token in Authorization header for authentication
- Error handling and status code interpretation

### Backend ↔ Database
- SQLModel ORM for database operations
- Async connection pooling for performance
- Transaction management for data consistency

## Performance Considerations
- Database query optimization with proper indexing
- Efficient API endpoint design to minimize data transfer
- Connection pooling for database operations

## Error Handling Strategy
- **Client-Side**: User-friendly error messages with proper UI feedback
- **API-Level**: Proper HTTP status codes and structured error responses
- **Database**: Transaction rollback and proper exception handling
- **Authentication**: Consistent handling of expired/invalid tokens

## Compliance with Specification Requirements

### Phase 1: Authentication & User Isolation
- [ ] Configure Better Auth for signup/signin
- [ ] Enable JWT issuance and expiry
- [ ] Define shared secret configuration
- [ ] Implement JWT verification in FastAPI
- [ ] Enforce user identity and request authorization
- [ ] Validate 401 behavior for unauthenticated requests

### Phase 2: Backend API & Persistence
- [ ] Design SQLModel schemas for users and tasks
- [ ] Connect FastAPI to Neon Serverless PostgreSQL
- [ ] Implement RESTful task endpoints
- [ ] Enforce task ownership in all queries
- [ ] Validate input, output, and error handling
- [ ] Confirm persistence across sessions

### Phase 3: Frontend Web Application
- [ ] Build auth-aware Next.js pages (login, signup)
- [ ] Implement task list, create, update, delete UI
- [ ] Attach JWT token to all API requests
- [ ] Handle loading, error, and empty states
- [ ] Ensure responsive layout and usability

## Key Risks and Mitigation Strategies

### Authentication Integration Risk
- Risk: Difficulty integrating Better Auth with FastAPI backend
- Mitigation: Research existing implementations and create proof-of-concept early

### Data Isolation Risk
- Risk: Accidental cross-user data access
- Mitigation: Design ownership checks into base API layer and database constraints

### Performance Risk
- Risk: Slow database queries affecting user experience
- Mitigation: Proper indexing strategy and query optimization from the start

## Validation & Review
- All success criteria from specification will be verified
- Security rules will be enforced at all levels
- No manual code edits will be made (all via Claude Code)
- All work will remain reproducible and inspectable