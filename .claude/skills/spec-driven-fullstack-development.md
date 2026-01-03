# Skill: Spec-Driven Full-Stack Web Development

A comprehensive skill for building full-stack web applications using Spec-Driven Development (SDD) methodology with API-first design principles.

---

## 1. Spec-Driven Full-Stack Architecture

### Overview
Full-stack SDD extends the specification methodology across all layers: frontend, backend, database, and infrastructure.

### Architecture Layers
```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                    │
│  Components │ Pages │ Hooks │ State │ API Client        │
├─────────────────────────────────────────────────────────┤
│                    API CONTRACTS                         │
│  OpenAPI Spec │ TypeScript Types │ Validation Schemas   │
├─────────────────────────────────────────────────────────┤
│                    BACKEND (FastAPI)                     │
│  Routes │ Services │ Models │ Auth │ Middleware         │
├─────────────────────────────────────────────────────────┤
│                    DATA LAYER                            │
│  ORM Models │ Migrations │ Database (PostgreSQL)        │
└─────────────────────────────────────────────────────────┘
```

### Full-Stack Specification Structure
```
specs/<feature>/
├── spec.md              # Feature requirements
├── plan.md              # Architecture decisions
├── tasks.md             # Implementation tasks
├── api-contract.yaml    # OpenAPI specification
├── db-schema.md         # Database design
└── ui-wireframes.md     # Frontend design
```

### Technology Stack (Reference)
| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Next.js 14+ | React framework with App Router |
| Backend | FastAPI | Python async API framework |
| Database | PostgreSQL (Neon) | Serverless PostgreSQL |
| Auth | Better Auth + JWT | Authentication library |
| ORM | SQLAlchemy / Drizzle | Database abstraction |
| Validation | Pydantic / Zod | Schema validation |

---

## 2. API-First Design Using Specifications

### Principles
1. **Contract First**: Define API before implementation
2. **Single Source of Truth**: OpenAPI spec drives both ends
3. **Type Safety**: Generate types from specifications
4. **Documentation**: Auto-generate API docs from spec

### API Specification Workflow
```
1. Define Requirements (spec.md)
        ↓
2. Design API Contract (api-contract.yaml)
        ↓
3. Generate Types (TypeScript + Python)
        ↓
4. Implement Backend (FastAPI routes)
        ↓
5. Implement Frontend (API client)
        ↓
6. Validate Contract (integration tests)
```

### API Design Document Template
```markdown
# API Design: [Feature Name]

## Overview
[Purpose of this API]

## Base URL
- Development: `http://localhost:8000/api/v1`
- Production: `https://api.example.com/v1`

## Authentication
- Type: Bearer Token (JWT)
- Header: `Authorization: Bearer <token>`

## Endpoints Summary
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /resources | List all resources |
| POST   | /resources | Create resource |
| GET    | /resources/{id} | Get single resource |
| PUT    | /resources/{id} | Update resource |
| DELETE | /resources/{id} | Delete resource |

## Rate Limiting
- Authenticated: 1000 req/hour
- Unauthenticated: 100 req/hour
```

---

## 3. RESTful API Specification

### OpenAPI 3.0 Template
```yaml
openapi: 3.0.3
info:
  title: [API Name]
  description: [API Description]
  version: 1.0.0

servers:
  - url: http://localhost:8000/api/v1
    description: Development
  - url: https://api.example.com/v1
    description: Production

paths:
  /tasks:
    get:
      summary: List all tasks
      operationId: listTasks
      tags:
        - Tasks
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, completed, all]
          required: false
        - name: limit
          in: query
          schema:
            type: integer
            default: 50
            maximum: 100
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskList'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create a new task
      operationId: createTask
      tags:
        - Tasks
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          $ref: '#/components/responses/ValidationError'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /tasks/{taskId}:
    parameters:
      - name: taskId
        in: path
        required: true
        schema:
          type: integer

    get:
      summary: Get task by ID
      operationId: getTask
      tags:
        - Tasks
      responses:
        '200':
          description: Task details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      summary: Update task
      operationId: updateTask
      tags:
        - Tasks
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
      responses:
        '200':
          description: Task updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      summary: Delete task
      operationId: deleteTask
      tags:
        - Tasks
      security:
        - bearerAuth: []
      responses:
        '204':
          description: Task deleted
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Task:
      type: object
      required:
        - id
        - title
        - completed
        - created_at
      properties:
        id:
          type: integer
          example: 1
        title:
          type: string
          example: "Buy groceries"
        description:
          type: string
          nullable: true
        completed:
          type: boolean
          default: false
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
          nullable: true

    TaskCreate:
      type: object
      required:
        - title
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 1000

    TaskUpdate:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 1000
        completed:
          type: boolean

    TaskList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Task'
        total:
          type: integer
        limit:
          type: integer
        offset:
          type: integer

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "UNAUTHORIZED"
            message: "Authentication required"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "NOT_FOUND"
            message: "Resource not found"

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "VALIDATION_ERROR"
            message: "Invalid input"
            details:
              field: "title"
              error: "Required field"
