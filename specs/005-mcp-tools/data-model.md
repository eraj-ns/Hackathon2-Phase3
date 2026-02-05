# Data Model: MCP Server & Tooling Integration

## Entities

### Task
Represents a user's task with properties like id, title, description, completion status, and associated user_id

**Fields**:
- id: UUID (primary key)
- title: String (required, max 255 characters)
- description: String (optional, max 1000 characters)
- completed: Boolean (default false)
- user_id: UUID (foreign key to User, required)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated, updates on change)

**Validation rules**:
- Title must not be empty
- Title must be less than 255 characters
- Description must be less than 1000 characters if provided

**State transitions**:
- Created with completed = false
- Can be updated to change title/description
- Can be marked as completed (completed = true)
- Can be marked as incomplete (completed = false)

### User
Represents a system user with unique identifier used for data isolation

**Fields**:
- id: UUID (primary key)
- email: String (unique, required)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated, updates on change)

**Validation rules**:
- Email must be valid email format
- Email must be unique across all users

### Tool Response
Structured data containing either operation results or error information

**Success Response Fields**:
- success: Boolean (always true for success)
- data: Object (contains the operation result)
- message: String (optional, human-readable message)

**Error Response Fields**:
- success: Boolean (always false for errors)
- error: Object (contains error details)
- error.type: String (error category)
- error.message: String (human-readable error message)
- error.code: String (optional, error code)

### MCP Tool Parameters
Input parameters for each tool

**add_task Parameters**:
- user_id: UUID (required)
- title: String (required)
- description: String (optional)

**list_tasks Parameters**:
- user_id: UUID (required)
- completed_only: Boolean (optional, default false)
- limit: Integer (optional, default 100)

**update_task Parameters**:
- user_id: UUID (required)
- task_id: UUID (required)
- title: String (optional)
- description: String (optional)
- completed: Boolean (optional)

**complete_task Parameters**:
- user_id: UUID (required)
- task_id: UUID (required)

**delete_task Parameters**:
- user_id: UUID (required)
- task_id: UUID (required)