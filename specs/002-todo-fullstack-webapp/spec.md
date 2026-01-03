# Feature Specification: Todo Full-Stack Web Application (Phase II)

**Feature Branch**: `002-todo-fullstack-webapp`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Phase II Todo Full-Stack Web Application"

## System Overview

Phase II transforms the Phase I CLI application into a modern, multi-user web application with separate frontend and backend services.

### Architecture

- **Frontend**: A server-rendered web application providing the user interface for authentication and task management
- **Backend**: A RESTful API service handling authentication, business logic, and data persistence
- **Database**: A managed PostgreSQL service for persistent storage
- **Authentication**: JWT-based stateless authentication via Better Auth

### Communication Flow

```
User Browser → Frontend (Next.js) → Backend API (FastAPI) → Database (PostgreSQL)
                    ↓                        ↓
              JWT stored in           JWT validated on
              httpOnly cookie         every request
```

## User Scenarios & Testing

### User Story 1 - User Registration (Priority: P1)

A new user wants to create an account to start managing their personal tasks.

**Why this priority**: Registration is the entry point for all new users. Without it, no other features can be accessed.

**Independent Test**: A user can register, receive confirmation, and be redirected to login without requiring any other feature.

**Acceptance Scenarios**:

1. **Given** a visitor is on the registration page, **When** they enter a valid email and password (minimum 8 characters), **Then** their account is created and they see a success message with a link to login
2. **Given** a visitor submits a registration form, **When** the email is already registered, **Then** they see an error message "Email already exists"
3. **Given** a visitor submits a registration form, **When** the password is less than 8 characters, **Then** they see a validation error "Password must be at least 8 characters"
4. **Given** a visitor submits a registration form, **When** the email format is invalid, **Then** they see a validation error "Invalid email format"

---

### User Story 2 - User Login and Logout (Priority: P1)

A registered user wants to log in to access their tasks and log out when finished.

**Why this priority**: Login is required to access any protected functionality. Critical path for all authenticated features.

**Independent Test**: A user can log in with valid credentials, see they are authenticated, and log out successfully.

**Acceptance Scenarios**:

1. **Given** a registered user is on the login page, **When** they enter valid credentials, **Then** they are authenticated and redirected to the task dashboard
2. **Given** a user enters credentials, **When** the email does not exist, **Then** they see an error "Invalid email or password"
3. **Given** a user enters credentials, **When** the password is incorrect, **Then** they see an error "Invalid email or password" (same message for security)
4. **Given** an authenticated user, **When** they click logout, **Then** their session is terminated and they are redirected to the login page
5. **Given** an unauthenticated user, **When** they try to access the dashboard, **Then** they are redirected to the login page

---

### User Story 3 - View Task List (Priority: P1)

An authenticated user wants to see all their tasks in one place.

**Why this priority**: Viewing tasks is the core value proposition. Users need to see their tasks before they can manage them.

**Independent Test**: After logging in, a user can see a list of their tasks (or an empty state message if none exist).

**Acceptance Scenarios**:

1. **Given** an authenticated user with tasks, **When** they access the dashboard, **Then** they see a list of all their tasks showing title, description (if any), and completion status
2. **Given** an authenticated user with no tasks, **When** they access the dashboard, **Then** they see an empty state message "No tasks yet. Create your first task!"
3. **Given** an authenticated user, **When** viewing tasks, **Then** they only see tasks they own (not tasks from other users)
4. **Given** an authenticated user, **When** viewing a task list, **Then** completed tasks are visually distinguished from incomplete tasks

---

### User Story 4 - Create New Task (Priority: P2)

An authenticated user wants to add a new task to their list.

**Why this priority**: Creating tasks is essential but depends on having a visible task list to confirm creation.

**Independent Test**: A user can create a task and immediately see it appear in their task list.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the dashboard, **When** they enter a task title and click "Add Task", **Then** the task is created and appears in their list
2. **Given** an authenticated user, **When** they create a task with title and description, **Then** both are saved and displayed
3. **Given** an authenticated user, **When** they submit a task with an empty title, **Then** they see a validation error "Task title is required"
4. **Given** an authenticated user, **When** they create a task, **Then** the new task is marked as incomplete by default

---

### User Story 5 - Update Existing Task (Priority: P2)

An authenticated user wants to modify the title or description of an existing task.

**Why this priority**: Users need to correct mistakes or update task details as circumstances change.

