# Tasks: Backend Core & Data Layer

**Input**: Design documents from `/specs/001-backend-core/`
**Prerequisites**: plan.md (✅), spec.md (✅ for user stories)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create directory structure `backend/src/{models,api,services}` and `backend/tests`
- [ ] T002 [P] Create `backend/requirements.txt` with FastAPI, SQLModel, psycopg2-binary, pytest
- [ ] T003 Verify `.env` file exists with DATABASE_URL and BETTER_AUTH_SECRET
- [ ] T004 Create `backend/src/__init__.py` and module init files

## Phase 2: Foundational (Database Layer)

**Purpose**: Set up database connection and schema

- [x] T005 [P] Create `backend/src/database.py` with Neon PostgreSQL connection using SQLModel
- [x] T006 Create `backend/src/models/task.py` with Task entity (id, title, description, completed, user_id, timestamps)
- [x] T007 Create database tables on application startup in `backend/src/main.py`

## Phase 3: User Story 1 - Task Lifecycle Management (P1)

**Purpose**: Implement full CRUD operations for tasks

### Tests (if requested) - would be in separate test files

### Implementation Tasks

#### Models & Services
- [x] T008 [P] [US1] Create `backend/src/services/task_service.py` with CRUD functions
  - `create_task(title, description, user_id=None)`
  - `get_task_by_id(task_id)`
  - `list_all_tasks()`
  - `update_task(task_id, **fields)`
  - `delete_task(task_id)`

#### API Router & All Endpoints (T009-T018)
- [x] T009 [US1] Create `backend/src/api/tasks_router.py` with router setup and all endpoints:
  - POST `/api/tasks` - Create task with validation (201 or 422)
  - GET `/api/tasks` - List all tasks (200)
  - GET `/api/tasks/{id}` - Get task by ID (200 or 404)
  - PUT `/api/tasks/{id}` - Update task (200 or 404)
  - DELETE `/api/tasks/{id}` - Delete task (204 or 404)
  - PATCH `/api/tasks/{id}/complete` - Toggle completion (200 or 404)
  - Path: `backend/src/api/tasks_router.py`

#### Router Registration
- [x] T015 [US1] Register tasks_router in `backend/src/main.py` with prefix `/api/tasks`
- [x] T016 [US1] Add exception handling in `backend/src/api/tasks_router.py` for 422/404 errors

## Phase 4: User Story 2 - Task Completion (P2)

**Purpose**: [COMPLETED - Combined with Phase 3] Task status completion toggle integrated into tasks_router.py

- [x] T017 [P] [US2] `toggle_task_completion(task_id)` function integrated into task_service.py via update_task
- [x] T018 [P] [US2] PATCH `/api/tasks/{id}/complete` endpoint implemented in tasks_router.py
  - Toggles `completed` field
  - Returns 200 with updated task or 404 if not found
  - Path: `backend/src/api/tasks_router.py`}

## Phase 5: Polish & Final Validation

**Purpose**: Cross-cutting concerns and final validation

- [ ] T019 [P] Create `backend/tests/test_tasks.py` with basic CRUD tests (if testing requested)
- [ ] T020 Run server and verify all endpoints with Postman/curl
- [ ] T021 Verify data persists after restart
- [ ] T022 Update `backend/README.md` with API documentation
- [ ] T023 Verify API returns correct status codes (200, 201, 204, 404, 422)
- [ ] T024 Create PHR for Phase 3-4 completion

**API Verification Checklist**:
- [ ] POST /api/tasks returns 201 with valid data
- [ ] POST /api/tasks returns 422 without title
- [ ] GET /api/tasks returns 200 with task list
- [ ] GET /api/tasks/{id} returns 200 for existing task
- [ ] GET /api/tasks/{id} returns 404 for non-existent task
- [ ] PUT /api/tasks/{id} returns 200 with updated task
- [ ] DELETE /api/tasks/{id} returns 204
- [ ] PATCH /api/tasks/{id}/complete toggles completed status
- [ ] All endpoints handle database errors gracefully (500)

## Phase 5: Polish & Final Validation

**Purpose**: Cross-cutting concerns and final validation