```

### FastAPI Implementation Pattern
```python
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Pydantic Models (match OpenAPI schemas)
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class TaskList(BaseModel):
    items: list[Task]
    total: int
    limit: int
    offset: int

# Routes
@router.get("", response_model=TaskList)
async def list_tasks(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all tasks with optional filtering."""
    pass

@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task."""
    pass

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a task by ID."""
    pass

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task."""
    pass

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task."""
    pass
```

---

## 4. Authentication & Authorization (JWT)

### Auth Specification Template
```markdown
# Authentication Specification

## Overview
JWT-based authentication with Better Auth integration.

## Auth Flows

### Registration
1. User submits email + password
2. Server validates input
3. Server hashes password (bcrypt)
4. Server creates user record
5. Server returns JWT tokens

### Login
1. User submits credentials
2. Server validates credentials
3. Server generates access + refresh tokens
4. Client stores tokens securely

### Token Refresh
1. Client sends refresh token
2. Server validates refresh token
3. Server issues new access token

## Token Structure
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234571490,
  "type": "access"
}
```

## Security Requirements
- Access token expiry: 15 minutes
- Refresh token expiry: 7 days
- Password: min 8 chars, mixed case + number
- Rate limit: 5 failed attempts / 15 min
```

### JWT Implementation (FastAPI)
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuration
SECRET_KEY = "your-secret-key"  # Use env variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Models
class TokenPayload(BaseModel):
    sub: str
    email: str
    type: str
    exp: datetime

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Password utilities
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Token utilities
def create_token(data: dict, token_type: str, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_token_pair(user_id: str, email: str) -> TokenPair:
    access_token = create_token(
        {"sub": user_id, "email": email},
        "access",
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"sub": user_id, "email": email},
        "refresh",
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return TokenPair(access_token=access_token, refresh_token=refresh_token)

def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# Dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)

    if payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user = db.query(User).filter(User.id == payload.sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

### Auth Routes
```python
router = APIRouter(prefix="/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", response_model=TokenPair)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check existing user
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    user = User(
        email=request.email,
        password_hash=hash_password(request.password),
        name=request.name
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return create_token_pair(str(user.id), user.email)

@router.post("/login", response_model=TokenPair)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return create_token_pair(str(user.id), user.email)

@router.post("/refresh", response_model=TokenPair)
async def refresh(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_token(credentials.credentials)

    if payload.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user = db.query(User).filter(User.id == payload.sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return create_token_pair(str(user.id), user.email)
```

---

## 5. Frontend ↔ Backend Contract Design

### Type Generation Workflow
```
OpenAPI Spec (YAML)
        ↓
    openapi-typescript
        ↓
TypeScript Types (frontend)
        ↓
API Client (type-safe fetch)
```

### Generated Types Example
```typescript
// types/api.ts (generated from OpenAPI)
export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface TaskList {
  items: Task[];
  total: number;
  limit: number;
  offset: number;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}
```

### Type-Safe API Client
```typescript
// lib/api-client.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private token: string | null = null;

  setToken(token: string | null) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new ApiClientError(error.message, error.code, response.status);
    }

    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  // Tasks API
  tasks = {
    list: (params?: { status?: string; limit?: number; offset?: number }) =>
      this.request<TaskList>(`/tasks?${new URLSearchParams(params as any)}`),

    get: (id: number) =>
      this.request<Task>(`/tasks/${id}`),

    create: (data: TaskCreate) =>
      this.request<Task>('/tasks', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    update: (id: number, data: TaskUpdate) =>
      this.request<Task>(`/tasks/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),

    delete: (id: number) =>
      this.request<void>(`/tasks/${id}`, { method: 'DELETE' }),
  };

  // Auth API
  auth = {
    login: (email: string, password: string) =>
      this.request<TokenPair>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }),

    register: (email: string, password: string, name: string) =>
      this.request<TokenPair>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, name }),
      }),

    refresh: (refreshToken: string) =>
      this.request<TokenPair>('/auth/refresh', {
        method: 'POST',
        headers: { Authorization: `Bearer ${refreshToken}` },
      }),
  };
}

export const apiClient = new ApiClient();
```

### React Query Integration
```typescript
// hooks/useTasks.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import type { Task, TaskCreate, TaskUpdate } from '@/types/api';

export function useTasks(status?: string) {
  return useQuery({
    queryKey: ['tasks', { status }],
    queryFn: () => apiClient.tasks.list({ status }),
  });
}

export function useTask(id: number) {
  return useQuery({
    queryKey: ['tasks', id],
    queryFn: () => apiClient.tasks.get(id),
    enabled: !!id,
  });
}

export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: TaskCreate) => apiClient.tasks.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });
}

export function useUpdateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: TaskUpdate }) =>
      apiClient.tasks.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['tasks', id] });
    },
  });
}

export function useDeleteTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.tasks.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });
}
```

---

## 6. Database Schema Design via Specs

### Schema Specification Template
```markdown
# Database Schema: [Feature Name]

## Overview
[Purpose and scope of this schema]

## Entity Relationship Diagram
```
┌──────────────┐       ┌──────────────┐
│    users     │       │    tasks     │
├──────────────┤       ├──────────────┤
│ id (PK)      │──────<│ id (PK)      │
│ email        │       │ user_id (FK) │
│ name         │       │ title        │
│ password_hash│       │ description  │
│ created_at   │       │ completed    │
│ updated_at   │       │ created_at   │
└──────────────┘       │ updated_at   │
                       └──────────────┘
```

## Tables

### users
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Primary key |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| name | VARCHAR(100) | NOT NULL | Display name |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hash |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NULL | Last update |

### tasks
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Primary key |
| user_id | UUID | FK → users.id, NOT NULL | Owner |
| title | VARCHAR(200) | NOT NULL | Task title |
| description | TEXT | NULL | Task details |
| completed | BOOLEAN | DEFAULT false | Status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NULL | Last update |

## Indexes
- `idx_tasks_user_id` ON tasks(user_id)
- `idx_tasks_completed` ON tasks(user_id, completed)
- `idx_users_email` ON users(email)

## Constraints
- `chk_task_title_length`: LENGTH(title) >= 1
```

### SQLAlchemy Models
```python
# models/base.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://user:pass@host/db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# models/user.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
```

```python
# models/task.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="tasks")

    # Indexes
    __table_args__ = (
        Index('idx_tasks_user_id', 'user_id'),
        Index('idx_tasks_completed', 'user_id', 'completed'),
    )
```

### Migration with Alembic
```python
# migrations/versions/001_initial.py
"""Initial migration

Revision ID: 001
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = '001'
down_revision = None

def upgrade():
    # Users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
    )
    op.create_index('idx_users_email', 'users', ['email'])

    # Tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('completed', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['user_id', 'completed'])

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
```

---

## 7. Migration from CLI → Web App

### Migration Strategy
```markdown
# CLI to Web Migration Plan