**Independent Test**: A user can edit a task's title and/or description and see the changes reflected immediately.

**Acceptance Scenarios**:

1. **Given** an authenticated user viewing their tasks, **When** they click edit on a task and change the title, **Then** the updated title is saved and displayed
2. **Given** an authenticated user, **When** they update a task description, **Then** the change is persisted
3. **Given** an authenticated user, **When** they try to update with an empty title, **Then** they see a validation error
4. **Given** an authenticated user, **When** they try to update another user's task, **Then** they receive a 403 Forbidden error

---

### User Story 6 - Delete Task (Priority: P2)

An authenticated user wants to remove a task they no longer need.

**Why this priority**: Users need to clean up completed or irrelevant tasks.

**Independent Test**: A user can delete a task and confirm it no longer appears in their list.

**Acceptance Scenarios**:

1. **Given** an authenticated user viewing their tasks, **When** they click delete on a task and confirm, **Then** the task is removed from their list
2. **Given** an authenticated user, **When** they delete a task, **Then** a confirmation prompt appears before deletion
3. **Given** an authenticated user, **When** they try to delete another user's task, **Then** they receive a 403 Forbidden error
4. **Given** an authenticated user, **When** they try to delete a non-existent task, **Then** they receive a 404 Not Found error

---

### User Story 7 - Toggle Task Completion (Priority: P2)

An authenticated user wants to mark tasks as complete or incomplete.

**Why this priority**: Tracking completion status is core to task management value.

**Independent Test**: A user can toggle a task's completion status and see the visual change immediately.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an incomplete task, **When** they click the completion toggle, **Then** the task is marked as complete with visual feedback
2. **Given** an authenticated user with a complete task, **When** they click the completion toggle, **Then** the task is marked as incomplete
3. **Given** an authenticated user, **When** they toggle completion on another user's task, **Then** they receive a 403 Forbidden error

---

### Edge Cases

- What happens when a user's session expires mid-operation? → The operation fails with 401 and user is redirected to login
- How does the system handle concurrent updates to the same task? → Last write wins (standard behavior for this scope)
- What happens if the backend is unreachable? → Frontend displays a user-friendly error "Unable to connect. Please try again."
- What is the maximum length for task titles? → 200 characters (reasonable default)
- What is the maximum length for task descriptions? → 2000 characters (reasonable default)

## Requirements

### Functional Requirements

#### Authentication

- **FR-001**: System MUST allow users to register with email and password
- **FR-002**: System MUST enforce password minimum length of 8 characters
- **FR-003**: System MUST prevent duplicate email registrations
- **FR-004**: System MUST allow registered users to log in with email and password
- **FR-005**: System MUST issue a JWT token upon successful login
- **FR-006**: System MUST store JWT in httpOnly cookie (not accessible via JavaScript)
- **FR-007**: System MUST allow authenticated users to log out, clearing their session
- **FR-008**: System MUST redirect unauthenticated users to login when accessing protected routes

#### Task Management

- **FR-009**: System MUST allow authenticated users to create tasks with title (required) and description (optional)
- **FR-010**: System MUST associate each task with the creating user (owner)
- **FR-011**: System MUST allow users to view only their own tasks
- **FR-012**: System MUST allow users to update only their own tasks
- **FR-013**: System MUST allow users to delete only their own tasks
- **FR-014**: System MUST allow users to toggle completion status only on their own tasks
- **FR-015**: System MUST auto-generate unique IDs for tasks
- **FR-016**: System MUST set new tasks as incomplete by default

#### REST API

- **FR-017**: All task endpoints MUST require valid JWT authentication
- **FR-018**: API MUST return 401 Unauthorized for missing or invalid JWT
- **FR-019**: API MUST return 403 Forbidden when accessing another user's task
- **FR-020**: API MUST return 404 Not Found for non-existent task IDs
- **FR-021**: API MUST return 400 Bad Request for validation errors with descriptive messages
- **FR-022**: API MUST return responses in JSON format
- **FR-023**: API MUST provide OpenAPI/Swagger documentation

#### User Interface

- **FR-024**: Frontend MUST display a registration form with email and password fields
- **FR-025**: Frontend MUST display a login form with email and password fields
- **FR-026**: Frontend MUST display a task dashboard showing all user tasks
- **FR-027**: Frontend MUST provide controls to create, edit, delete, and toggle tasks
- **FR-028**: Frontend MUST display inline validation errors
- **FR-029**: Frontend MUST show loading states during API operations
- **FR-030**: Frontend MUST be responsive (usable on mobile and desktop)

