# Implementation Plan: Frontend Application & Full-Stack Integration (Spec-3)

**Branch**: `003-frontend-integration` | **Date**: 2026-01-24 | **Spec**: `/specs/003-frontend-integration/spec.md`
**Input**: Feature specification from `/specs/003-frontend-integration/spec.md`

**Note**: This plan defines the architecture and design for the Next.js frontend application integrated with the FastAPI backend. Execution phases follow: Phase 0 (Research) → Phase 1 (Design & Contracts) → Phase 2 (Tasks).

## Summary

Build a Next.js 16+ App Router frontend that provides user authentication (signup/signin via Better Auth with JWT tokens) and a task management dashboard. The frontend will integrate with the FastAPI backend via RESTful APIs, automatically attaching JWT tokens to all requests, displaying user-specific data with strict isolation, and providing responsive UI across desktop and mobile devices. Core features: user authentication, task CRUD operations, loading/error states, and responsive layouts.

## Technical Context

**Language/Version**: TypeScript 4.8+ with React 18 (Next.js 16+)
**Primary Dependencies**: Next.js 16+ (App Router), Better Auth (JWT plugin), @better-auth/react, Axios or Fetch API
**Storage**: JWT tokens stored in browser (localStorage or cookie), user data managed on backend (Neon PostgreSQL via FastAPI)
**Testing**: Next.js testing utilities, manual E2E validation against running backend
**Target Platform**: Web browser (desktop 1024px+, mobile 320px+)
**Project Type**: Web application (frontend SPA consuming REST API)
**Performance Goals**: Page load <2s, API response <500ms p95, responsive UI
**Constraints**: Must integrate with existing FastAPI backend (Spec-1, Spec-2), JWT token must be attached to all protected endpoints, no hardcoded secrets, mobile-responsive
**Scale/Scope**: Single-user per session, ~5-10 UI screens/pages, CRUD operations on tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**1.1 Spec-Driven Development**: ✅ PASS – Spec-3 follows Spec-1 (Backend) and Spec-2 (Auth), this plan is specification-driven.

**1.2 Backend-First Architecture**: ✅ PASS – Frontend consumes existing FastAPI backend; all business logic in backend; frontend is API consumer only.

**1.3 Security by Design**: ✅ PASS – JWT tokens mandatory (from Spec-2); protected routes implemented; no auth logic in frontend, delegated to backend.

**1.4 Deterministic, Reproducible Development**: ✅ PASS – All code will be generated via Claude Code with explicit specifications; no manual hacks.

**1.5 Clarity for Reviewers**: ✅ PASS – Architecture documented; contracts defined; traceability from spec to code via references.

**1.6 Production-Aligned Engineering**: ✅ PASS – Error handling, loading states, responsive design included; no shortcuts beyond hackathon scope.

**2.1 Technology Standards**: ✅ PASS – Uses Next.js 16+ App Router, Better Auth (JWT), RESTful API.

**2.2 Security Standards**: ✅ PASS – JWT from Spec-2 (BETTER_AUTH_SECRET); Authorization header on all API calls; backend validates on every endpoint.

**2.3 Data Standards**: ✅ PASS – Frontend never stores user tasks locally; all data from backend (Neon PostgreSQL via FastAPI); display is read-only on frontend.

**2.4 Frontend Standards**: ✅ PASS – Responsive (desktop/mobile), auth-gated routes, clear error messages, loading states.

**2.5 Documentation Standards**: ✅ PASS – Follows Spec-1 → Spec-2 → Spec-3 order; Spec-3 depends on Specs 1 & 2.

