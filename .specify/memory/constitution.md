<!--
Sync Impact Report
==================
<<<<<<< HEAD
Version change: 0.0.0 → 1.0.0 (MAJOR - initial ratification)
Modified principles: N/A (initial version)
Added sections:
  - Core Principles (I–VI)
  - Technical Constraints
  - Project Structure Requirements
  - Governance
Removed sections: N/A (initial version)
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ aligned (Constitution Check section exists)
  - .specify/templates/spec-template.md: ✅ aligned (scope/requirements structure compatible)
  - .specify/templates/tasks-template.md: ✅ aligned (task phases align with constitution workflow)
Follow-up TODOs: None
-->

# The Evolution of Todo – Phase I Constitution
=======
Version change: 1.0.0 → 2.0.0 (MAJOR - Phase II transformation)
Modified principles:
  - II. In-Scope Features: Phase I CLI features → Phase II web application features
  - III. Exclusions: Removed database, web, auth from exclusions → Now core requirements
  - V. Data Storage Rules: In-memory only → PostgreSQL with user isolation
Added sections:
  - VII. Security Principles (JWT, user isolation, endpoint protection)
  - VIII. Statelessness Requirements
  - IX. API Contract Rules
  - Extended Technical Constraints for full-stack architecture
Removed sections:
  - Phase I specific in-memory storage constraints
  - CLI-only interface constraints
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ aligned (Constitution Check and web app structure exist)
  - .specify/templates/spec-template.md: ✅ aligned (supports multi-tier requirements)
  - .specify/templates/tasks-template.md: ✅ aligned (backend/frontend structure supported)
Follow-up TODOs: None
-->

# The Evolution of Todo – Phase II Constitution

## Preamble

Phase I established the foundational Spec-Driven Development (SDD) workflow through a minimal in-memory CLI application. Phase II transforms the Todo application into a production-ready, full-stack, multi-user web application while preserving the SDD methodology that ensures traceability and quality.
>>>>>>> e88161c (complete phase 2)

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

<<<<<<< HEAD
All behavior MUST be defined in specifications before implementation. Code MUST be generated only by Claude Code. Manual coding is strictly forbidden. If behavior is incorrect, the spec MUST be refined—not the code.

**Rationale**: This principle ensures traceability from requirement to implementation and prevents ad-hoc changes that bypass the specification process.

### II. In-Scope Features

The application MUST support the following and ONLY the following features:

1. **Add Task** — Create a new task with title (required) and description (optional)
2. **View Tasks** — Display all tasks showing ID, title, and completion status
3. **Update Task** — Modify task title and/or description by ID
4. **Delete Task** — Remove a task by ID
5. **Mark Task Complete/Incomplete** — Toggle completion status by ID

**Rationale**: Phase I scope is intentionally minimal to validate the Spec-Driven Development workflow before adding complexity.

### III. Exclusions (NON-NEGOTIABLE)

The following are explicitly OUT OF SCOPE for Phase I:

- Databases or file storage
- Web or mobile interfaces
- Authentication
- AI or chatbot features
- Docker, Kubernetes, or cloud deployment

**Rationale**: These exclusions keep Phase I focused on core Todo functionality with in-memory storage only.

### IV. Task Rules & Validation

- Task IDs MUST be auto-incrementing integers
- Task title MUST NOT be empty
- Invalid task IDs MUST be handled gracefully with clear error messages
- The application MUST NOT crash on invalid input

**Rationale**: Defensive validation ensures a robust user experience even with erroneous input.

### V. Data Storage Rules

- All data MUST be stored in memory only (Python list or dictionary)
- No data persistence between program runs is permitted
- No external storage mechanisms are allowed

**Rationale**: In-memory storage simplifies Phase I implementation and avoids external dependencies.

### VI. Simplicity & YAGNI

- Start with the smallest viable implementation
- Do not add features beyond what is specified
- Avoid premature abstraction or over-engineering

**Rationale**: Complexity MUST be justified. Phase I validates the process, not architectural scalability.

## Technical Constraints

- **Language**: Python 3.13+
- **Interface**: Terminal / Console (CLI)
- **External Dependencies**: None (standard library only preferred)
- **Storage**: In-memory (Python list or dictionary)
- **Testing**: pytest (if tests are requested)
=======
All behavior MUST be defined in specifications before implementation. Code MUST be generated only by Claude Code. Manual coding is strictly forbidden. If behavior is incorrect, the spec MUST be refined—not the code. No assumptions outside specs are permitted.

**Rationale**: This principle ensures traceability from requirement to implementation and prevents ad-hoc changes that bypass the specification process.

