# Data Model & Entity Definitions

**Feature**: Frontend Application & Full-Stack Integration
**Date**: 2026-01-24
**Scope**: Frontend application data structures and their relationships to backend entities

## Frontend Data Models

### User Entity (from Spec-2, consumed by frontend)

**Responsibility**: Authentication system (Spec-2) manages; frontend reads via auth state

```typescript
interface User {
  id: string                    // Unique user identifier
  email: string                 // User email (unique)
  name?: string                 // User display name (optional)
  createdAt: ISO8601DateTime    // Account creation timestamp
  lastLogin?: ISO8601DateTime   // Last login time
}
```

**Frontend Access Pattern**:
- Retrieved from Better Auth session during login/signup
- Stored in auth context via @better-auth/react
- Not persisted locally; refreshed on page load via session check

---

### Task Entity (from Spec-1, consumed by frontend)

**Responsibility**: Backend (Spec-1) manages persistence; frontend fetches, displays, and sends mutations

```typescript
interface Task {
  id: string                    // Unique task identifier (UUID)
  userId: string                // Owner user ID (enforced on backend)
  title: string                 // Task description/title
  completed: boolean            // Completion status (default: false)
  createdAt: ISO8601DateTime    // Creation timestamp
  updatedAt: ISO8601DateTime    // Last update timestamp
}
```

**Frontend State Management**:
```typescript
interface TasksPageState {
  tasks: Task[]                 // Current user's task list
  loading: boolean              // Fetching in progress
  error?: string                // Error message if fetch failed
  lastSyncAt?: ISO8601DateTime  // When tasks were last fetched
}
```

**Validation Rules** (Frontend):
- title: Required, 1-500 characters
- completed: Boolean only
- Other fields: Read-only from backend

---

### Session Entity (from Spec-2, managed by frontend)

**Responsibility**: Better Auth manages; frontend accesses via hooks

```typescript
interface Session {
  token: string                 // JWT token (httpOnly cookie or header)
  user: User                    // Current authenticated user
  expiresAt: ISO8601DateTime    // Token expiration time
  isValid: boolean              // Whether session is still active
}
```

**Frontend Behavior**:
- Check session validity before protected routes
- Automatic refresh before expiration (Better Auth handles)
- Clear session on logout
- Redirect to signin if session invalid (401 response)

---

### API Error Entity

**Responsibility**: Standardized error responses from backend (Spec-1)

```typescript
interface APIError {
  status: number                // HTTP status code (400, 401, 403, 500, etc.)
  code: string                  // Error code (e.g., "VALIDATION_ERROR", "UNAUTHORIZED")
  message: string               // Human-readable error message
  details?: Record<string, any> // Additional context (e.g., validation field errors)
}
```

**Frontend Handling**:
```typescript
// Error response types
type ValidationError = { field: string; message: string }[]
type AuthError = { reason: "expired" | "invalid" | "missing" }
type ServerError = { retryAfter?: number }
```

---

## State Management Architecture

### Frontend Context Structure

```typescript
// Root layout context
interface AppContextType {
  auth: {
    user: User | null
    isAuthenticated: boolean
    isLoading: boolean
    error?: string
  }
  tasks: {
    items: Task[]
    loading: boolean
    error?: string
  }
  ui: {
    showNotification?: {
      type: "success" | "error" | "info"
      message: string
    }
  }
}
```

### Component Props Interface

```typescript
// Page components receive auth state
interface ProtectedPageProps {
  user: User
}

// Task components
interface TaskItemProps {
  task: Task
  onComplete: (taskId: string) => Promise<void>
  onDelete: (taskId: string) => Promise<void>
  onUpdate: (taskId: string, title: string) => Promise<void>
}

interface TaskFormProps {
  onSubmit: (title: string) => Promise<void>
  isLoading: boolean
  error?: string
}
```

---

## Data Flow Diagram

```
User Action
  ↓
Frontend Component (TaskForm)
  ↓
API Client (with JWT)
  ↓
Backend REST API (Spec-1)
  ↓
Database (Neon PostgreSQL)
  ↓
Backend Validation & Response
  ↓
API Client (handle errors)
  ↓
Frontend State Update
  ↓
Component Re-render
```

---

## Type Safety

All data models will have corresponding TypeScript interfaces in `frontend/src/types/index.ts`:

- `User`: From auth system
- `Task`: CRUD operations
- `Session`: Auth state
- `APIError`: Error standardization
- `CreateTaskInput`: Form submission
- `UpdateTaskInput`: Task edits

---

## Notes

- All timestamps use ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)
- User IDs are UUIDs (from Spec-2)
- Task IDs are UUIDs (from Spec-1)
- Frontend does NOT store sensitive data (tokens managed by Better Auth/cookies)
- Backend (Spec-1) is source of truth for all data
- Frontend state is ephemeral; refreshes on navigation or page reload
