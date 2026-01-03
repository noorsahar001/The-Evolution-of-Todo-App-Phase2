# Implementation Plan: Todo Full-Stack Web Application (Phase II)

**Branch**: `002-todo-fullstack-webapp` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-fullstack-webapp/spec.md`

## Summary

Phase II transforms the Phase I CLI application into a production-ready, multi-user full-stack web application. The implementation consists of a FastAPI backend with SQLModel ORM for persistent storage in Neon PostgreSQL, and a Next.js 14+ frontend with App Router. Authentication uses JWT tokens stored in httpOnly cookies via Better Auth patterns.

**Key Deliverables**:
1. RESTful API with 9 endpoints (3 auth, 6 task operations)
2. User registration and JWT-based authentication
3. Per-user task isolation with ownership enforcement
4. Responsive web interface for task management

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Pydantic v2, Next.js 14+, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL via `DATABASE_URL`
**Testing**: pytest with pytest-asyncio (backend), Jest + RTL (frontend, optional)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
**Project Type**: Web application (frontend + backend monorepo)
**Performance Goals**: 2s page load, 100 concurrent users, 99% API success rate
**Constraints**: Stateless services, JWT auth, user isolation
**Scale/Scope**: 100 concurrent users, ~10 screens, 2 entities (User, Task)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Verification |
|-----------|--------|--------------|
| I. Spec-Driven Development | PASS | All behavior defined in spec.md before implementation |
| II. In-Scope Features | PASS | Auth + Task CRUD + REST API + Web UI as specified |
| III. Exclusions | PASS | No AI, sharing, categories, priorities, mobile, Docker |
| IV. Task Rules & Validation | PASS | Auto-increment IDs, validation, error responses defined |
| V. Data Storage Rules | PASS | PostgreSQL via SQLModel, user isolation, env vars |
| VI. Simplicity & YAGNI | PASS | Minimal implementation, no extra features |
| VII. Security Principles | PASS | JWT required, user isolation, no frontend trust |
| VIII. Statelessness | PASS | No memory state in frontend or backend |
| IX. API Contract Rules | PASS | OpenAPI documented, Pydantic schemas, error format |

**Gate Status**: PASSED - Proceeding to implementation planning

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-fullstack-webapp/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Setup and run guide
├── contracts/
│   └── openapi.yaml     # API contract
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth business logic
│   │   └── task.py          # Task CRUD logic
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # get_current_user, get_db
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py      # Auth endpoints
│   │   │   └── tasks.py     # Task endpoints
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── user.py      # User Pydantic schemas
│   │       └── task.py      # Task Pydantic schemas
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings from env vars
│   │   ├── database.py      # Database connection
│   │   └── security.py      # JWT utilities
│   └── main.py              # FastAPI app entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── unit/
│   │   └── test_services.py
│   └── integration/
│       ├── test_auth.py
│       └── test_tasks.py
├── requirements.txt
└── .env.example

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home/redirect
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   └── dashboard/
│   │       ├── layout.tsx   # Protected layout
│   │       └── page.tsx     # Task list
│   ├── components/
│   │   ├── ui/              # Basic UI components
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   └── tasks/
│   │       ├── TaskList.tsx
│   │       ├── TaskItem.tsx
│   │       ├── TaskForm.tsx
│   │       └── DeleteConfirm.tsx
│   ├── lib/
│   │   ├── api.ts           # Fetch wrapper
│   │   └── auth.ts          # Auth helpers
│   └── types/
│       └── index.ts         # TypeScript types
├── middleware.ts            # Auth redirect middleware
├── package.json
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── .env.local.example
```

**Structure Decision**: Web application pattern with separate backend/ and frontend/ directories. Backend follows FastAPI best practices with layered architecture (routes → services → models). Frontend uses Next.js App Router with route groups for auth pages.

## Implementation Order

### Phase 1: Backend Foundation

1. **Project Setup**
   - Initialize backend directory structure
   - Create requirements.txt with dependencies
   - Set up .env.example with required variables

2. **Core Infrastructure**
   - config.py: Load environment variables
   - database.py: PostgreSQL connection with SQLModel
   - security.py: JWT create/verify utilities

3. **Database Models**
   - User model with email, hashed_password
   - Task model with user_id foreign key
   - Database initialization

### Phase 2: Backend Authentication

4. **Auth Schemas**
   - UserCreate, UserLogin request schemas
   - UserResponse schema

