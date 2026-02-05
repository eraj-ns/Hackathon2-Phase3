---
description: "Task list for Frontend Application & Full-Stack Integration (Spec-3)"
---

# Tasks: Frontend Application & Full-Stack Integration (Spec-3)

**Input**: Design documents from `/specs/003-frontend-integration/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/api-integration.md

**Organization**: Tasks grouped by user story (P1 → P2 → P3) to enable independent implementation and delivery. Each story is independently testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story identifier (US1, US2, US3)
- **File paths**: Exact frontend project structure per plan.md

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Next.js project initialization and structural setup

- [ ] T001 Initialize Next.js 16+ project with App Router in `/frontend` directory
- [ ] T002 Install dependencies: better-auth, @better-auth/react, axios, typescript, react 18
- [ ] T003 [P] Configure TypeScript (`tsconfig.json`) for strict mode and path aliases
- [ ] T004 [P] Set up environment configuration (`.env.local` template with `NEXT_PUBLIC_API_URL`)
- [ ] T005 Create project directory structure per plan: `frontend/src/app`, `components`, `services`, `hooks`, `types`
- [ ] T006 [P] Configure Next.js config (`next.config.js`) for App Router and build optimization
- [ ] T007 [P] Set up basic styling infrastructure in `frontend/src/styles/globals.css` with responsive breakpoints

**Checkpoint**: Project structure ready for feature development

---

## Phase 2: Foundational (Core Infrastructure)

**Purpose**: Shared infrastructure that MUST be complete before any user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create root layout component in `frontend/src/app/layout.tsx` with common UI structure
- [ ] T009 [P] Create TypeScript types/interfaces file at `frontend/src/types/index.ts` (Task, User, AuthState, Session, APIError)
- [ ] T010 Create API client with Axios in `frontend/src/services/api.ts` with JWT interceptor (attach token to all requests)
- [ ] T011 [P] Create error handling interceptor in api.ts (catch 401, redirect to signin; format error responses)
- [ ] T012 [P] Implement Better Auth client setup in `frontend/src/services/auth.ts` with JWT plugin configuration
- [ ] T013 Create utility function for token storage/retrieval in `frontend/src/services/api.ts` (localStorage integration)
- [ ] T014 [P] Create `ErrorBanner.tsx` component in `frontend/src/components/` for centralized error display
- [ ] T015 [P] Create `LoadingSpinner.tsx` component in `frontend/src/components/` for loading states
- [ ] T016 Create `useAuth.ts` custom hook in `frontend/src/hooks/` to manage auth state and session validation
- [ ] T017 [P] Set up app root page at `frontend/src/app/page.tsx` that redirects authenticated users to dashboard, unauthenticated to signin

**Checkpoint**: Foundation complete - user story implementation can begin

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can create accounts and sign in securely, accessing the application with JWT authentication

**Independent Test**: Create new account → Sign in → Redirected to dashboard with valid session → Logout → Redirected to signin

### Implementation for User Story 1

- [ ] T018 [P] [US1] Create auth layout group at `frontend/src/app/(auth)/layout.tsx` (non-protected, plain styling)
- [ ] T019 [P] [US1] Create signup page at `frontend/src/app/(auth)/signup/page.tsx` with form (email, password, confirm password fields)
- [ ] T020 [P] [US1] Create signin page at `frontend/src/app/(auth)/signin/page.tsx` with form (email, password fields)
- [ ] T021 [US1] Implement Better Auth integration in signup page: call signup endpoint, store JWT, redirect to `/dashboard` on success
- [ ] T022 [US1] Implement Better Auth integration in signin page: call signin endpoint, store JWT, redirect to `/dashboard` on success
- [ ] T023 [P] [US1] Create `Navbar.tsx` component in `frontend/src/components/` with user email display and logout button
- [ ] T024 [US1] Implement form validation in signup page: email format, password strength, password match (show field-level errors)
- [ ] T025 [US1] Implement error handling in signup/signin pages: display validation errors, duplicate email (409), invalid credentials (401)
- [ ] T026 [P] [US1] Add loading states to signup/signin buttons (disable during submission)
- [ ] T027 [US1] Create protected layout at `frontend/src/app/(protected)/layout.tsx` that checks auth state via `useAuth()` hook and redirects unauthenticated users to `/signin`
- [ ] T028 [P] [US1] Test signup flow: Create account → Verify token stored → Session persists on page refresh
- [ ] T029 [P] [US1] Test signin flow: Sign in with valid credentials → Redirected to dashboard → Token in Authorization header for API calls
- [ ] T030 [US1] Test protected route: Access dashboard without login → Redirected to signin page

**Checkpoint**: User Story 1 complete - Users can sign up, sign in, and access protected routes with JWT authentication

---

## Phase 4: User Story 2 - Task Management Dashboard (Priority: P2)

**Goal**: Authenticated users can view, create, update, and delete tasks with real-time UI updates

**Independent Test**: Sign in → View task list → Create task → Task appears in list → Toggle completion → Delete task → Task removed

### Implementation for User Story 2

- [ ] T031 [P] [US2] Create dashboard page at `frontend/src/app/(protected)/dashboard/page.tsx` (main container for task UI)
- [ ] T032 [P] [US2] Create `TaskList.tsx` component in `frontend/src/components/` to display list of tasks with proper formatting
- [ ] T033 [P] [US2] Create `TaskItem.tsx` component in `frontend/src/components/` for individual task row (description, checkbox, delete button, hover states)
- [ ] T034 [P] [US2] Create `TaskForm.tsx` component in `frontend/src/components/` for task creation (input field, submit button, clear on success)
- [ ] T035 [US2] Implement `useTasks.ts` custom hook in `frontend/src/hooks/` with fetchTasks, createTask, updateTask, deleteTask functions
- [ ] T036 [US2] Create task API client methods in `frontend/src/services/taskClient.ts` (GET /api/tasks, POST, PATCH, DELETE endpoints with proper error handling)
- [ ] T037 [US2] Implement dashboard page: fetch tasks on mount via useTasks hook, display TaskList and TaskForm, show loading spinner while fetching
- [ ] T038 [P] [US2] Implement TaskForm: call createTask on submit, refetch tasks on success, show validation errors if title empty
- [ ] T039 [P] [US2] Implement TaskItem: checkbox toggles task completion via updateTask, delete button removes task, show loading state during mutations
- [ ] T040 [US2] Implement error handling in dashboard: show ErrorBanner for API failures, display "No tasks yet" empty state
- [ ] T041 [P] [US2] Add loading indicators: spinner in TaskList while fetching, disable buttons during mutation, prevent duplicate submissions
- [ ] T042 [US2] Implement responsive layout: TaskForm full-width on mobile, TaskList stacked on mobile, side-by-side on desktop via CSS media queries
- [ ] T043 [P] [US2] Test create task: Submit form → Task appears in list → New task has correct data (user_id, timestamp, completed=false)
- [ ] T044 [P] [US2] Test update task: Toggle completion → UI updates → Backend receives PATCH request with JWT
- [ ] T045 [P] [US2] Test delete task: Delete task → Task removed from list → Backend receives DELETE request with JWT
- [ ] T046 [P] [US2] Test data isolation: Create tasks as User A → Sign in as User B → User B's task list is empty (no cross-user data)
- [ ] T047 [US2] Test empty state: Dashboard with no tasks shows "No tasks yet" message

**Checkpoint**: User Story 2 complete - Users can create, view, update, delete tasks with responsive UI

---

## Phase 5: User Story 3 - API Integration & Error Handling (Priority: P3)

**Goal**: Application handles errors gracefully with clear user feedback; robust API integration across all CRUD operations

**Independent Test**: Simulate network errors → See error messages → Simulate validation errors → See field-level errors → Session expires → Redirected to signin

### Implementation for User Story 3

- [ ] T048 [P] [US3] Implement validation error display in TaskForm: map error.details to field errors, show red borders and error messages
- [ ] T049 [P] [US3] Implement validation error display in signup/signin: map error.details to email/password fields, show inline error messages
- [ ] T050 [US3] Implement 401 handler: When API returns 401, clear token, redirect to signin, show "Session expired" message via ErrorBanner
- [ ] T051 [P] [US3] Implement 400/422 handler: Show validation errors via ErrorBanner with retry option
- [ ] T052 [P] [US3] Implement 500 handler: Show "Server error" message via ErrorBanner with retry button
- [ ] T053 [P] [US3] Implement network error handler: Show "Connection lost" message when fetch fails, provide retry option
- [ ] T054 [US3] Add loading state timeout: If API takes >5s, show warning message "Server taking longer than expected..."
- [ ] T055 [P] [US3] Prevent duplicate submissions: Disable TaskForm submit button while request in flight, disable TaskItem buttons during mutations
- [ ] T056 [P] [US3] Add retry mechanism: ErrorBanner shows "Retry" button, clicking retries the failed operation
- [ ] T057 [US3] Implement form field validation messages: TaskForm shows error if title length invalid (1-500 chars), signup/signin show password requirements
- [ ] T058 [P] [US3] Add accessibility: Error messages semantic HTML (aria-live for dynamic errors), keyboard navigation for form fields
- [ ] T059 [P] [US3] Test network failure: Disable network → Create task → Shows error message → Enable network → Retry works
- [ ] T060 [P] [US3] Test validation errors: Submit empty task → Shows "Title required" → Fill and retry → Success
- [ ] T061 [P] [US3] Test session expiration: Sign in → Wait for token expiration → Create task → 401 error → Redirected to signin
- [ ] T062 [P] [US3] Test slow API: Make API slow → Dashboard shows loading indicator → >5s shows warning → Response arrives → UI updates
- [ ] T063 [US3] Test invalid credentials: Sign in with wrong password → Shows "Invalid credentials" error → Can retry

**Checkpoint**: User Story 3 complete - Error handling and API integration robust with clear user feedback

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Responsive design validation, documentation, and quality improvements

- [ ] T064 [P] Test responsive design: Dashboard works on 320px (mobile), 768px (tablet), 1024px+ (desktop) viewports
- [ ] T065 [P] Test responsive design: Forms stack vertically on mobile, side-by-side on desktop
- [ ] T066 [P] Test responsive design: Navbar/navigation accessible on mobile (readable, tappable buttons)
- [ ] T067 [P] Verify all components have proper TypeScript types: No `any` types, strict null checks enabled
- [ ] T068 [P] Code cleanup: Remove unused imports, consistent formatting per prettier config
- [ ] T069 [P] Update README at `frontend/README.md` with setup instructions, environment variables, running the app
- [ ] T070 Validate quickstart.md scenarios: Run through all acceptance test cases from spec.md
- [ ] T071 [P] Performance check: Dashboard page load <2s, API responses <500ms p95, no memory leaks in components
- [ ] T072 [P] Security audit: Verify no hardcoded secrets, all sensitive data in .env.local, JWT attached to all protected API calls
- [ ] T073 [P] End-to-end validation: Full signup → signin → create/update/delete tasks → logout → signin flow works seamlessly
- [ ] T074 Final integration test: Run frontend against running FastAPI backend, verify all CRUD operations work with JWT authentication

**Checkpoint**: All user stories complete, responsive, tested, and ready for hackathon evaluation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user story work
- **Phase 3 (US1 - P1)**: Depends on Phase 2 - MVP scope (users can sign in)
- **Phase 4 (US2 - P2)**: Depends on Phase 2 (can run after Phase 3, but independent of US1 completion)
- **Phase 5 (US3 - P3)**: Depends on Phase 2 (can run after other stories, but independent)
- **Phase 6 (Polish)**: Depends on all desired stories being complete

### Within Each User Story

Tasks marked [P] can run in parallel (different files, no dependencies).
Tasks without [P] depend on previous task completion (model before service, service before component).

---

## Parallel Execution Examples

### Setup Phase (Phase 1)
```bash
# Can run in parallel:
T003 Configure TypeScript
T004 Set up environment
T006 Configure Next.js
T007 Set up styling
# While sequential:
T001 Initialize Next.js → T002 Install deps → (then above in parallel)
```

### Foundational Phase (Phase 2)
```bash
# Can run in parallel:
T009 Create types
T011 Create error interceptor
T012 Create auth client
T014 Create ErrorBanner component
T015 Create LoadingSpinner component
# Sequential foundation:
T010 Create API client (depends on T013 for token storage)
T016 Create useAuth hook (depends on T012)
T017 Create root page (depends on T016)
```

### User Story 1 (Phase 3)
```bash
# Can run in parallel:
T018 Create auth layout
T019 Create signup page
T020 Create signin page
T023 Create Navbar component
T026 Add loading states
T028-T030 Write tests
# Sequential:
T021 Implement signup (depends on T019, T012)
T022 Implement signin (depends on T020, T012)
T024 Add form validation (depends on T019, T020)
T027 Create protected layout (depends on T016)
```

### User Story 2 (Phase 4) - Can start after Phase 2, runs parallel to US1
```bash
# Can run in parallel:
T032 Create TaskList component
T033 Create TaskItem component
T034 Create TaskForm component
T043-T046 Write tests
# Sequential:
T031 Create dashboard page (depends on T027 layout)
T035 Create useTasks hook (depends on T036)
T036 Create taskClient (depends on T010 api client)
T037 Implement dashboard (depends on T031, T035)
```

### User Story 3 (Phase 5) - Can start after Phase 2, runs parallel to US1 and US2
```bash
# Can run in parallel:
T048-T062 All error handling tasks (independent components/services)
T059-T063 Test tasks
# Sequential:
T050 Implement 401 handler (depends on T011 interceptor)
T057 Implement validation display (depends on T024, T049)
```

---

## Task Checklist Format

All tasks follow strict format for automation:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

Examples:
- ✅ `- [ ] T001 Initialize Next.js 16+ project with App Router in /frontend directory`
- ✅ `- [ ] T010 [P] Create error handling interceptor in frontend/src/services/api.ts`
- ✅ `- [ ] T021 [US1] Implement Better Auth integration in signup page`
- ✅ `- [ ] T043 [P] [US2] Test create task: Submit form → Task appears in list`

---

## Implementation Strategy

### MVP (Minimum Viable Product)
Complete **Phase 1 + Phase 2 + Phase 3 (User Story 1)** for MVP:
- Project initialized with Next.js and dependencies
- Signup/signin pages with Better Auth integration
- Protected routes with auth checking
- JWT token storage and API authentication
- Users can create accounts and log in

**Timeline**: Suitable for hackathon MVP demo

### Full Feature
Complete all phases for full feature:
- Users can sign up, sign in (US1)
- Users can create, view, update, delete tasks (US2)
- Robust error handling and API integration (US3)
- Responsive design and polish

**Timeline**: Suitable for hackathon final submission

---

## Independent Test Criteria

### User Story 1 Independent Test
- [ ] Create new account with valid email/password
- [ ] Redirected to dashboard
- [ ] Refresh page → Session persists (token in localStorage)
- [ ] Sign in with different email → Still logged in
- [ ] Access protected route as authenticated user → Allowed
- [ ] Clear token manually → Protected route redirects to signin

### User Story 2 Independent Test
- [ ] Sign in successfully (User A)
- [ ] Dashboard shows empty state (no tasks yet)
- [ ] Create task → Task appears in list
- [ ] Create second task → Both tasks visible
- [ ] Toggle completion on first task → Checkbox updates
- [ ] Delete second task → Removed from list
- [ ] Refresh page → Tasks persist (fetched from backend)
- [ ] Sign out and sign in as User B → User B's task list is empty
- [ ] Return to User A → User A sees original tasks

### User Story 3 Independent Test
- [ ] Submit empty task form → Shows "Title required" error
- [ ] Submit task with >500 chars → Shows validation error
- [ ] Network offline → Create task → Shows "Connection lost" → Retry works
- [ ] Server returns 500 → Shows error banner with retry option
- [ ] Session expires (token invalid) → Any API call → Redirected to signin with "Session expired"
- [ ] Slow API (>5s) → Shows loading state + warning message after 5s
- [ ] Duplicate submission: Click submit twice quickly → Only one request sent, prevent duplicate

---

## Acceptance Criteria Summary

**All tasks must satisfy**:
- Exact file paths provided (no ambiguity)
- Clear description of what to implement
- Testable acceptance criteria
- Follows Next.js 16+ App Router conventions
- TypeScript strict mode compliance
- No hardcoded secrets (use .env.local)
- JWT attached to all protected API calls
- Responsive design (mobile + desktop)
- Error handling with user-friendly messages
- Loading states prevent duplicate submissions

---

## Quick Reference: Task Organization

**By Phase**:
- Phase 1: T001-T007 (Setup)
- Phase 2: T008-T017 (Foundation)
- Phase 3: T018-T030 (US1 - Auth)
- Phase 4: T031-T047 (US2 - Tasks)
- Phase 5: T048-T063 (US3 - Error Handling)
- Phase 6: T064-T074 (Polish)

**By User Story**:
- US1 (Auth): T018-T030
- US2 (Tasks): T031-T047
- US3 (Errors): T048-T063

**Parallelizable Tasks** (marked [P]):
- T003, T004, T006, T007 (Setup)
- T009, T011, T012, T014, T015 (Foundation)
- T018, T019, T020, T023, T026, T028-T030 (US1)
- T032-T034, T038-T039, T043-T047 (US2)
- T048-T049, T051-T053, T055-T063 (US3)
- T064-T072 (Polish)

---

## Next Steps

1. **Review & Approve**: Confirm task organization and MVP scope
2. **Begin Implementation**: Run `sp.implement` to execute Phase 1 → Phase 2 → Phase 3
3. **Iterate**: Complete each phase checkpoint before advancing
4. **Validate**: Run quickstart.md acceptance test scenarios
5. **Deliver**: Push to branch and create PR for hackathon submission