- [ ] T019 [P] Create `backend/tests/test_tasks.py` with basic CRUD tests (if testing requested)
- [ ] T020 Run server and verify all endpoints work via Postman/curl
- [ ] T021 Verify data persists after restart (confirm Neon connection)
- [ ] T022 Update `backend/src/quickstart.md` with running instructions
- [ ] T023 Verify API returns correct status codes for all scenarios (200, 201, 204, 404, 422)
- [ ] T024 Document assumptions: `user_id` field exists but is not enforced (mocked placeholder)

#### API Endpoints - POST /api/tasks
- [ ] T009 [US1] Create `backend/src/api/tasks_router.py` with router setup
- [ ] T010 [P] [US1] Implement POST `/api/tasks` endpoint with validation:
  - Accept JSON body {"title": string, "description": string?}
  - Return 422 if title missing
  - Return 201 with created task
  - Path: `backend/src/api/tasks_router.py`

#### API Endpoints - GET /api/tasks
- [ ] T011 [P] [US1] Implement GET `/api/tasks` endpoint:
  - Return list of all tasks (empty array if none)
  - Return 200 OK
  - Path: `backend/src/api/tasks_router.py`

#### API Endpoints - GET /api/tasks/{id}
- [ ] T012 [P] [US1] Implement GET `/api/tasks/{id}` endpoint:
  - Return task details if exists
  - Return 404 if task not found
  - Return 422 if ID format invalid
  - Path: `backend/src/api/tasks_router.py`

#### API Endpoints - PUT /api/tasks/{id}
- [ ] T013 [P] [US1] Implement PUT `/api/tasks/{id}` endpoint:
  - Accept full task update JSON
  - Return 404 if task not found
  - Return 200 with updated task
  - Path: `backend/src/api/tasks_router.py`

#### API Endpoints - DELETE /api/tasks/{id}
- [ ] T014 [P] [US1] Implement DELETE `/api/tasks/{id}` endpoint:
  - Return 204 No Content on success
  - Return 404 if not found
  - Path: `backend/src/api/tasks_router.py`

#### Router Registration
- [ ] T015 [US1] Register tasks_router in `backend/src/main.py` with prefix `/api/tasks`
- [ ] T016 [US1] Add global exception handler in `backend/src/main.py` for 422/404/500 errors

## Phase 4: User Story 2 - Task Completion (P2)

**Purpose**: Implement task status completion toggle

#### Models & Services
- [ ] T017 [P] [US2] Add `toggle_task_completion(task_id)` to `backend/src/services/task_service.py`

#### API Endpoint
- [ ] T018 [P] [US2] Implement PATCH `/api/tasks/{id}/complete` endpoint in `tasks_router.py`:
  - Toggle `completed` field from false to true or true to false
  - Return 200 with updated task
  - Return 404 if not found

## Phase 5: Polish & Final Validation

**Purpose**: Cross-cutting concerns and final validation

- [ ] T019 [P] Create `backend/tests/test_tasks.py` with basic CRUD tests (if testing requested)
- [ ] T020 Run server and verify all endpoints work via Postman/curl
- [ ] T021 Verify data persists after restart (confirm Neon connection)
- [ ] T022 Update `backend/src/quickstart.md` with running instructions
- [ ] T023 Verify API returns correct status codes for all scenarios (200, 201, 204, 404, 422)
- [ ] T024 Document assumptions: `user_id` field exists but is not enforced (mocked placeholder)

## Implementation Order & Dependencies

**Parallel Execution** (Phase 1-2):
- T001-T003: Environment setup (can start immediately)
- T004-T007: Database layer (independent of API)

**Story Parallelism** (Phase 3-4):
- US1 (T008-T016): All CRUD operations are co-dependent - implement sequentially
- US2 (T017-T018): Can be developed after US1 but is independent enough to be P2

**MVP Scope**: Complete Phase 1-3 to deliver core task management (US1) as first working increment.

**After MVP**: Proceed to Phase 4-5 to add completion toggle and polish.

## Testing Strategy (per spec)

Each story is independently testable:

- **US1 Test**: Use curl/Postman to create, read, update, delete tasks - all operations succeed
- **US2 Test**: Create task → toggle complete → verify status → toggle back → verify

Tests are Optional per feature spec: tests NOT requested
