# Advanced Todo App with Modern UI

This is a full-stack todo application featuring a modern UI with advanced task management capabilities.

## Features

### Modern UI Components
- Sleek, contemporary design with gradient backgrounds
- Responsive layout for all device sizes
- Dark/light mode toggle
- Smooth animations and transitions
- Intuitive navigation and user flows

### Advanced Task Management
- **Priority Levels**: Tasks can be assigned low, medium, or high priority
- **Due Dates**: Set deadlines for tasks with calendar integration
- **Categories**: Organize tasks by category (work, personal, etc.)
- **Search & Filter**: Advanced filtering by priority, status, and search terms
- **Statistics Dashboard**: Real-time stats showing task distribution

### Authentication System
- Secure JWT-based authentication
- Sign up and sign in functionality
- Protected routes for authorized users only
- Session management with automatic refresh

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/signin` - Authenticate existing user

### Task Management
- `GET /api/tasks/` - Retrieve all user tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion

### Request/Response Format

#### Create Task
```json
{
  "title": "Task title",
  "description": "Optional description",
  "priority": "low|medium|high",
  "dueDate": "2023-12-31T10:00:00Z",
  "category": "work|personal|other"
}
```

#### Response
```json
{
  "id": "task-id",
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "priority": "medium",
  "due_date": "2023-12-31T10:00:00Z",
  "category": "work",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

## Technology Stack

### Frontend
- Next.js 14+ with App Router
- React 18+
- TypeScript
- Tailwind CSS for styling
- Framer Motion for animations
- Lucide React for icons
- Modern CSS with gradients, shadows, and transitions

### Backend
- FastAPI
- SQLModel for database modeling
- PostgreSQL with Neon
- JWT for authentication
- BCrypt for password hashing

## Setup Instructions

1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies: `npm install`
4. Set up environment variables in `.env` files
5. Run the backend: `python -m src.main`
6. Run the frontend: `npm run dev`

## Environment Variables

### Backend (.env)
```
DATABASE_URL=your_postgresql_connection_string
AUTH_SECRET=your_jwt_secret
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Key Improvements

1. **Modern UI Design**:
   - Contemporary card-based layout
   - Gradient backgrounds and subtle shadows
   - Smooth animations and transitions
   - Responsive design for all screen sizes

2. **Advanced Task Features**:
   - Priority levels for better task organization
   - Due dates for deadline tracking
   - Categorization for task grouping
   - Enhanced filtering and search

3. **Performance Optimizations**:
   - Efficient data fetching
   - Optimistic UI updates
   - Proper error handling

4. **Security Enhancements**:
   - JWT-based authentication
   - Secure password hashing
   - Input validation

## Screenshots

The application features:
- Modern landing page with gradient background
- Elegant sign-in/sign-up forms
- Advanced dashboard with statistics
- Task cards with priority indicators
- Responsive design for mobile and desktop