### Key Entities

- **User**: Represents a registered account. Key attributes: unique identifier, email (unique), hashed password, created timestamp.
- **Task**: Represents a todo item. Key attributes: unique identifier, title (required, max 200 chars), description (optional, max 2000 chars), completion status (boolean), owner (reference to User), created timestamp, updated timestamp.

## REST API Endpoints

### Authentication Endpoints (Public)

| Method | Endpoint           | Description       | Request Body         | Success Response       |
|--------|--------------------|-------------------|----------------------|------------------------|
| POST   | /api/auth/register | Register new user | `{email, password}`  | 201 Created            |
| POST   | /api/auth/login    | Authenticate user | `{email, password}`  | 200 OK + JWT cookie    |
| POST   | /api/auth/logout   | End session       | None                 | 200 OK (clears cookie) |

### Task Endpoints (Protected - JWT Required)

| Method | Endpoint              | Description       | Request Body              | Success Response    |
|--------|-----------------------|-------------------|---------------------------|---------------------|
| GET    | /api/tasks            | List user's tasks | None                      | 200 OK + task array |
| POST   | /api/tasks            | Create new task   | `{title, description?}`   | 201 Created + task  |
| GET    | /api/tasks/{id}       | Get single task   | None                      | 200 OK + task       |
| PUT    | /api/tasks/{id}       | Update task       | `{title?, description?}`  | 200 OK + task       |
| DELETE | /api/tasks/{id}       | Delete task       | None                      | 204 No Content      |
| PATCH  | /api/tasks/{id}/toggle | Toggle completion | None                      | 200 OK + task       |

### Error Response Format

All error responses follow this structure:

```json
{
  "detail": "Human-readable error message",
  "code": "ERROR_CODE"
}
```

Error codes include: `VALIDATION_ERROR`, `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `CONFLICT`, `INTERNAL_ERROR`

## Data Ownership Rules

1. Every task MUST have exactly one owner (the user who created it)
2. Users can only perform operations on tasks they own
3. The backend MUST extract the user ID from the JWT token, never from request parameters
4. Attempting to access another user's task MUST return 403 Forbidden
5. Task listings MUST be filtered by the authenticated user's ID

## Error Handling Behavior

| HTTP Status      | When                                              | User Message                                         |
|------------------|---------------------------------------------------|------------------------------------------------------|
| 400 Bad Request  | Validation fails (empty title, invalid email)     | Specific validation error                            |
| 401 Unauthorized | No JWT, expired JWT, invalid JWT                  | "Please log in to continue"                          |
| 403 Forbidden    | User tries to access/modify another user's task   | "You don't have permission to access this resource"  |
| 404 Not Found    | Task ID doesn't exist                             | "Task not found"                                     |
| 409 Conflict     | Email already registered                          | "Email already exists"                               |
| 500 Internal     | Unexpected server error                           | "Something went wrong. Please try again."            |

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can complete registration in under 30 seconds
- **SC-002**: Users can complete login in under 10 seconds
- **SC-003**: Task list loads within 2 seconds for up to 100 tasks
- **SC-004**: Users can create a task in under 5 seconds (from click to confirmation)
- **SC-005**: System supports 100 concurrent users without degradation
- **SC-006**: 99% of API requests complete successfully under normal load
- **SC-007**: All form validation errors are displayed within 500ms
- **SC-008**: Users can manage tasks on mobile devices without horizontal scrolling

## Assumptions

1. **Password Storage**: Passwords will be hashed using industry-standard algorithms (not stored in plain text)
2. **Session Duration**: JWT tokens expire after a reasonable duration (implementation to define exact time)
3. **Email Validation**: Email format validation only; no email verification/confirmation flow in Phase II
4. **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
5. **Network**: Users have stable internet connectivity; offline mode is not supported
6. **Data Retention**: Task data is retained indefinitely until user deletes it
7. **Localization**: English only for Phase II

## Out of Scope

As defined in the Phase II Constitution, the following are explicitly excluded:

- AI or chatbot features
- Task sharing between users
- Task categories, tags, or labels
- Due dates, reminders, or notifications
- Task priorities or ordering
- Mobile native applications
- Docker, Kubernetes, or cloud deployment configurations
- Third-party OAuth providers
- Email verification or password reset flows
- Rate limiting or throttling
- Caching layers
