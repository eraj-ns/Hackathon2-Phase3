# Frontend API Integration Contracts

**Feature**: Frontend Application & Full-Stack Integration
**Date**: 2026-01-24
**Purpose**: Define integration contracts between frontend and backend (Spec-1) and authentication (Spec-2)

---

## Overview

Frontend integrates with two backend systems:

1. **Authentication API** (Spec-2): User signup, signin, session management
2. **Task API** (Spec-1): CRUD operations for tasks

All API calls include JWT token in Authorization header. Backend returns standard HTTP status codes and JSON responses.

---

## Authentication API Contracts (Spec-2 Integration)

### Entry Point
**Base URL**: `http://localhost:5000/api/auth` (or `https://{backend-host}/api/auth`)

### 1. Signup
Create new user account and return session

**Endpoint**: `POST /api/auth/signup`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "User Name"
}
```

**Response (201)**:
```json
{
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "User Name",
    "createdAt": "2026-01-24T10:00:00Z"
  },
  "token": "eyJhbGc..."
}
```

**Response (400)**:
```json
{
  "code": "VALIDATION_ERROR",
  "message": "Invalid email format",
  "details": {
    "email": "Must be valid email"
  }
}
```

**Response (409)**:
```json
{
  "code": "USER_EXISTS",
  "message": "User with this email already exists"
}
```

**Frontend Handling**:
- Extract token and user from response
- Store token in httpOnly cookie (Better Auth)
- Redirect to `/dashboard` on success
- Show validation errors on form

---

### 2. Signin
Authenticate existing user and return session

**Endpoint**: `POST /api/auth/signin`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200)**:
```json
{
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "User Name",
    "createdAt": "2026-01-24T10:00:00Z",
    "lastLogin": "2026-01-24T10:15:00Z"
  },
  "token": "eyJhbGc..."
}
```

**Response (401)**:
```json
{
  "code": "INVALID_CREDENTIALS",
  "message": "Invalid email or password"
}
```

**Frontend Handling**:
- Extract token and user
- Store in session via Better Auth
- Redirect to `/dashboard` on success
- Show "Invalid credentials" on 401

---

### 3. Session Validation
Check if current session is valid

**Endpoint**: `GET /api/auth/me`

**Headers**:
```
Authorization: Bearer {token}
```

**Response (200)**:
```json
{
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "User Name"
  },
  "expiresAt": "2026-01-25T10:15:00Z"
}
```

**Response (401)**:
```json
{
  "code": "UNAUTHORIZED",
  "message": "Token expired or invalid"
}
```

**Frontend Handling**:
- Called on app initialization to restore session
- Used in middleware to check protected routes
- On 401, redirect to signin and clear session

---

### 4. Logout
Invalidate current session

**Endpoint**: `POST /api/auth/logout`

**Headers**:
```
Authorization: Bearer {token}
```

**Response (200)**:
```json
{
  "message": "Logged out successfully"
}
```

**Frontend Handling**:
- Clear token from cookies
- Clear auth context
- Redirect to `/auth/signin`

---

## Task API Contracts (Spec-1 Integration)

### Entry Point
**Base URL**: `http://localhost:8000/api/tasks` (or `https://{api-host}/api/tasks`)

**Authentication**: All requests require JWT in Authorization header

---

### 1. Get All Tasks for Current User
Retrieve list of tasks belonging to authenticated user

**Endpoint**: `GET /api/tasks`

**Headers**:
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Response (200)**:
```json
{
  "tasks": [
    {
      "id": "task-uuid-1",
      "userId": "user-uuid",
      "title": "Buy groceries",
      "completed": false,
      "createdAt": "2026-01-24T09:00:00Z",
      "updatedAt": "2026-01-24T09:00:00Z"
    },
    {
      "id": "task-uuid-2",
      "userId": "user-uuid",
      "title": "Finish report",
      "completed": true,
      "createdAt": "2026-01-23T14:00:00Z",
      "updatedAt": "2026-01-24T10:00:00Z"
    }
  ]
}
```

**Response (401)**:
```json
{
  "code": "UNAUTHORIZED",
  "message": "Invalid or expired token"
}
```

**Frontend Handling**:
- Call on dashboard mount
- Set loading state while fetching
- Update task list state with response
- Show error message on 401

---

### 2. Create New Task
Add a new task for authenticated user

**Endpoint**: `POST /api/tasks`

**Headers**:
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request**:
```json
{
  "title": "New task description"
}
```

**Response (201)**:
```json
{
  "task": {
    "id": "new-task-uuid",
    "userId": "user-uuid",
    "title": "New task description",
    "completed": false,
    "createdAt": "2026-01-24T10:30:00Z",
    "updatedAt": "2026-01-24T10:30:00Z"
  }
}
```

