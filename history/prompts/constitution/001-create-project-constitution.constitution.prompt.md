---
id: 001
title: Create Project Constitution
stage: constitution
date: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-auth-jwt
user: eraj_naz
command: /sp.constitution
labels: ["governance", "standards", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution

Project: Todo Full-Stack Web Application (Spec-Driven, Hackathon Phase-2)

Core principles:
- Spec-driven development (spec → plan → tasks → implementation)
- Backend-first architecture (data correctness before UI)
- Security by design (JWT-based authentication and strict user isolation)
- Deterministic, reproducible development using Claude Code
- Clarity for hackathon reviewers and full-stack engineers
- Production-aligned engineering practices

Spec structure (mandatory order):
- Spec-1: Backend Core & Data Layer (FastAPI + Database)
- Spec-2: Authentication & Security Integration (Better Auth + JWT)
- Spec-3: Frontend Application & Full-Stack Integration (Next.js)

Key standards:
- All features must originate from written specs
- No manual coding; all code generated via Claude Code
- Backend logic must be correct before auth or UI integration
- API contracts must be explicit and stable
- User data must always be isolated and protected
- Frontend must never bypass backend validation

Technology standards:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- API style: RESTful with proper HTTP status codes

Security standards:
- JWT required for all protected endpoints
- JWT verification performed in FastAPI
- Shared secret configured via BETTER_AUTH_SECRET
- Authenticated user identity derived only from JWT
- Task ownership enforced on every operation
- Unauthorized access returns 401 or 403 consistently

Data standards:
- Persistent storage required
- Clear ownership relationship between users and tasks
- No cross-user data leakage
- Schema changes must be spec-approved

Frontend standards:
- Responsive UI (desktop and mobile)
- Auth-gated routes
- JWT automatically attached to API requests
- Clear error and loading states
- End-to-end integration validated

Constraints:
- Must implement all basic Todo features
- Multi-user support is mandatory
- No advanced features beyond defined specs
- Hackathon-ready scope and delivery
- All decisions must be reviewable via specs and plans

Success criteria:
- Fully functional multi-user Todo web application
- Backend, auth, and frontend integrated correctly
- Users can only access their own tasks
- All APIs protected and validated
- Project passes hackathon evaluation for correctness, security, and clarity

## Response snapshot

Project constitution created at `.specify/memory/constitution.md` with version 1.0.0. Defined core principles (Spec-Driven, Backend-First, Security by Design), technology standards (Next.js, FastAPI, Neon, Better Auth), and governance rules.

## Outcome

- ✅ Impact: Established project governance and standards.
- 🧪 Tests: none
- 📁 Files: Created .specify/memory/constitution.md
- 🔁 Next prompts: /sp.clarify
- 🧠 Reflection: Successfully initialized the constitution from user input.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