## Phase 1: Analyze CLI Structure
- [ ] Document all CLI commands
- [ ] Map commands to API endpoints
- [ ] Identify data models
- [ ] List business logic

## Phase 2: Design API Layer
- [ ] Create OpenAPI specification
- [ ] Map CLI commands → REST endpoints
- [ ] Design request/response schemas
- [ ] Plan authentication layer

## Phase 3: Extract Core Logic
- [ ] Separate I/O from business logic
- [ ] Create service layer
- [ ] Add dependency injection
- [ ] Write unit tests for services

## Phase 4: Build API
- [ ] Implement FastAPI routes
- [ ] Add authentication
- [ ] Connect to database
- [ ] Integration tests

## Phase 5: Build Frontend
- [ ] Create Next.js project
- [ ] Implement API client
- [ ] Build UI components
- [ ] E2E tests
```

### Command to Endpoint Mapping
```markdown
| CLI Command | HTTP Method | Endpoint | Notes |
|-------------|-------------|----------|-------|
| `add <task>` | POST | /api/v1/tasks | Create task |
| `list` | GET | /api/v1/tasks | List all |
| `list --status done` | GET | /api/v1/tasks?status=completed | Filter |
| `view <id>` | GET | /api/v1/tasks/{id} | Get one |
| `update <id> --title` | PUT | /api/v1/tasks/{id} | Update |
| `done <id>` | PUT | /api/v1/tasks/{id} | Mark complete |
| `delete <id>` | DELETE | /api/v1/tasks/{id} | Remove |
```

### Service Layer Extraction
```python
# BEFORE: CLI with embedded logic
# cli.py
def add_command(args):
    if not args.title:
        print("Error: Title required")
        return 1
    task = {"id": next_id(), "title": args.title, "completed": False}
    tasks.append(task)
    print(f"Created task {task['id']}")
    return 0

# AFTER: Separated service layer
# services/task_service.py
from dataclasses import dataclass
from typing import Optional
from models import Task
from repositories import TaskRepository

