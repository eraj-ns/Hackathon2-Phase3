# Frontend Quickstart Guide

**Feature**: Frontend Application & Full-Stack Integration
**Date**: 2026-01-24
**Purpose**: Quick reference for frontend architecture, key components, and getting started

---

## Architecture at a Glance

```
┌─────────────────────────────────────────┐
│     Browser (Next.js App Router)        │
├─────────────────────────────────────────┤
│  Pages (Auth, Dashboard)                │
│  ├─ /auth/signin                        │
│  ├─ /auth/signup                        │
│  └─ /dashboard                          │
│                                          │
│  Middleware                             │
│  └─ Auth guard (redirect unauth users)  │
│                                          │
│  Components (Reusable)                  │
│  ├─ TaskList                            │
│  ├─ TaskForm                            │
│  ├─ TaskItem                            │
│  └─ Error/Loading states                │
│                                          │
│  Libraries                              │
│  ├─ API client (with JWT attach)        │
│  ├─ Auth hooks (Better Auth)            │
│  └─ Utils (types, helpers)              │
└─────────────────────────────────────────┘
         ↓ (All requests with JWT)
┌─────────────────────────────────────────┐
│  Backend APIs (Spec-1 & Spec-2)         │
├─────────────────────────────────────────┤
│  Auth API (Spec-2)                      │
│  ├─ POST /api/auth/signup               │
│  ├─ POST /api/auth/signin               │
│  ├─ GET /api/auth/me                    │
│  └─ POST /api/auth/logout               │
│                                          │
│  Task API (Spec-1)                      │
│  ├─ GET /api/tasks                      │
│  ├─ POST /api/tasks                     │
│  ├─ PATCH /api/tasks/{id}               │
│  └─ DELETE /api/tasks/{id}              │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  Database (Neon PostgreSQL)             │
│  ├─ users table (Spec-2)                │
│  └─ tasks table (Spec-1)                │
└─────────────────────────────────────────┘
```

---

## Key Files & Responsibilities

### Pages (Next.js App Router)

| File | Purpose | Key Logic |
|------|---------|-----------|
| `app/page.tsx` | Home/redirect | Redirect authenticated users to `/dashboard`, others to `/auth/signin` |
| `app/auth/signin/page.tsx` | Sign in page | Render form, call auth API, redirect to dashboard on success |
| `app/auth/signup/page.tsx` | Sign up page | Render form, create account, redirect to dashboard on success |
| `app/dashboard/page.tsx` | Task management | Fetch tasks, render list, handle CRUD operations |
| `middleware.ts` | Auth guard | Check auth state, redirect unauth to signin |

### Components

| Component | Responsibility | Props |
|-----------|-----------------|-------|
| `TaskList.tsx` | Render list of tasks | `tasks: Task[]`, callbacks for actions |
| `TaskForm.tsx` | Create/edit task | `onSubmit`, `isLoading`, `error` |
| `TaskItem.tsx` | Single task row | `task`, `onComplete`, `onDelete`, `onUpdate` |
| `ErrorBoundary.tsx` | Catch rendering errors | `children` |
| `LoadingSpinner.tsx` | Loading indicator | `size`, `color` |

### Libraries

| Module | Purpose | Key Functions |
|--------|---------|----------------|
| `lib/api/client.ts` | API HTTP client | Attach JWT, handle errors, base request setup |
| `lib/api/tasks.ts` | Task API calls | `getTasks()`, `createTask()`, `updateTask()`, `deleteTask()` |
| `lib/api/auth.ts` | Auth API calls | `signup()`, `signin()`, `getSession()`, `logout()` |
| `lib/auth/config.ts` | Better Auth config | JWT plugin settings, secret, endpoints |
| `lib/auth/hooks.ts` | Auth context hooks | `useAuth()`, `useIsAuthenticated()` |
| `types/index.ts` | TypeScript definitions | `User`, `Task`, `Session`, `APIError` |

---

## Data Flow Examples

### Example 1: User Signs Up

```
1. User fills signup form (email, password)
   ↓
2. Form component calls api/auth.ts → signup()
   ↓
3. API client adds headers, POST /api/auth/signup
   ↓
4. Backend returns token + user
   ↓
5. Better Auth stores token in httpOnly cookie
   ↓
6. useAuth() hook updates context
   ↓
7. Middleware sees authenticated state
   ↓
8. Redirect to /dashboard
```

### Example 2: User Creates Task

```
1. User types task title, clicks "Add"
   ↓
2. TaskForm calls api/tasks.ts → createTask(title)
   ↓
3. API client:
   - Gets JWT from cookie/header
   - Attaches Authorization: Bearer {token}
   - POST /api/tasks with { title }
   ↓
4. Backend validates owner (via JWT), creates task
   ↓
5. Returns 201 + new task
   ↓
6. Component adds to local state
   ↓
7. TaskList re-renders with new item
```

### Example 3: Session Expires

