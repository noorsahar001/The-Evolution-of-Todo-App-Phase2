# Data Model: Todo Full-Stack Web Application (Phase II)

**Feature Branch**: `002-todo-fullstack-webapp`
**Date**: 2025-12-30
**Status**: Complete

## Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│              User                   │
├─────────────────────────────────────┤
│ id: Integer (PK, auto-increment)    │
│ email: String(255) [unique, not null]│
│ hashed_password: String(255) [not null]│
│ created_at: Timestamp [default: now]│
└─────────────────────────────────────┘
                 │
                 │ 1:N (one user has many tasks)
                 ▼
┌─────────────────────────────────────┐
│              Task                   │
├─────────────────────────────────────┤
│ id: Integer (PK, auto-increment)    │
│ title: String(200) [not null]       │
│ description: Text(2000) [nullable]  │
│ is_completed: Boolean [default: false]│
│ user_id: Integer (FK → User.id)     │
│ created_at: Timestamp [default: now]│
│ updated_at: Timestamp [on update]   │
└─────────────────────────────────────┘
```

## Entity: User

Represents a registered user account in the system.

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| email | String(255) | UNIQUE, NOT NULL | User's email address for login |
| hashed_password | String(255) | NOT NULL | bcrypt-hashed password |
| created_at | Timestamp | NOT NULL, DEFAULT NOW() | Account creation timestamp |

### Validation Rules

- **email**: Must be valid email format (RFC 5322)
- **email**: Maximum 255 characters
- **email**: Must be unique across all users
- **password** (before hashing): Minimum 8 characters

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| pk_user | id | PRIMARY | Unique identifier |
| idx_user_email | email | UNIQUE | Login lookup |

## Entity: Task

Represents a todo item owned by a user.

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| title | String(200) | NOT NULL | Task title (required) |
| description | Text(2000) | NULLABLE | Optional task description |
| is_completed | Boolean | NOT NULL, DEFAULT FALSE | Completion status |
| user_id | Integer | FOREIGN KEY (User.id), NOT NULL | Task owner |
| created_at | Timestamp | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| updated_at | Timestamp | NOT NULL, ON UPDATE NOW() | Last modification timestamp |

### Validation Rules

- **title**: Required, not empty, maximum 200 characters
- **description**: Optional, maximum 2000 characters
- **user_id**: Must reference existing user
- **is_completed**: Boolean only (no null)

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| pk_task | id | PRIMARY | Unique identifier |
| idx_task_user | user_id | BTREE | Filter tasks by user |
| idx_task_user_id | user_id, id | BTREE | Ownership validation |

### Foreign Keys

| Constraint | Columns | References | On Delete |
|------------|---------|------------|-----------|
| fk_task_user | user_id | User(id) | CASCADE |

## Relationships

### User → Task (1:N)

- One user can have many tasks
- Each task belongs to exactly one user
- When a user is deleted, all their tasks are deleted (CASCADE)
- Tasks cannot exist without an owner

## State Transitions

### Task Completion State

```
┌──────────────┐    toggle()    ┌──────────────┐
│  Incomplete  │ ◄────────────► │   Complete   │
│ is_completed │                │ is_completed │
│   = false    │                │   = true     │
└──────────────┘                └──────────────┘
```

- New tasks start as incomplete (is_completed = false)
- Users can toggle between states
- No intermediate states exist

## Data Access Patterns

### User Operations

| Operation | Query Pattern | Auth Required |
|-----------|---------------|---------------|
| Register | INSERT User | No |
| Login | SELECT User WHERE email = ? | No |
| Get current user | SELECT User WHERE id = ? (from JWT) | Yes |

### Task Operations

| Operation | Query Pattern | Auth Required |
|-----------|---------------|---------------|
| List tasks | SELECT Task WHERE user_id = ? | Yes |
| Get task | SELECT Task WHERE id = ? AND user_id = ? | Yes |
| Create task | INSERT Task (user_id from JWT) | Yes |
| Update task | UPDATE Task WHERE id = ? AND user_id = ? | Yes |
| Delete task | DELETE Task WHERE id = ? AND user_id = ? | Yes |
| Toggle task | UPDATE Task SET is_completed = NOT is_completed WHERE id = ? AND user_id = ? | Yes |

## Data Ownership Enforcement

Per Constitution Principle VII (Security Principles):

1. **All task queries MUST include user_id filter**
   - Never query tasks by ID alone
   - Always: `WHERE id = ? AND user_id = ?`

2. **User ID source**
   - ALWAYS from JWT token
   - NEVER from request body or URL parameters

3. **Response for unauthorized access**
   - 403 Forbidden (not 404) to prevent enumeration

## Migration Strategy

### Initial Schema (Phase II)

1. Create `user` table
2. Create `task` table with foreign key
3. Add indexes

### SQL Schema (PostgreSQL)

```sql
-- Users table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tasks table
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX idx_task_user ON task(user_id);
CREATE INDEX idx_task_user_id ON task(user_id, id);
```

## Pydantic Schema Mapping

### User Schemas

```python
# Registration request
class UserCreate:
    email: str  # max 255, valid email
    password: str  # min 8 chars

# Login request
class UserLogin:
    email: str
    password: str

# User response (no password)
class UserResponse:
    id: int
    email: str
    created_at: datetime
```

### Task Schemas

```python
# Create request
class TaskCreate:
    title: str  # max 200, required
    description: str | None  # max 2000, optional

# Update request
class TaskUpdate:
    title: str | None  # max 200, optional
    description: str | None  # max 2000, optional

# Response
class TaskResponse:
    id: int
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime
```