### II. In-Scope Features (Phase II)

The application MUST support the following features for multi-user web access:

1. **User Authentication**
   - User registration with email and password
   - User login/logout with JWT token management
   - Session management via Better Auth

2. **Task Management (Per-User)**
   - Add Task — Create a new task with title (required) and description (optional)
   - View Tasks — Display all tasks for the authenticated user
   - Update Task — Modify task title and/or description by ID (owner only)
   - Delete Task — Remove a task by ID (owner only)
   - Mark Task Complete/Incomplete — Toggle completion status by ID (owner only)

3. **REST API**
   - All task operations exposed via RESTful endpoints
   - JSON request/response format
   - Proper HTTP status codes and error responses

4. **Web Interface**
   - Server-rendered pages with client-side interactivity
   - Authentication forms (register, login)
   - Task management dashboard

**Rationale**: Phase II extends Phase I functionality to multi-user web access while maintaining feature parity with the CLI for task operations.

### III. Exclusions (Phase II)

The following are explicitly OUT OF SCOPE for Phase II:

- AI or chatbot features
- Task sharing between users
- Task categories, tags, or labels
- Due dates, reminders, or notifications
- Task priorities or ordering
- Mobile native applications
- Docker, Kubernetes, or cloud deployment configurations
- Third-party OAuth providers (GitHub, Google, etc.)
- Email verification or password reset flows
- Rate limiting or throttling
- Caching layers (Redis, etc.)

**Rationale**: These exclusions keep Phase II focused on core multi-user task management. Future phases may introduce these features.

### IV. Task Rules & Validation

- Task IDs MUST be auto-incrementing integers or UUIDs (implementation decision in spec)
- Task title MUST NOT be empty
- Invalid task IDs MUST return 404 Not Found
- Unauthorized access to another user's tasks MUST return 403 Forbidden
- Invalid input MUST return 400 Bad Request with clear error messages
- The application MUST NOT expose stack traces or internal errors to clients

**Rationale**: Defensive validation ensures a robust and secure user experience.

### V. Data Storage Rules (Phase II)

- All data MUST be persisted in Neon Serverless PostgreSQL
- Database schema MUST be managed via SQLModel ORM
- Each task MUST be associated with exactly one user (owner)
- Users MUST only access their own tasks
- Database credentials MUST be stored in environment variables, never hardcoded

**Rationale**: PostgreSQL provides the durability and multi-user isolation required for a production web application.

### VI. Simplicity & YAGNI

- Start with the smallest viable implementation that meets the spec
- Do not add features beyond what is specified
- Avoid premature abstraction or over-engineering
- Complexity MUST be justified in writing (Complexity Tracking in plan.md)

**Rationale**: Phase II validates full-stack SDD, not architectural scalability for millions of users.

### VII. Security Principles (NON-NEGOTIABLE)

- **Authentication Required**: All task-related endpoints MUST require valid JWT authentication
- **JWT Validation**: Every request MUST validate the JWT token before processing
- **User Isolation**: Backend MUST enforce that users can only access their own tasks
- **No Trust of Frontend**: Backend MUST NOT trust any user ID from frontend; extract from JWT only
- **Secrets Management**: All secrets (database URL, JWT secret) MUST be in environment variables
- **HTTPS**: Production deployment MUST use HTTPS (development may use HTTP)
- **Input Sanitization**: All user input MUST be sanitized to prevent injection attacks

**Rationale**: Security is non-negotiable in a multi-user system. These principles prevent common vulnerabilities.

### VIII. Statelessness Requirements (NON-NEGOTIABLE)

- **Frontend Statelessness**: Next.js frontend MUST NOT store user state in memory between requests; all state from JWT or database
- **Backend Statelessness**: FastAPI backend MUST NOT store session state in memory; use JWT for authentication state
- **Horizontal Scalability**: Architecture MUST support multiple frontend and backend instances without shared memory

**Rationale**: Statelessness enables horizontal scaling and prevents session affinity issues.

### IX. API Contract Rules

- All API endpoints MUST be documented in OpenAPI/Swagger format
- Request and response schemas MUST be defined using Pydantic models
- Breaking API changes MUST be versioned (future phases)
- Error responses MUST follow a consistent structure:
  ```json
  {
    "detail": "Human-readable error message",
    "code": "ERROR_CODE"
  }
  ```

**Rationale**: Clear API contracts enable frontend-backend development in parallel and improve maintainability.

## Technical Constraints

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS (or as specified in feature specs)
- **State Management**: React Server Components + minimal client state
- **HTTP Client**: fetch API or as specified

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLModel
- **Validation**: Pydantic v2
- **Authentication**: Better Auth with JWT
- **API Documentation**: Auto-generated OpenAPI/Swagger

