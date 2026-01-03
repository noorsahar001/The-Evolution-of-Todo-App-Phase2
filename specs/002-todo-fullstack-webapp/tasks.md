# Tasks: Todo Full-Stack Web Application (Phase II)

**Input**: Design documents from `/specs/002-todo-fullstack-webapp/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/openapi.yaml

**Organization**: Tasks are grouped by implementation phase from plan.md, mapped to user stories and functional requirements from spec.md.

## Format: `[ID] [P?] [Story/FR] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story/FR]**: Which user story or functional requirement this task implements
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/`

---

## Phase 1: Backend Foundation (Setup)

**Purpose**: Project initialization and core infrastructure

**Spec References**: Technical Constraints (Constitution), Project Structure (plan.md)

### Setup Tasks

- [x] T001 [P] Create backend directory structure per plan.md in `backend/`
- [x] T002 [P] Create `backend/requirements.txt` with FastAPI, SQLModel, Pydantic, python-jose, passlib, bcrypt, uvicorn, asyncpg, python-dotenv
- [x] T003 [P] Create `backend/.env.example` with DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS, CORS_ORIGINS

### Core Infrastructure Tasks

- [x] T004 Create `backend/src/core/__init__.py`
- [x] T005 Create `backend/src/core/config.py` - Settings class loading env vars (FR-017: secrets in env vars)
- [x] T006 Create `backend/src/core/database.py` - SQLModel engine and session (FR-005: PostgreSQL connection)
- [x] T007 Create `backend/src/core/security.py` - JWT create_token and verify_token functions (FR-005, FR-006)

**Checkpoint**: Backend project structure complete, can import core modules

---

## Phase 2: Backend Database Models (Foundational)

**Purpose**: Database schema that MUST be complete before API implementation

**Spec References**: data-model.md, FR-010, FR-015, FR-016

### Model Tasks

- [x] T008 Create `backend/src/models/__init__.py`
- [x] T009 Create `backend/src/models/user.py` - User SQLModel with id, email, hashed_password, created_at (data-model.md)
- [x] T010 Create `backend/src/models/task.py` - Task SQLModel with id, title, description, is_completed, user_id, created_at, updated_at (data-model.md)
- [x] T011 Update `backend/src/core/database.py` - Add create_db_and_tables function to initialize schema

**Checkpoint**: Database models defined, tables can be created

---

## Phase 3: Backend Authentication - User Story 1 & 2 (P1)

**Purpose**: Implement user registration, login, and logout

**Spec References**: US1, US2, FR-001 to FR-008

### Auth Schemas

- [x] T012 Create `backend/src/api/schemas/__init__.py`
- [x] T013 Create `backend/src/api/schemas/user.py` - UserCreate (email, password min 8), UserLogin, UserResponse schemas (FR-001, FR-002)

### Auth Service

- [x] T014 Create `backend/src/services/__init__.py`
- [x] T015 Create `backend/src/services/auth.py` - register() with password hashing, duplicate email check (FR-001, FR-003)
- [x] T016 Update `backend/src/services/auth.py` - authenticate() verify credentials, return user (FR-004)

### Auth Dependencies

- [x] T017 Create `backend/src/api/__init__.py`
- [x] T018 Create `backend/src/api/deps.py` - get_db dependency for database session
- [x] T019 Update `backend/src/api/deps.py` - get_current_user dependency extracting user from JWT cookie (FR-005, FR-006, FR-017)

### Auth Routes

- [x] T020 Create `backend/src/api/routes/__init__.py`
- [x] T021 Create `backend/src/api/routes/auth.py` - POST /api/auth/register (FR-001, FR-002, FR-003, US1)
- [x] T022 Update `backend/src/api/routes/auth.py` - POST /api/auth/login with JWT cookie (FR-004, FR-005, FR-006, US2)
- [x] T023 Update `backend/src/api/routes/auth.py` - POST /api/auth/logout clearing cookie (FR-007, US2)

### Auth Error Handling

- [x] T024 Create `backend/src/api/schemas/error.py` - ErrorResponse schema with detail and code (FR-021, FR-022)
- [x] T025 Update `backend/src/api/routes/auth.py` - Return 409 CONFLICT for duplicate email (FR-003)
- [x] T026 Update `backend/src/api/routes/auth.py` - Return 401 UNAUTHORIZED for invalid credentials (FR-018)
- [x] T027 Update `backend/src/api/routes/auth.py` - Return 400 VALIDATION_ERROR for invalid input (FR-021)

**Checkpoint**: Auth endpoints work via Swagger UI, JWT cookie is set on login

---

## Phase 4: Backend Task API - User Story 3, 4, 5, 6, 7 (P1/P2)

**Purpose**: Implement task CRUD with user isolation

**Spec References**: US3-US7, FR-009 to FR-020

### Task Schemas

- [x] T028 Create `backend/src/api/schemas/task.py` - TaskCreate (title required, description optional) (FR-009)
- [x] T029 Update `backend/src/api/schemas/task.py` - TaskUpdate (title optional, description optional) (FR-012)
- [x] T030 Update `backend/src/api/schemas/task.py` - TaskResponse with all fields (FR-022)

### Task Service

- [x] T031 Create `backend/src/services/task.py` - list_tasks() filtered by user_id (FR-011, US3)
- [x] T032 Update `backend/src/services/task.py` - get_task() with user_id check, return None if not owner (FR-011)
- [x] T033 Update `backend/src/services/task.py` - create_task() with user_id from JWT, is_completed=False (FR-009, FR-010, FR-015, FR-016, US4)
- [x] T034 Update `backend/src/services/task.py` - update_task() with ownership validation (FR-012, US5)
- [x] T035 Update `backend/src/services/task.py` - delete_task() with ownership validation (FR-013, US6)
- [x] T036 Update `backend/src/services/task.py` - toggle_task() flip is_completed with ownership validation (FR-014, US7)

### Task Routes

- [x] T037 Create `backend/src/api/routes/tasks.py` - GET /api/tasks list (FR-011, FR-017, US3)
- [x] T038 Update `backend/src/api/routes/tasks.py` - POST /api/tasks create (FR-009, FR-010, FR-017, US4)
- [x] T039 Update `backend/src/api/routes/tasks.py` - GET /api/tasks/{id} (FR-011, FR-017)
- [x] T040 Update `backend/src/api/routes/tasks.py` - PUT /api/tasks/{id} update (FR-012, FR-017, US5)
- [x] T041 Update `backend/src/api/routes/tasks.py` - DELETE /api/tasks/{id} (FR-013, FR-017, US6)
- [x] T042 Update `backend/src/api/routes/tasks.py` - PATCH /api/tasks/{id}/toggle (FR-014, FR-017, US7)

### Task Error Handling (Security)

- [x] T043 Update `backend/src/api/routes/tasks.py` - Return 401 for missing/invalid JWT (FR-018)
- [x] T044 Update `backend/src/api/routes/tasks.py` - Return 403 FORBIDDEN for accessing other user's task (FR-019)
- [x] T045 Update `backend/src/api/routes/tasks.py` - Return 404 NOT_FOUND for non-existent task (FR-020)
- [x] T046 Update `backend/src/api/routes/tasks.py` - Return 400 for validation errors (empty title) (FR-021)

### Main Application

- [x] T047 Create `backend/src/main.py` - FastAPI app with CORS, include auth and tasks routers (FR-022, FR-023)
- [x] T048 Update `backend/src/main.py` - Add startup event to create tables
- [x] T049 Update `backend/src/main.py` - Configure OpenAPI documentation (FR-023)

**Checkpoint**: All API endpoints work via Swagger UI, user isolation enforced

---

## Phase 5: Frontend Foundation (Setup)

**Purpose**: Next.js project initialization and core infrastructure

**Spec References**: Technical Constraints (Constitution), FR-024 to FR-030

### Setup Tasks

- [x] T050 Initialize Next.js 14+ project with App Router in `frontend/` using `npx create-next-app@latest`
- [x] T051 [P] Configure TypeScript strict mode in `frontend/tsconfig.json`
- [x] T052 [P] Set up Tailwind CSS in `frontend/tailwind.config.js`
- [x] T053 [P] Create `frontend/.env.local.example` with NEXT_PUBLIC_API_URL

### Type Definitions

- [x] T054 Create `frontend/src/types/index.ts` - User, Task, ErrorResponse types matching API schemas

### API Client

- [x] T055 Create `frontend/src/lib/api.ts` - Fetch wrapper with credentials:'include' for cookies (FR-006)
- [x] T056 Update `frontend/src/lib/api.ts` - Error handling transforming API errors to user messages

### Layouts

- [x] T057 Update `frontend/src/app/layout.tsx` - Root layout with global styles, Tailwind classes
- [x] T058 Create `frontend/src/app/page.tsx` - Home page redirecting to /dashboard or /login

**Checkpoint**: Frontend project runs with `npm run dev`

---

## Phase 6: Frontend Authentication - User Story 1 & 2 (P1)

**Purpose**: Implement registration and login UI

**Spec References**: US1, US2, FR-024, FR-025, FR-028, FR-029

### Auth Middleware

- [x] T059 Create `frontend/middleware.ts` - Redirect unauthenticated users from /dashboard to /login (FR-008)

### Auth Components

- [x] T060 Create `frontend/src/components/auth/RegisterForm.tsx` - Email, password fields, validation (FR-024, FR-028)
- [x] T061 Create `frontend/src/components/auth/LoginForm.tsx` - Email, password fields, validation (FR-025, FR-028)

### Auth Pages

- [x] T062 Create `frontend/src/app/(auth)/register/page.tsx` - Registration page with RegisterForm (US1)
- [x] T063 Create `frontend/src/app/(auth)/login/page.tsx` - Login page with LoginForm (US2)

### Auth API Integration

- [x] T064 Update `frontend/src/lib/api.ts` - register() function calling POST /api/auth/register (US1)
- [x] T065 Update `frontend/src/lib/api.ts` - login() function calling POST /api/auth/login (US2)
- [x] T066 Update `frontend/src/lib/api.ts` - logout() function calling POST /api/auth/logout (US2)

### Auth Flow

- [x] T067 Update `frontend/src/components/auth/RegisterForm.tsx` - Submit handler, success message, redirect to login (US1)
- [x] T068 Update `frontend/src/components/auth/LoginForm.tsx` - Submit handler, redirect to dashboard on success (US2)
- [x] T069 Update `frontend/src/components/auth/RegisterForm.tsx` - Display validation errors inline (FR-028)
- [x] T070 Update `frontend/src/components/auth/LoginForm.tsx` - Display error for invalid credentials (FR-028)
- [x] T071 Add loading states to RegisterForm and LoginForm (FR-029)

**Checkpoint**: User can register, login, and is redirected to dashboard

---

## Phase 7: Frontend Task Management - User Story 3, 4, 5, 6, 7 (P1/P2)

**Purpose**: Implement task dashboard with CRUD operations

**Spec References**: US3-US7, FR-026, FR-027, FR-028, FR-029, FR-030

### Dashboard Layout

- [x] T072 Create `frontend/src/app/dashboard/layout.tsx` - Protected layout with logout button
- [x] T073 Create `frontend/src/app/dashboard/page.tsx` - Task dashboard page (FR-026, US3)

### Task API Integration

- [x] T074 Update `frontend/src/lib/api.ts` - getTasks() function calling GET /api/tasks (US3)
- [x] T075 Update `frontend/src/lib/api.ts` - createTask() function calling POST /api/tasks (US4)
- [x] T076 Update `frontend/src/lib/api.ts` - updateTask() function calling PUT /api/tasks/{id} (US5)
- [x] T077 Update `frontend/src/lib/api.ts` - deleteTask() function calling DELETE /api/tasks/{id} (US6)
- [x] T078 Update `frontend/src/lib/api.ts` - toggleTask() function calling PATCH /api/tasks/{id}/toggle (US7)

### Task Components

- [x] T079 Create `frontend/src/components/tasks/TaskList.tsx` - Display task array or empty state (FR-026, US3)
- [x] T080 Create `frontend/src/components/tasks/TaskItem.tsx` - Single task with toggle, edit, delete buttons (FR-027, US3)
- [x] T081 Create `frontend/src/components/tasks/TaskForm.tsx` - Create/edit task form with title, description (FR-027, US4, US5)
- [x] T082 Create `frontend/src/components/tasks/DeleteConfirm.tsx` - Confirmation modal before delete (US6)

### Task Operations

- [x] T083 Update `frontend/src/app/dashboard/page.tsx` - Fetch and display tasks on load (US3)
- [x] T084 Update `frontend/src/app/dashboard/page.tsx` - Show "No tasks yet" empty state (US3)
- [x] T085 Update `frontend/src/components/tasks/TaskItem.tsx` - Visual distinction for completed tasks (US3)
- [x] T086 Update `frontend/src/app/dashboard/page.tsx` - Create task flow with TaskForm (US4)
- [x] T087 Update `frontend/src/components/tasks/TaskForm.tsx` - Validation error for empty title (FR-028, US4)
- [x] T088 Update `frontend/src/app/dashboard/page.tsx` - Edit task flow with TaskForm (US5)
- [x] T089 Update `frontend/src/app/dashboard/page.tsx` - Delete task flow with DeleteConfirm (US6)
- [x] T090 Update `frontend/src/components/tasks/TaskItem.tsx` - Toggle completion handler (US7)

### Loading and Error States

- [x] T091 Add loading states to dashboard during API calls (FR-029)
- [x] T092 Handle and display API errors on dashboard (network errors, 401 redirect) (FR-028)

**Checkpoint**: Full task management working - create, view, edit, delete, toggle

---

## Phase 8: Polish & Responsive Design (P2/P3)

**Purpose**: Mobile responsiveness and UX improvements

**Spec References**: FR-030, Success Criteria SC-008

### Responsive Design

- [ ] T093 [P] Update `frontend/src/components/auth/RegisterForm.tsx` - Mobile-friendly layout (FR-030)
- [ ] T094 [P] Update `frontend/src/components/auth/LoginForm.tsx` - Mobile-friendly layout (FR-030)
- [ ] T095 [P] Update `frontend/src/components/tasks/TaskList.tsx` - Mobile-friendly layout (FR-030)
- [ ] T096 [P] Update `frontend/src/components/tasks/TaskItem.tsx` - Touch-friendly buttons (FR-030)
- [ ] T097 [P] Update `frontend/src/components/tasks/TaskForm.tsx` - Mobile-friendly form (FR-030)

### Error Handling Enhancement

- [ ] T098 Create `frontend/src/components/ui/ErrorMessage.tsx` - Reusable error display component
- [ ] T099 Update all forms to use ErrorMessage component for consistent error display

**Checkpoint**: Application usable on mobile devices without horizontal scrolling

---

## Phase 9: Backend Testing

**Purpose**: Verify API behavior matches specification

**Spec References**: All FR requirements, Constitution compliance

### Test Setup

- [ ] T100 Create `backend/tests/__init__.py`
- [ ] T101 Create `backend/tests/conftest.py` - Pytest fixtures for test client, test database, test user

### Auth Integration Tests

- [ ] T102 Create `backend/tests/integration/test_auth.py` - Test POST /api/auth/register success (US1)
- [ ] T103 Update `backend/tests/integration/test_auth.py` - Test register with duplicate email returns 409 (US1, FR-003)
- [ ] T104 Update `backend/tests/integration/test_auth.py` - Test register with short password returns 400 (US1, FR-002)
- [ ] T105 Update `backend/tests/integration/test_auth.py` - Test POST /api/auth/login success (US2, FR-004)
- [ ] T106 Update `backend/tests/integration/test_auth.py` - Test login with wrong password returns 401 (US2, FR-018)
- [ ] T107 Update `backend/tests/integration/test_auth.py` - Test POST /api/auth/logout clears cookie (US2, FR-007)

### Task Integration Tests

- [ ] T108 Create `backend/tests/integration/test_tasks.py` - Test GET /api/tasks returns user's tasks only (US3, FR-011)
- [ ] T109 Update `backend/tests/integration/test_tasks.py` - Test POST /api/tasks creates task (US4, FR-009)
- [ ] T110 Update `backend/tests/integration/test_tasks.py` - Test create task without auth returns 401 (FR-017, FR-018)
- [ ] T111 Update `backend/tests/integration/test_tasks.py` - Test PUT /api/tasks/{id} updates task (US5, FR-012)
- [ ] T112 Update `backend/tests/integration/test_tasks.py` - Test update other user's task returns 403 (US5, FR-019)
- [ ] T113 Update `backend/tests/integration/test_tasks.py` - Test DELETE /api/tasks/{id} deletes task (US6, FR-013)
- [ ] T114 Update `backend/tests/integration/test_tasks.py` - Test delete non-existent task returns 404 (US6, FR-020)
- [ ] T115 Update `backend/tests/integration/test_tasks.py` - Test PATCH /api/tasks/{id}/toggle toggles status (US7, FR-014)
- [ ] T116 Update `backend/tests/integration/test_tasks.py` - Test toggle other user's task returns 403 (US7, FR-019)

**Checkpoint**: All backend tests pass

---

## Phase 10: Final Validation

**Purpose**: Constitution compliance review and final verification

**Spec References**: Constitution Compliance Review Checklist

### Compliance Verification

- [ ] T117 Verify all task endpoints require JWT authentication (except auth routes)
- [ ] T118 Verify backend extracts user ID from JWT only, never from request body
- [ ] T119 Verify 403 returned when accessing other user's tasks
- [ ] T120 Verify no secrets hardcoded in source code (check for .env usage)
- [ ] T121 Verify API responses follow standard error format {detail, code}
- [ ] T122 Verify frontend does not store user state between page loads (only from API)
- [ ] T123 Verify backend does not store session state in memory (JWT only)
- [ ] T124 Verify OpenAPI documentation at /docs is complete and accurate

### Manual E2E Testing

- [ ] T125 Test complete user journey: register → login → create tasks → edit → toggle → delete → logout
- [ ] T126 Test on mobile viewport (FR-030, SC-008)

**Checkpoint**: Phase II Complete - All acceptance criteria met

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Backend Setup)
    ↓
Phase 2 (Database Models) ←── BLOCKS all API work
    ↓
Phase 3 (Auth API) ←── BLOCKS task API and frontend auth
    ↓
Phase 4 (Task API) ←── BLOCKS frontend task features
    ↓
Phase 5 (Frontend Setup) [Can start after Phase 1]
    ↓
Phase 6 (Frontend Auth) ←── Requires Phase 3 complete
    ↓
Phase 7 (Frontend Tasks) ←── Requires Phase 4 complete
    ↓
Phase 8 (Polish) ←── Requires Phase 7 complete
    ↓
Phase 9 (Testing) [Can start after Phase 4]
    ↓
Phase 10 (Validation) ←── Requires all phases complete
```

