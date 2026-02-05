# Quickstart Guide: MCP Server & Tooling Integration

## Prerequisites

- Python 3.11+
- pip package manager
- Access to Neon Serverless PostgreSQL database
- Official MCP SDK

## Setup Instructions

### 1. Install Dependencies

```bash
pip install python-mcp-sdk sqlmodel psycopg2-binary python-dotenv
```

### 2. Environment Configuration

Create a `.env` file with your database connection details:

```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### 3. Start the MCP Server

```python
from backend.src.mcp.server import start_mcp_server

if __name__ == "__main__":
    start_mcp_server(host="localhost", port=3000)
```

## Using the MCP Tools

Once the server is running, the following tools will be available:

### add_task
```json
{
  "user_id": "uuid-string",
  "title": "Task title",
  "description": "Optional description"
}
```

### list_tasks
```json
{
  "user_id": "uuid-string",
  "completed_only": false,
  "limit": 100
}
```

### update_task
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string",
  "title": "New title",
  "description": "New description",
  "completed": true
}
```

### complete_task
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string"
}
```

### delete_task
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string"
}
```

## Error Handling

All tools return structured responses. Successful operations return:

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

Failed operations return:

```json
{
  "success": false,
  "error": {
    "type": "error-type",
    "message": "Human-readable error message",
    "code": "optional-error-code"
  }
}
```

## Testing the Integration

Run the following tests to verify the MCP tools work correctly:

```bash
# Unit tests
pytest tests/unit/test_mcp_tools.py

# Integration tests
pytest tests/integration/test_mcp_integration.py
pytest tests/integration/test_data_isolation.py
```