```
1. User tries to fetch tasks
   ↓
2. API returns 401 Unauthorized
   ↓
3. API client catches 401
   ↓
4. Clears auth context
   ↓
5. Middleware redirects to /auth/signin
   ↓
6. User sees "Session expired" message
   ↓
7. User signs in again to continue
```

---

## Component Structure Example

### TaskList Component

```typescript
// frontend/src/components/TaskList.tsx

interface TaskListProps {
  tasks: Task[]
  onTaskComplete: (id: string, completed: boolean) => Promise<void>
  onTaskDelete: (id: string) => Promise<void>
  onTaskUpdate: (id: string, title: string) => Promise<void>
  isLoading: boolean
  error?: string
}

export function TaskList({
  tasks,
  onTaskComplete,
  onTaskDelete,
  onTaskUpdate,
  isLoading,
  error,
}: TaskListProps) {
  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />
  if (tasks.length === 0) return <EmptyState />

  return (
    <ul>
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onComplete={() => onTaskComplete(task.id, !task.completed)}
          onDelete={() => onTaskDelete(task.id)}
          onUpdate={(title) => onTaskUpdate(task.id, title)}
        />
      ))}
    </ul>
  )
}
```

### Dashboard Page Using Component

```typescript
// frontend/src/app/dashboard/page.tsx

import { useEffect, useState } from "react"
import { useAuth } from "@/lib/auth/hooks"
import { getTasks, createTask } from "@/lib/api/tasks"
import { TaskList, TaskForm } from "@/components"
import type { Task } from "@/types"

export default function DashboardPage() {
  const { user, isAuthenticated } = useAuth()
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>()

  // Fetch tasks on mount
  useEffect(() => {
    if (isAuthenticated) {
      getTasks()
        .then(setTasks)
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false))
    }
  }, [isAuthenticated])

  const handleCreate = async (title: string) => {
    try {
      const task = await createTask(title)
      setTasks([...tasks, task])
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <h1>Tasks for {user?.email}</h1>
      <TaskForm onSubmit={handleCreate} />
      <TaskList tasks={tasks} isLoading={loading} error={error} />
    </div>
  )
}
```

---

## JWT Handling

### Automatic Attachment (via API Client)

```typescript
// frontend/src/lib/api/client.ts

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

apiClient.interceptors.request.use((config) => {
  // Better Auth handles cookies automatically
  // OR manually attach token if needed:
  // const token = localStorage.getItem("auth_token")
  // if (token) {
  //   config.headers.Authorization = `Bearer ${token}`
  // }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired, redirect to signin
      // Better Auth or middleware handles this
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

---

## Error Handling Patterns

### Component-Level Error

```typescript
function TaskForm() {
  const [error, setError] = useState<string>()

  const handleSubmit = async (title: string) => {
    try {
      await createTask(title)
      setError(undefined)
    } catch (err) {
      if (err.status === 400) {
        setError("Invalid task title")
      } else if (err.status === 401) {
        // Handled by middleware
      } else {
        setError("Failed to create task")
      }
    }
  }

  return (
    <form>
      {error && <ErrorAlert message={error} />}
      <input type="text" onChange={(e) => setTitle(e.target.value)} />
      <button onClick={() => handleSubmit(title)}>Add Task</button>
    </form>
  )
}
```

### Middleware-Level Error

```typescript
// frontend/src/middleware.ts

import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-token")?.value

  if (!token && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/auth/signin", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*"],
}
```

---

## Testing Checklist

Before moving to implementation phase:

- [ ] Understand data models (User, Task, Session)
- [ ] Review API contracts (auth, task endpoints)
- [ ] Know JWT handling approach (cookies + fallback)
- [ ] Understand error handling (3-layer approach)
- [ ] Know component structure (reusable TaskList, TaskForm)
- [ ] Understand data flow (signup → dashboard → task creation)
- [ ] Know responsive design approach (Tailwind + mobile-first)
- [ ] Review project structure (app/, components/, lib/)

---

## Environment Setup Requirements

### Frontend
- Node.js 16+
- npm or yarn
- Next.js 16+
- Better Auth + JWT plugin
- Tailwind CSS

### Backend Integration
- Spec-1 (Task API) running on `http://localhost:8000` or configured endpoint
- Spec-2 (Auth API) running on `http://localhost:5000` or configured endpoint
- CORS enabled for frontend origin
- JWT shared secret configured

### Environment Variables
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_URL=http://localhost:5000
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-secret-here
```

---

## Next Steps

1. **Initialize Next.js project** with App Router
2. **Setup Better Auth** with JWT plugin
3. **Create authentication pages** (signin, signup)
4. **Setup middleware** for route protection
5. **Build task components** (TaskList, TaskForm, TaskItem)
6. **Implement API client** with JWT attachment
7. **Connect components to APIs**
8. **Add error handling and loading states**
9. **Test end-to-end flow**
10. **Deploy and validate with backend**