**Overall Gate**: ✅ PASS – All constraints satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/                    # Next.js 16+ App Router
│   │   ├── (auth)/              # Auth layout group
│   │   │   ├── signin/
│   │   │   │   └── page.tsx     # Sign-in page
│   │   │   ├── signup/
│   │   │   │   └── page.tsx     # Sign-up page
│   │   │   └── layout.tsx        # Auth layout wrapper
│   │   ├── (protected)/          # Protected layout group (requires auth)
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx      # Task dashboard
│   │   │   └── layout.tsx        # Protected layout (redirects if no auth)
│   │   ├── layout.tsx             # Root layout
│   │   └── page.tsx               # Home/redirect page
│   ├── components/
│   │   ├── TaskForm.tsx           # Task creation/edit form
│   │   ├── TaskList.tsx           # Task list display
│   │   ├── TaskItem.tsx           # Individual task row
│   │   ├── LoadingSpinner.tsx     # Loading indicator
│   │   ├── ErrorBanner.tsx        # Error message display
│   │   └── Navbar.tsx             # Top navigation/logout
│   ├── services/
│   │   ├── api.ts                 # Axios client with JWT middleware
│   │   ├── auth.ts                # Better Auth client setup
│   │   └── taskClient.ts          # Task-specific API calls
│   ├── hooks/
│   │   ├── useAuth.ts             # Auth state hook
│   │   └── useTasks.ts            # Task data & mutations hook
│   ├── styles/
│   │   └── globals.css            # Global styling (responsive)
│   └── types/
│       └── index.ts               # TypeScript types for API responses
├── public/                       # Static assets
├── tests/                        # Test files (unit/integration)
├── package.json
├── tsconfig.json
└── next.config.js
```

**Structure Decision**: Web application pattern with Next.js App Router. Organized by domain (auth, protected) with shared components and services. Follows conventional Next.js patterns for scalability and clarity.

## Complexity Tracking

> No constitution violations. Structure is minimal and necessary.

---

## Phase 0: Research & Decisions

### Key Research Questions Resolved

1. **JWT Token Storage**
   - Decision: Store JWT in localStorage initially; consider secure HTTP-only cookie strategy in production.
   - Rationale: localStorage allows easy access for API headers; hackathon scope prioritizes rapid development.
   - Alternatives: sessionStorage (lost on browser close), HTTP-only cookie (more secure, requires backend coordination).

2. **Route Protection Strategy**
   - Decision: Route-level protection via layout component that checks auth state; redirect to signin if unauthenticated.
   - Rationale: Cleaner architecture; uses Next.js App Router layout groups for clean separation.
   - Alternatives: Component-level checks (more granular but verbose); API-level only (poor UX, shows errors instead of redirect).

3. **Data Fetching Approach**
   - Decision: Client-side fetching (useEffect + useState) with loading and error states.
   - Rationale: Simplifies implementation; server-side data fetching with Protected Layout requires additional session handling.
   - Constraints: Must attach JWT to every request; backend must validate.

4. **Error Handling & Feedback**
   - Decision: Centralized error banner component + field-level validation messages.
   - Rationale: Consistent UX; clear feedback for network, validation, and auth errors.
   - Error taxonomy:
     - 401 Unauthorized: Session expired → Redirect to signin
     - 403 Forbidden: User lacks permission → Show error banner
     - 400/422 Validation: Invalid input → Show field-level errors
     - 5xx Server: Unexpected → Show generic error with retry

5. **Responsive Design Approach**
   - Decision: Mobile-first CSS with breakpoints (320px, 768px, 1024px).
   - Rationale: Hackathon requires mobile support; modern approach ensures accessibility.
   - Tools: CSS Grid/Flexbox for responsive layouts; @media queries for breakpoints.

### Backend API Integration Points

The following APIs from Spec-1 (Backend) are consumed:

- `GET /test-auth` (for JWT verification)
- `GET /api/tasks` (fetch user's tasks)
- `POST /api/tasks` (create task)
- `PATCH /api/tasks/{id}` (update task)
- `DELETE /api/tasks/{id}` (delete task)

All endpoints require `Authorization: Bearer <JWT_TOKEN>` header.

### Better Auth Setup

Better Auth from Spec-2 provides:
- User signup/signin via email + password
- JWT token generation (with shared secret `BETTER_AUTH_SECRET`)
- Session management

Frontend integrates via `@better-auth/react` plugin for automatic token handling.

---

## Phase 1: Design & Contracts

### 1.1 Data Model

**Frontend State Types** (types/index.ts):

```typescript
interface Task {
  id: string;
  user_id: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
}

