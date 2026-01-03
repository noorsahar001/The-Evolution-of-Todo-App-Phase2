# Quickstart: Todo Full-Stack Web Application (Phase II)

**Feature Branch**: `002-todo-fullstack-webapp`
**Date**: 2025-12-30

## Prerequisites

### Required Software

- **Python**: 3.11 or higher
- **Node.js**: 18.x or higher
- **npm**: 9.x or higher (comes with Node.js)
- **Git**: Any recent version

### Required Accounts/Services

- **Neon**: Account for PostgreSQL database ([neon.tech](https://neon.tech))

## Environment Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd todo-app
git checkout 002-todo-fullstack-webapp
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Backend Environment Variables

Create `backend/.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# JWT Configuration
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
CORS_ORIGINS=http://localhost:3000
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory (from repo root)
cd frontend

# Install dependencies
npm install
```

### 5. Frontend Environment Variables

Create `frontend/.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`

API documentation at: `http://localhost:8000/docs`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Verification Steps

### 1. Verify Backend is Running

```bash
curl http://localhost:8000/docs
```

Should return HTML for Swagger UI.

### 2. Verify Database Connection

The backend logs should show:
```
INFO:     Application startup complete.
```

No database connection errors should appear.

### 3. Test Registration Flow

1. Open `http://localhost:3000/register`
2. Enter email: `test@example.com`
3. Enter password: `password123`
4. Submit form
5. Should see success message

### 4. Test Login Flow

1. Open `http://localhost:3000/login`
2. Enter credentials from step 3
3. Submit form
4. Should redirect to dashboard

### 5. Test Task Operations

1. On dashboard, create a new task
2. Verify task appears in list
3. Toggle completion status
4. Edit task title
5. Delete task

## Common Issues

### Database Connection Failed

**Symptom**: Backend fails to start with database error

**Solution**:
1. Verify `DATABASE_URL` in `.env` is correct
2. Check Neon dashboard for connection string
3. Ensure `?sslmode=require` is in the URL

### CORS Error in Browser

**Symptom**: Network errors when frontend calls backend

**Solution**:
1. Verify `CORS_ORIGINS` includes frontend URL
2. Ensure both services are running
3. Check browser console for specific error

### JWT Token Not Set

**Symptom**: Login succeeds but dashboard shows unauthorized

**Solution**:
1. Check browser cookies for `access_token`
2. Verify cookie settings (SameSite, Secure)
3. Ensure backend and frontend are on same domain in production

### Frontend Can't Find API

**Symptom**: "Unable to connect" errors

**Solution**:
1. Verify `NEXT_PUBLIC_API_URL` is set
2. Ensure backend is running on correct port
3. Check for typos in the URL

## Development Workflow

### Making Backend Changes

1. Edit files in `backend/src/`
2. Uvicorn auto-reloads on save
3. Test via Swagger UI at `/docs`

### Making Frontend Changes

1. Edit files in `frontend/src/`
2. Next.js hot-reloads on save
3. Test in browser

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests (if implemented)
cd frontend
npm test
```

## Production Deployment

### Backend

1. Set secure `JWT_SECRET` (random 32+ character string)
2. Configure `DATABASE_URL` for production database
3. Set `CORS_ORIGINS` to production frontend URL
4. Deploy behind HTTPS reverse proxy

### Frontend

1. Set `NEXT_PUBLIC_API_URL` to production backend URL
2. Build: `npm run build`
3. Deploy to Vercel, Netlify, or similar

## API Endpoints Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/register | No | Register new user |
| POST | /api/auth/login | No | Login user |
| POST | /api/auth/logout | Yes | Logout user |
| GET | /api/tasks | Yes | List all tasks |
| POST | /api/tasks | Yes | Create task |
| GET | /api/tasks/{id} | Yes | Get task |
| PUT | /api/tasks/{id} | Yes | Update task |
| DELETE | /api/tasks/{id} | Yes | Delete task |
| PATCH | /api/tasks/{id}/toggle | Yes | Toggle completion |

Full API documentation available at `http://localhost:8000/docs` when backend is running.
