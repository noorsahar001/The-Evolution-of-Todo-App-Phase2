# Research: Todo Full-Stack Web Application (Phase II)

**Feature Branch**: `002-todo-fullstack-webapp`
**Date**: 2025-12-30
**Status**: Complete

## Overview

This document captures technology decisions and best practices research for Phase II implementation. All choices align with the Phase II Constitution technical constraints.

## Technology Stack Decisions

### Backend Framework: FastAPI

**Decision**: Use FastAPI as the backend framework

**Rationale**:
- Constitution mandates FastAPI (Technical Constraints)
- Native async support for database operations
- Automatic OpenAPI documentation generation (FR-023)
- Built-in Pydantic v2 integration for request/response validation
- Excellent performance for API workloads

**Alternatives Considered**:
- Django REST Framework: More batteries-included but heavier, not mandated
- Flask: Lighter but lacks native async and auto-documentation

### ORM: SQLModel

**Decision**: Use SQLModel for database models and queries

**Rationale**:
- Constitution mandates SQLModel (Technical Constraints)
- Combines SQLAlchemy Core with Pydantic models
- Reduces boilerplate by sharing models between DB and API
- Type-safe queries with IDE support

**Alternatives Considered**:
- SQLAlchemy alone: More verbose, requires separate Pydantic schemas
- Tortoise ORM: Good async support but less mature ecosystem

### Database: Neon Serverless PostgreSQL

**Decision**: Use Neon as the PostgreSQL provider

**Rationale**:
- Constitution mandates Neon Serverless PostgreSQL (Technical Constraints)
- Serverless scaling for variable workloads
- PostgreSQL compatibility for reliable ACID transactions
- Connection pooling included

**Connection Pattern**:
- Use connection string from `DATABASE_URL` environment variable
- Enable connection pooling for serverless environments
- Use async database driver (asyncpg) for FastAPI compatibility

### Authentication: Better Auth + JWT

**Decision**: Implement JWT-based authentication using Better Auth patterns

**Rationale**:
- Constitution mandates Better Auth with JWT (Technical Constraints)
- Stateless authentication enables horizontal scaling (Principle VIII)
- httpOnly cookies prevent XSS token theft (FR-006)

**Implementation Approach**:
- JWT tokens stored in httpOnly, Secure, SameSite=Lax cookies
- Token contains user ID and expiration time
- Backend validates JWT on every protected request
- No session storage in backend memory

**JWT Configuration**:
- Algorithm: HS256 (symmetric, sufficient for single-service)
- Expiration: 24 hours (reasonable for task management app)
- Secret: From `JWT_SECRET` environment variable
- Refresh tokens: Out of scope for Phase II

### Password Hashing: bcrypt

**Decision**: Use bcrypt for password hashing

**Rationale**:
- Industry-standard algorithm for password storage
- Built-in salt generation
- Configurable work factor for future-proofing
- Available via `passlib` or `bcrypt` Python packages

**Configuration**:
- Work factor (rounds): 12 (default, balances security and performance)

### Frontend Framework: Next.js 14+ App Router

**Decision**: Use Next.js with App Router

**Rationale**:
- Constitution mandates Next.js 14+ with App Router (Technical Constraints)
- Server Components reduce client-side JavaScript
- Built-in routing with layouts
- API routes for BFF pattern (if needed)

**Key Patterns**:
- React Server Components for data fetching
- Client Components for interactive forms
- Middleware for auth redirects

### Styling: Tailwind CSS

**Decision**: Use Tailwind CSS for styling

**Rationale**:
- Constitution specifies Tailwind CSS (Technical Constraints)
- Utility-first approach speeds development
- Responsive design built-in (FR-030)
- No custom CSS files needed

### TypeScript Configuration

**Decision**: Strict TypeScript mode

**Rationale**:
- Constitution mandates strict mode (Technical Constraints)
- Catches type errors at compile time
- Better IDE support and refactoring

**Key tsconfig.json Settings**:
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

## API Design Decisions

### REST API Patterns

**Decision**: Standard REST conventions with JSON

**Rationale**:
- Constitution requires JSON format (FR-022)
- Predictable URL structure
- Standard HTTP methods (GET, POST, PUT, DELETE, PATCH)

**URL Conventions**:
- Base path: `/api`
- Auth routes: `/api/auth/*` (public)
- Task routes: `/api/tasks/*` (protected)
- Use plural nouns for collections