interface TaskListState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}
```

### 1.2 API Contracts

#### Task Endpoints

**GET /api/tasks**
- Header: `Authorization: Bearer {JWT_TOKEN}`
- Response 200: `{ tasks: Task[] }`
- Response 401: Session expired
- Response 500: Server error

**POST /api/tasks**
- Header: `Authorization: Bearer {JWT_TOKEN}`
- Body: `{ description: string }`
- Response 201: `{ id: string, ... }`
- Response 400: Invalid input (missing description)
- Response 401: Session expired
- Response 422: Validation error (description length limits)

**PATCH /api/tasks/{id}**
- Header: `Authorization: Bearer {JWT_TOKEN}`
- Body: `{ description?: string, completed?: boolean }`
- Response 200: `{ id: string, ... }`
- Response 404: Task not found (or belongs to different user)
- Response 401: Session expired

**DELETE /api/tasks/{id}**
- Header: `Authorization: Bearer {JWT_TOKEN}`
- Response 204: No content
- Response 404: Task not found
- Response 401: Session expired

#### Authentication Flow

1. User submits signup form → Better Auth creates account, returns JWT
2. Frontend stores JWT in localStorage
3. On every API call, Axios interceptor adds `Authorization: Bearer {JWT}` header
4. Backend validates JWT; if expired/invalid, returns 401
5. Frontend catches 401 → Redirects to signin

### 1.3 Page & Component Breakdown

#### Pages

**/(auth)/signin/page.tsx** - Sign-in Page
- Form: email, password fields
- Submit button
- Link to signup
- Error display for failed login
- Redirect to dashboard on success

**/(auth)/signup/page.tsx** - Sign-up Page
- Form: email, password, confirm password
- Submit button
- Link to signin
- Validation: password match, email format
- Redirect to dashboard on success

**(protected)/dashboard/page.tsx** - Task Dashboard
- Task list (TaskList component)
- Task form (TaskForm component)
- Navbar with logout
- Loading spinner during fetch
- Error banner for API failures

#### Components

**TaskForm.tsx** - Task Creation Form
- Input field for description
- Submit button
- Loading state (disable on submit)
- Error display for validation failures
- Clear input on successful submission

**TaskList.tsx** - Task List Container
- Fetches tasks on mount (useEffect)
- Loading spinner
- Empty state message
- Renders TaskItem for each task

**TaskItem.tsx** - Individual Task Row
- Task description display
- Checkbox for completion toggle
- Delete button
- Edit mode (inline edit or modal)
- Hover states for actions

**LoadingSpinner.tsx** - Loading Indicator
- Centered spinner
- Optional message (e.g., "Loading tasks...")

**ErrorBanner.tsx** - Error Display
- Red/warning styling
- Clear message based on error type
- Dismiss button
- Session expired special handling

**Navbar.tsx** - Top Navigation
- User email display
- Logout button
- Redirect to signin on logout

#### Services (API Integration)

**api.ts** - Axios Client with JWT
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Interceptor: attach JWT to every request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor: handle 401 (redirect to signin)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to signin
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

**auth.ts** - Better Auth Setup
```typescript
import { createAuthClient } from '@better-auth/react';

export const client = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});
```

**taskClient.ts** - Task-specific API Calls
```typescript
import apiClient from './api';

export const taskClient = {
  fetchTasks: () => apiClient.get('/api/tasks'),
  createTask: (description: string) => apiClient.post('/api/tasks', { description }),
  updateTask: (id: string, data: { completed?: boolean; description?: string }) =>
    apiClient.patch(`/api/tasks/${id}`, data),
  deleteTask: (id: string) => apiClient.delete(`/api/tasks/${id}`),
};
```

#### Hooks

**useAuth.ts** - Auth State Management
```typescript
import { useEffect, useState } from 'react';
import { client } from '@/services/auth';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getSession = async () => {
      const session = await client.getSession();
      setUser(session?.user || null);
      setLoading(false);
    };
    getSession();
  }, []);

  return { user, loading };
};
```

**useTasks.ts** - Task Data & Mutations
```typescript
import { useEffect, useState } from 'react';
import { taskClient } from '@/services/taskClient';