**Response (400)**:
```json
{
  "code": "VALIDATION_ERROR",
  "message": "Validation failed",
  "details": {
    "title": "Title must be 1-500 characters"
  }
}
```

**Response (401)**:
```json
{
  "code": "UNAUTHORIZED",
  "message": "Token missing or invalid"
}
```

**Frontend Handling**:
- Show loading spinner on form submit
- Disable form inputs while submitting
- Add returned task to local state
- Show success/error message
- Clear form on success

---

### 3. Update Task
Modify task title or completion status

**Endpoint**: `PATCH /api/tasks/{taskId}`

**Headers**:
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request** (update title):
```json
{
  "title": "Updated task description"
}
```

**Request** (toggle completed):
```json
{
  "completed": true
}
```

**Response (200)**:
```json
{
  "task": {
    "id": "task-uuid",
    "userId": "user-uuid",
    "title": "Updated task description",
    "completed": true,
    "createdAt": "2026-01-24T09:00:00Z",
    "updatedAt": "2026-01-24T10:35:00Z"
  }
}
```

**Response (404)**:
```json
{
  "code": "NOT_FOUND",
  "message": "Task not found or does not belong to user"
}
```

**Response (400)**:
```json
{
  "code": "VALIDATION_ERROR",
  "message": "Invalid update",
  "details": {
    "title": "Title must be 1-500 characters"
  }
}
```

**Frontend Handling**:
- Optimistic UI update (show change immediately)
- Show loading state on affected task item
- Revert change if API returns error
- Show error message on failure

---

### 4. Delete Task
Remove a task

**Endpoint**: `DELETE /api/tasks/{taskId}`

**Headers**:
```
Authorization: Bearer {token}
```

**Response (204)**:
No content (task deleted successfully)

**Response (404)**:
```json
{
  "code": "NOT_FOUND",
  "message": "Task not found or does not belong to user"
}
```

**Response (401)**:
```json
{
  "code": "UNAUTHORIZED",
  "message": "Token missing or invalid"
}
```

**Frontend Handling**:
- Show confirmation dialog before delete
- Optimistic removal from UI
- Revert if 404 error
- Show success/error message

---

## Error Handling Standards

### HTTP Status Codes

| Code | Scenario | Frontend Action |
|------|----------|-----------------|
| 200 | Success | Process response |
| 201 | Created | Process response, show success |
| 204 | Deleted | Remove from list, show success |
| 400 | Bad Request | Show field-specific errors |
| 401 | Unauthorized | Redirect to signin, show "session expired" |
| 403 | Forbidden | Show "access denied" message |
| 404 | Not Found | Show "not found" or refresh list |
| 500 | Server Error | Show "server error" with retry |

### Error Response Format

All error responses follow this format:

```json
{
  "code": "ERROR_CODE",
  "message": "Human-readable message",
  "details": {}
}
```

**Common Error Codes**:
- `UNAUTHORIZED`: Missing/invalid token
- `VALIDATION_ERROR`: Invalid input data
- `NOT_FOUND`: Resource doesn't exist
- `CONFLICT`: Resource already exists (duplicate)
- `SERVER_ERROR`: Backend error

---

## JWT Token Format & Headers

### Token Placement
**Preferred**: httpOnly cookie set by server
**Fallback**: Authorization header

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Claims (for reference)
```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234654290
}
```

### Cookie Format (set by backend)
```
Set-Cookie: auth-token=eyJhbGc...; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=86400
```

---

## Timeout & Retry Strategy

### Timeouts
- Initial request timeout: 30 seconds
- Retry timeout: 60 seconds

### Automatic Retries
- Retry on network timeout: Yes (max 3 times with exponential backoff)
- Retry on 5xx errors: Yes (max 2 times)
- Retry on 4xx errors: No (user input error)

### Backoff Pattern
```
Attempt 1: Immediate
Attempt 2: After 1 second
Attempt 3: After 2 seconds
```

---

## CORS & Cross-Domain

### Required Backend CORS Configuration
```
Access-Control-Allow-Origin: {frontend-host}
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
```

---

## Integration Checklist

- [ ] Signup endpoint accessible and returns token
- [ ] Signin endpoint accessible and returns token
- [ ] Session validation endpoint works
- [ ] Task list endpoint returns user's tasks only
- [ ] Create task returns 201 with new task
- [ ] Update task modifies and returns updated task
- [ ] Delete task returns 204 and task removed
- [ ] 401 responses trigger signin redirect
- [ ] JWT token attached to all requests
- [ ] Error responses follow standard format
- [ ] CORS headers allow frontend requests
- [ ] Timeouts and retries work correctly