### Parallel Opportunities

**Within Backend (after Phase 2):**
- T012-T013 (Auth schemas) can run parallel with T028-T030 (Task schemas)
- Auth tests can start after Phase 3

**Within Frontend (after Phase 5):**
- T060-T061 (Auth components) can run parallel with T079-T082 (Task components) if API mocks available
- T093-T097 (Responsive tasks) can all run in parallel

**Cross-cutting:**
- Backend testing (Phase 9) can run in parallel with frontend polish (Phase 8)

---

## Task Verification Matrix

| Task Range | User Story | Functional Requirements | Verifiable By |
|------------|------------|------------------------|---------------|
| T001-T011 | - | Constitution Tech Constraints | Import test |
| T012-T027 | US1, US2 | FR-001 to FR-008 | Swagger UI, Integration tests |
| T028-T049 | US3-US7 | FR-009 to FR-023 | Swagger UI, Integration tests |
| T050-T058 | - | FR-024 to FR-030 | npm run dev |
| T059-T071 | US1, US2 | FR-024, FR-025, FR-028, FR-029 | Manual browser test |
| T072-T092 | US3-US7 | FR-026 to FR-030 | Manual browser test |
| T093-T099 | - | FR-030 | Mobile viewport test |
| T100-T116 | All | All FR | pytest |
| T117-T126 | All | Constitution Compliance | Checklist review |

---

## Notes

- All tasks derive from spec.md, plan.md, and data-model.md
- No task introduces behavior not defined in specifications
- Each task is independently verifiable via stated verification method
- Tasks marked [P] can run in parallel within their phase
- Commit after each task or logical group for clear history