### Database
- **Provider**: Neon Serverless PostgreSQL
- **Connection**: Via environment variable `DATABASE_URL`
- **Migrations**: SQLModel/Alembic (as specified in feature specs)

### Testing
- **Backend**: pytest with pytest-asyncio
- **Frontend**: Jest + React Testing Library (if tests requested)
- **API**: Contract tests against OpenAPI spec
>>>>>>> e88161c (complete phase 2)

## Project Structure Requirements

The generated project MUST follow this structure:

```text
<<<<<<< HEAD
src/
├── models/          # Task data model
├── services/        # Business logic (add, update, delete, toggle)
├── cli/             # Command-line interface handlers
└── main.py          # Entry point

tests/
├── unit/            # Unit tests for models and services
└── integration/     # End-to-end CLI tests
=======
backend/
├── src/
│   ├── models/          # SQLModel database models (User, Task)
│   ├── services/        # Business logic (task CRUD, auth)
│   ├── api/
│   │   ├── routes/      # FastAPI route handlers
│   │   ├── deps.py      # Dependency injection (get_current_user, get_db)
│   │   └── schemas/     # Pydantic request/response schemas
│   ├── core/
│   │   ├── config.py    # Settings and environment variables
│   │   └── security.py  # JWT utilities
│   └── main.py          # FastAPI application entry point
├── tests/
│   ├── unit/            # Unit tests for services
│   ├── integration/     # API endpoint tests
│   └── conftest.py      # Pytest fixtures
├── alembic/             # Database migrations (if used)
└── requirements.txt     # Python dependencies

frontend/
├── src/
│   ├── app/             # Next.js App Router pages
│   │   ├── (auth)/      # Auth pages (login, register)
│   │   ├── dashboard/   # Protected task management pages
│   │   └── layout.tsx   # Root layout
│   ├── components/      # Reusable UI components
│   ├── lib/             # Utilities (API client, auth helpers)
│   └── types/           # TypeScript type definitions
├── tests/               # Frontend tests (if requested)
├── package.json         # Node dependencies
└── next.config.js       # Next.js configuration

specs/
├── <feature-name>/
│   ├── spec.md          # Feature specification
│   ├── plan.md          # Implementation plan
│   ├── tasks.md         # Task breakdown
│   └── contracts/       # API contracts (OpenAPI snippets)

history/
├── prompts/             # Prompt History Records
│   ├── constitution/
│   ├── <feature-name>/
│   └── general/
└── adr/                 # Architecture Decision Records

.specify/
├── memory/
│   └── constitution.md  # This file
├── templates/           # Spec-Kit Plus templates
└── scripts/             # Automation scripts
>>>>>>> e88161c (complete phase 2)
```

## Governance

<<<<<<< HEAD
1. This constitution supersedes all other documentation and practices for Phase I
2. Amendments require:
   - Written justification
   - Version increment following semantic versioning
   - Updated Last Amended date
3. All specifications and implementations MUST verify compliance with this constitution
4. Complexity beyond these principles MUST be justified in writing

**Version**: 1.0.0 | **Ratified**: 2025-12-26 | **Last Amended**: 2025-12-26
=======
1. This constitution supersedes all other documentation and practices for Phase II
2. All specifications and implementations MUST verify compliance with this constitution
3. Amendments require:
   - Written justification documenting the need for change
   - Version increment following semantic versioning:
     - MAJOR: Principle removal or backward-incompatible governance changes
     - MINOR: New principle or materially expanded guidance
     - PATCH: Clarifications, wording fixes, non-semantic refinements
   - Updated Last Amended date
4. Complexity beyond these principles MUST be justified in the plan.md Complexity Tracking table
5. All changes MUST go through specs—no direct code modifications without spec updates
6. Architecture decisions meeting significance criteria MUST be documented via ADR

## Compliance Review Checklist

Before marking any feature as complete, verify:

- [ ] All endpoints require JWT authentication (except public auth routes)
- [ ] Backend extracts user ID from JWT, never from request body
- [ ] Users can only access their own tasks (403 on unauthorized access)
- [ ] No secrets hardcoded in source code
- [ ] API responses follow the standard error format
- [ ] Frontend does not assume server state between requests
- [ ] Backend does not store session state in memory
- [ ] OpenAPI documentation is up to date

**Version**: 2.0.0 | **Ratified**: 2025-12-26 | **Last Amended**: 2025-12-30
>>>>>>> e88161c (complete phase 2)