export const useTasks = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const { data } = await taskClient.fetchTasks();
      setTasks(data.tasks);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks,
    loading,
    error,
    refetch: fetchTasks,
    createTask: async (description: string) => {
      try {
        await taskClient.createTask(description);
        await fetchTasks();
      } catch (err) {
        setError(err.message);
      }
    },
    updateTask: async (id: string, data: any) => {
      try {
        await taskClient.updateTask(id, data);
        await fetchTasks();
      } catch (err) {
        setError(err.message);
      }
    },
    deleteTask: async (id: string) => {
      try {
        await taskClient.deleteTask(id);
        await fetchTasks();
      } catch (err) {
        setError(err.message);
      }
    },
  };
};
```

### 1.4 Protected Routes Implementation

**Layout: (protected)/layout.tsx**
```typescript
'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';

export default function ProtectedLayout({ children }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/signin');
    }
  }, [user, loading, router]);

  if (loading) return <div>Loading...</div>;
  if (!user) return null; // Will redirect

  return children;
}
```

### 1.5 Responsive Design Strategy

**Mobile-First Breakpoints** (globals.css):
- 320px–767px: Mobile (single column, stacked layout)
- 768px–1023px: Tablet (2-column for tasks if needed)
- 1024px+: Desktop (full layout)

**Key Components**:
- Task form: Full-width input on mobile, side-by-side on desktop
- Task list: Card view on mobile, table view on desktop
- Navbar: Hamburger menu on mobile (scope: simplified navbar)

---

## Phase 2: Tasks (Execution) — To be Generated by `/sp.tasks`

After Phase 1 design is approved, the `/sp.tasks` command will generate:

1. **Foundation Tasks**: Initialize Next.js project, install dependencies, set up environment
2. **Auth UI Tasks**: Build signin/signup pages with Better Auth integration
3. **Task UI Tasks**: Build dashboard, task form, task list components
4. **API Integration Tasks**: Implement API client with JWT, test endpoints
5. **Routing Tasks**: Implement protected routes and redirects
6. **Responsive Design Tasks**: Add CSS, test on mobile/desktop
7. **Testing Tasks**: Manual E2E validation against backend

---

## Architecture Decisions (Identified for ADR Documentation)

The following decisions have architecturally significant implications and should be documented in ADRs:

1. **JWT Storage in localStorage** — Tradeoff: Simplicity vs. Security; suitable for hackathon, should be documented
2. **Client-Side Data Fetching** — Tradeoff: Simplicity vs. Server-Side Rendering; impacts caching and performance
3. **Route-Level Protection via Layout** — Tradeoff: Clean architecture vs. Per-Component Control

These will be formalized after user confirmation.

---

## Acceptance Criteria & Validation

### Functional Acceptance

- [ ] Users can sign up with email/password and are redirected to dashboard
- [ ] Users can sign in and see their task list
- [ ] Unauthenticated users are redirected to signin on protected page access
- [ ] Authenticated users can create, read, update, and delete tasks
- [ ] Task data is correctly isolated per user (cross-user data not visible)
- [ ] API errors display clear user-friendly messages
- [ ] Loading indicators show during API operations
- [ ] Sessions persist across browser refresh (JWT from localStorage)
- [ ] Session expiration (401) redirects to signin

### Technical Acceptance

- [ ] All API requests include JWT Authorization header
- [ ] Backend validates JWT on every protected endpoint
- [ ] Responsive layout works on 320px and 1024px viewports
- [ ] TypeScript compilation succeeds (no type errors)
- [ ] Environment variables (API_URL, BETTER_AUTH_SECRET) are not hardcoded
- [ ] Code follows Next.js and React best practices
- [ ] Error handling covers network failures, validation, and auth errors

### Quality Acceptance

- [ ] Code is reviewable by hackathon judges (clear structure, comments where logic is non-obvious)
- [ ] Architecture aligns with project constitution and Spec-Driven Development
- [ ] Full-stack integration works end-to-end (frontend + backend)

---

## Next Steps

1. **User Review**: Confirm Phase 1 design (page structure, API contracts, component breakdown)
2. **Phase 2 Execution**: Run `/sp.tasks` to generate execution tasks
3. **Implementation**: Follow task list in dependency order
4. **Validation**: Manual E2E testing against running backend and frontend