@dataclass
class TaskService:
    repository: TaskRepository

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create a new task. Raises ValidationError if invalid."""
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty")

        task = Task(title=title.strip(), description=description)
        return self.repository.save(task)

    def list_tasks(self, user_id: str, status: Optional[str] = None) -> list[Task]:
        """List tasks with optional status filter."""
        return self.repository.find_by_user(user_id, status=status)

    def complete_task(self, task_id: int, user_id: str) -> Task:
        """Mark a task as completed."""
        task = self.repository.find_by_id(task_id)
        if not task or task.user_id != user_id:
            raise NotFoundError(f"Task {task_id} not found")

        task.completed = True
        return self.repository.save(task)
```

```python
# CLI uses service
# cli.py
from services import TaskService

def add_command(args):
    try:
        task = task_service.create_task(args.title)
        print(f"Created task {task.id}")
        return 0
    except ValidationError as e:
        print(f"Error: {e.message}")
        return 1

# API uses same service
# routes/tasks.py
@router.post("", response_model=TaskResponse)
async def create_task(
    request: TaskCreate,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.create_task(request.title, request.description)
```

---

## 8. Claude Code for Full-Stack Generation

### Project Scaffolding Prompt
```markdown
Generate a full-stack project structure for a [App Name] with:

Backend (FastAPI):
- `/backend/app/main.py` - FastAPI application
- `/backend/app/routes/` - API route handlers
- `/backend/app/models/` - SQLAlchemy models
- `/backend/app/schemas/` - Pydantic schemas
- `/backend/app/services/` - Business logic
- `/backend/app/auth/` - JWT authentication
- `/backend/app/database.py` - Database config

Frontend (Next.js):
- `/frontend/app/` - App router pages
- `/frontend/components/` - React components
- `/frontend/lib/` - API client, utilities
- `/frontend/hooks/` - Custom React hooks
- `/frontend/types/` - TypeScript types

Follow the OpenAPI spec in `specs/api-contract.yaml`
```

### Component Generation Pattern
```markdown
## Request
Generate a TaskList component that:
1. Fetches tasks using the useTasks hook
2. Displays loading and error states
3. Shows empty state when no tasks
4. Renders TaskItem for each task
5. Supports filtering by status

## Expected Output Structure
```typescript
// components/TaskList.tsx
'use client';

import { useTasks } from '@/hooks/useTasks';
import { TaskItem } from './TaskItem';
import { TaskListSkeleton } from './TaskListSkeleton';

interface TaskListProps {
  status?: 'pending' | 'completed' | 'all';
}

export function TaskList({ status }: TaskListProps) {
  const { data, isLoading, error } = useTasks(status);

  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorMessage error={error} />;
  if (!data?.items.length) return <EmptyState />;

  return (
    <ul className="space-y-2">
      {data.items.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </ul>
  );
}
```
```

### Full-Stack Feature Implementation
```markdown
## Implementation Checklist

### Backend Tasks
- [ ] Create Pydantic schemas matching OpenAPI
- [ ] Implement SQLAlchemy model
- [ ] Write database migration
- [ ] Create service layer with business logic
- [ ] Implement API route handlers
- [ ] Add authentication guards
- [ ] Write API tests

### Frontend Tasks
- [ ] Generate TypeScript types from OpenAPI
- [ ] Implement API client methods
- [ ] Create React Query hooks
- [ ] Build UI components
- [ ] Add form validation (Zod)
- [ ] Handle loading/error states
- [ ] Write component tests

### Integration
- [ ] Verify contract compliance
- [ ] Run E2E tests
- [ ] Update API documentation
```

### Validation Commands
```bash
# Backend
cd backend
python -m pytest tests/ -v --cov=app
python -m mypy app/

# Frontend
cd frontend
npm run type-check
npm run test
npm run lint

# E2E
npm run test:e2e

# Contract validation
npx openapi-typescript-codegen \
  --input specs/api-contract.yaml \
  --output frontend/types/generated
```

---

## Quick Reference

### Full-Stack SDD Workflow
```
1. /sp.specify    → Define feature requirements
2. Design API     → Write OpenAPI spec
3. /sp.plan       → Architecture decisions
4. /sp.tasks      → Break into tasks
5. Generate Types → OpenAPI → TypeScript
6. /sp.implement  → Backend → Frontend
7. /sp.analyze    → Validate alignment
```

### Key Files
| File | Purpose |
|------|---------|
| `spec.md` | Feature requirements |
| `api-contract.yaml` | OpenAPI specification |
| `db-schema.md` | Database design |
| `plan.md` | Architecture decisions |
| `tasks.md` | Implementation tasks |

### Technology Quick Commands
```bash
# FastAPI dev server
uvicorn app.main:app --reload

# Next.js dev server
npm run dev

# Generate types from OpenAPI
npx openapi-typescript api-contract.yaml -o types/api.ts

# Run migrations
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "description"
```