5. **Auth Service**
   - register(): Create user with hashed password
   - authenticate(): Verify credentials, return JWT
   - Duplicate email handling

6. **Auth Routes**
   - POST /api/auth/register
   - POST /api/auth/login
   - POST /api/auth/logout
   - Cookie handling

7. **Auth Middleware**
   - deps.py: get_current_user dependency
   - JWT validation and user extraction

### Phase 3: Backend Task API

8. **Task Schemas**
   - TaskCreate, TaskUpdate request schemas
   - TaskResponse schema

9. **Task Service**
   - CRUD operations with user_id filtering
   - Ownership validation

10. **Task Routes**
    - GET /api/tasks (list)
    - POST /api/tasks (create)
    - GET /api/tasks/{id} (read)
    - PUT /api/tasks/{id} (update)
    - DELETE /api/tasks/{id} (delete)
    - PATCH /api/tasks/{id}/toggle

11. **Error Handling**
    - Standard error response format
    - 401, 403, 404 handlers

### Phase 4: Frontend Foundation

12. **Project Setup**
    - Initialize Next.js with App Router
    - Configure TypeScript strict mode
    - Set up Tailwind CSS
    - Create .env.local.example

13. **Core Infrastructure**
    - API client with fetch wrapper
    - Type definitions for User, Task, Error

14. **Layouts**
    - Root layout with global styles
    - Protected dashboard layout

15. **Auth Middleware**
    - Next.js middleware for route protection
    - Redirect unauthenticated users to login

### Phase 5: Frontend Authentication

16. **Auth Pages**
    - Register page with form
    - Login page with form
    - Form validation

17. **Auth Components**
    - RegisterForm component
    - LoginForm component
    - Error display

18. **Auth Flow**
    - Submit to backend
    - Handle success/error
    - Redirect on success

### Phase 6: Frontend Task Management

19. **Dashboard Page**
    - Fetch tasks from API
    - Display task list or empty state
    - Loading states

20. **Task Components**
    - TaskList container
    - TaskItem with toggle, edit, delete
    - TaskForm for create/edit
    - DeleteConfirm modal

21. **Task Operations**
    - Create task flow
    - Edit task flow
    - Delete task flow
    - Toggle completion

### Phase 7: Polish and Validation

22. **Responsive Design**
    - Mobile-friendly layouts
    - Touch-friendly buttons

23. **Error Handling**
    - User-friendly error messages
    - Network error handling

24. **Testing**
    - Backend integration tests
    - Manual E2E testing

## Complexity Tracking

> **No violations identified** - Implementation follows Constitution principles

| Aspect | Complexity Level | Justification |
|--------|-----------------|---------------|
| Architecture | Standard | Typical full-stack web app |
| Authentication | Standard | JWT with cookies, no OAuth |
| Database | Simple | 2 entities, 1 relationship |
| Frontend | Moderate | Server Components + Client forms |

## Milestones and Checkpoints

### Milestone 1: Backend API Complete
**Verification**:
- All endpoints accessible via Swagger UI
- Register/login returns JWT cookie
- Tasks CRUD works with authentication
- User isolation enforced (403 on other's tasks)

### Milestone 2: Frontend Auth Complete
**Verification**:
- User can register new account
- User can login and see dashboard
- Unauthenticated access redirects to login
- User can logout

### Milestone 3: Task Management Complete
**Verification**:
- User can create tasks
- User can view task list
- User can edit tasks
- User can delete tasks
- User can toggle completion

### Final Checkpoint: Phase II Complete
**Constitution Compliance Review**:
- [ ] All endpoints require JWT authentication (except public auth routes)
- [ ] Backend extracts user ID from JWT, never from request body
- [ ] Users can only access their own tasks (403 on unauthorized access)
- [ ] No secrets hardcoded in source code
- [ ] API responses follow the standard error format
- [ ] Frontend does not assume server state between requests
- [ ] Backend does not store session state in memory
- [ ] OpenAPI documentation is up to date

## Dependencies and Risks

### Dependencies
- Neon PostgreSQL account setup
- Node.js and Python environment availability
- Network connectivity for database

### Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Database connection issues | High | Test connection early, document troubleshooting |
| CORS configuration | Medium | Test frontend-backend communication early |
| JWT cookie not setting | Medium | Test across browsers, document cookie settings |

## Next Steps

1. Run `/sp.tasks` to generate detailed task breakdown
2. Begin implementation following task order
3. Validate each milestone before proceeding
4. Complete final compliance review