### Error Response Format

**Decision**: Consistent error structure per Constitution

**Format**:
```json
{
  "detail": "Human-readable message",
  "code": "ERROR_CODE"
}
```

**Error Codes**:
| Code | HTTP Status | When |
|------|-------------|------|
| VALIDATION_ERROR | 400 | Invalid input |
| UNAUTHORIZED | 401 | Missing/invalid JWT |
| FORBIDDEN | 403 | Access denied |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Duplicate resource |
| INTERNAL_ERROR | 500 | Server error |

### Task ID Format

**Decision**: Use auto-incrementing integers for task IDs

**Rationale**:
- Simpler than UUIDs for this scope
- Constitution allows either (Principle IV)
- Easier for users to reference

## Frontend Architecture Decisions

### State Management

**Decision**: Minimal client state with Server Components

**Rationale**:
- Constitution requires frontend statelessness (Principle VIII)
- Server Components handle data fetching
- Client state only for UI interactions (form inputs, loading states)

**Pattern**:
- Fetch data in Server Components
- Pass to Client Components as props
- Use `useState` only for local UI state
- Revalidate data after mutations

### API Client Pattern

**Decision**: Custom fetch wrapper with cookie handling

**Rationale**:
- Need to send httpOnly cookies with requests
- Centralized error handling
- Type-safe request/response

**Implementation**:
- Wrapper around `fetch` with `credentials: 'include'`
- Generic typing for responses
- Error transformation to user-friendly messages

### Auth Flow

**Decision**: Redirect-based authentication

**Flow**:
1. Unauthenticated user → Login page
2. Login form submits to backend
3. Backend sets JWT cookie
4. Frontend redirects to dashboard
5. Protected routes check auth via middleware
6. Logout clears cookie and redirects to login

## Database Schema Decisions

### User Table

**Decision**: Minimal user schema

**Fields**:
- `id`: Integer, primary key, auto-increment
- `email`: String(255), unique, not null
- `hashed_password`: String(255), not null
- `created_at`: Timestamp, default now

### Task Table

**Decision**: Task with user ownership

**Fields**:
- `id`: Integer, primary key, auto-increment
- `title`: String(200), not null
- `description`: Text(2000), nullable
- `is_completed`: Boolean, default false
- `user_id`: Integer, foreign key to User
- `created_at`: Timestamp, default now
- `updated_at`: Timestamp, on update now

**Indexes**:
- `user_id` for filtering tasks by user
- `user_id + id` for task lookup with ownership check

## Testing Strategy

### Backend Tests

**Tools**: pytest, pytest-asyncio, httpx (for async test client)

**Test Categories**:
1. Unit tests for services
2. Integration tests for API endpoints
3. Auth flow tests

### Frontend Tests (Optional)

**Tools**: Jest, React Testing Library

**Test Categories**:
1. Component render tests
2. Form interaction tests
3. API integration tests (mocked)

## Environment Variables

### Backend

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | Neon PostgreSQL connection string | Yes |
| JWT_SECRET | Secret key for JWT signing | Yes |
| JWT_ALGORITHM | JWT algorithm (default: HS256) | No |
| JWT_EXPIRATION_HOURS | Token expiration (default: 24) | No |

### Frontend

| Variable | Description | Required |
|----------|-------------|----------|
| NEXT_PUBLIC_API_URL | Backend API base URL | Yes |

## Performance Considerations

### Database
- Connection pooling via Neon
- Index on user_id for task queries
- Limit task list queries (pagination in future phases)

### Backend
- Async handlers for non-blocking I/O
- Pydantic validation on request boundary

### Frontend
- Server Components reduce bundle size
- Tailwind CSS purges unused styles
- No heavy client-side libraries

## Security Checklist

Based on Constitution Principle VII:

- [x] JWT in httpOnly cookie (XSS protection)
- [x] User ID from JWT only (no trust of frontend)
- [x] Password hashing with bcrypt
- [x] Input validation with Pydantic
- [x] SQL injection prevention via ORM
- [x] CORS configuration for frontend origin
- [x] Secrets in environment variables

## Resolved Clarifications

| Item | Resolution |
|------|------------|
| JWT expiration | 24 hours (reasonable for task app) |
| Password hash algorithm | bcrypt with 12 rounds |
| Task ID format | Auto-incrementing integers |
| Session refresh | Out of scope (no refresh tokens) |
| CORS origins | Frontend URL only |
