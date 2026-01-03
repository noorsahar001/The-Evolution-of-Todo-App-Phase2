---
id: 002
title: Phase II Constitution Ratification
stage: constitution
date: 2025-12-30
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: main
user: system
command: /sp.constitution
labels: ["constitution", "phase-ii", "full-stack", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

Define the Phase II Constitution for the Todo application.

Context:
- Phase I CLI app is complete.
- Phase II transforms the app into a full-stack, multi-user web application.
- Spec-driven development is mandatory.

Must include:
- Purpose of Phase II
- Scope (what is included and excluded)
- Technology constraints:
  - Frontend: Next.js (App Router)
  - Backend: FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Auth: Better Auth with JWT
- Security principles (JWT required on all endpoints)
- Rules:
  - No assumptions outside specs
  - All changes must go through specs
  - Backend must enforce user isolation
  - Frontend and backend must remain stateless

Output:
A clear Phase II constitution document that governs all specs and implementations.

## Response snapshot

Created Phase II constitution (v2.0.0) at `.specify/memory/constitution.md` with:

**9 Core Principles:**
1. Spec-Driven Development (NON-NEGOTIABLE)
2. In-Scope Features - User auth, per-user task CRUD, REST API, web interface
3. Exclusions - AI features, task sharing, priorities, mobile apps, cloud deployment
4. Task Rules & Validation - HTTP error codes, no stack trace exposure
5. Data Storage Rules - Neon PostgreSQL, SQLModel ORM, user isolation
6. Simplicity & YAGNI
7. Security Principles (NON-NEGOTIABLE) - JWT on all endpoints, user isolation, no frontend trust
8. Statelessness Requirements (NON-NEGOTIABLE) - No in-memory state on frontend or backend
9. API Contract Rules - OpenAPI/Swagger, Pydantic schemas, consistent error format

**Technical Constraints:**
- Frontend: Next.js 14+ (App Router), TypeScript, Tailwind CSS
- Backend: FastAPI, Python 3.11+, SQLModel, Pydantic v2, Better Auth
- Database: Neon Serverless PostgreSQL
- Testing: pytest, Jest (if requested)

**Project Structure:** Defined backend/ and frontend/ directory hierarchies with clear separation.

**Governance:** Semantic versioning, amendment procedures, compliance checklist.

## Outcome

- Impact: MAJOR version bump (1.0.0 → 2.0.0) establishing Phase II governance
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md
- Next prompts: Create feature specs for authentication, task-api, frontend-dashboard
- Reflection: Phase II constitution successfully captures all user requirements for full-stack transformation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
