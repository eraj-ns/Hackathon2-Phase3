# Tasks: 002-auth-integration

**Branch**: `002-auth-integration` | **Date**: 2026-01-23 | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Summary
Total tasks: 18 | US1: 4 | US2: 6 | US3: 4 | Parallel: 8 [P] | MVP: Phase 3 (US1 complete + foundational)

**Dependencies**: Phase 1 → 2 → 3+ (stories independent post-foundational)

**Parallel Execution**:
- US1: T003 [P], T004 [P]
- US2: T009 [P], T010 [P], T012 [P]
- US3: T015 [P], T016 [P]

## Phase 1: Setup
- [x] T001 Add python-jose[cryptography] to backend/requirements.txt
- [x] T002 Set BETTER_AUTH_SECRET in backend/.env (generate if missing)

## Phase 2: Foundational (Auth Deps + Models)
**Independent Test**: curl invalid token → 401 on /api/tasks
- [x] T003 Create JWT verification in backend/src/dependencies.py (get_current_user, python-jose decode)
- [x] T004 [P] Ensure User model exists and queryable in backend/src/models/user.py
- [x] T005 Update backend/src/database.py for User table creation
- [x] T006 Confirm Task.user_id FK non-nullable in backend/src/models/task.py

## Phase 3: US1 Authenticate User
**Goal**: Backend verifies JWT, extracts user_id.
**Independent Test**: Valid mock JWT → user fetched; invalid → 401.
- [x] T007 [US1] Add get_current_user dep to test endpoint in backend/src/main.py
- [x] T008 [US1] Verify token decode raises 401 for expired/invalid in backend/src/dependencies.py

## Phase 4: US2 Access Protected User Data
**Goal**: CRUD filtered by user_id.
**Independent Test**: Valid JWT user A → own tasks only; POST sets user_id.
- [x] T009 [P] [US2] Protect GET /api/tasks with Depends(get_current_user) in backend/src/api/tasks_router.py
- [x] T010 [P] [US2] Filter tasks by current_user.id in GET list backend/src/api/tasks_router.py
- [x] T011 [US2] Protect POST /api/tasks; set task.user_id = current_user.id in backend/src/api/tasks_router.py
- [x] T012 [P] [US2] Protect PUT/PATCH /api/tasks/{id}; filter + ownership check backend/src/api/tasks_router.py
- [x] T013 [US2] Protect DELETE /api/tasks/{id}; ownership check backend/src/api/tasks_router.py
- [x] T014 [US2] Update schemas if needed (hide user_id input) in backend/src/api/tasks_router.py

## Phase 5: US3 Reject Unauthorized Access
**Goal**: 401/403 enforcement.
**Independent Test**: No/missing token → 401; wrong user → 403; tamper → 401.
- [x] T015 [P] [US3] Add 401 handling for missing Authorization header in backend/src/dependencies.py
- [x] T016 [P] [US3] Add 403 for ownership mismatch in task ops backend/src/api/tasks_router.py
- [x] T017 [US3] Test tampered JWT raises JWTError → 401 in backend/src/dependencies.py
- [x] T018 [US3] Ensure all protected routes use dep backend/src/main.py and backend/src/api/tasks_router.py

## Phase 6: Polish & Cross-Cutting
**Independent Test**: Full curl flow: auth → CRUD own data → reject others.
- [x] T019 Add OpenAPI security scheme to backend/src/main.py
- [x] T020 Update quickstart.md with multi-user curl examples
