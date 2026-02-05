# AI Chat Agent API Endpoints

## Overview

This document describes the API endpoints for the AI Chat Agent & Conversation System.

## Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Endpoints

### POST /api/{user_id}/chat

Process natural language input and return AI response with conversation state management.

#### Parameters
- `{user_id}` (path): The ID of the authenticated user making the request. Must match the current user's ID.

#### Request Body
```json
{
  "message": "Natural language input from user",
  "conversation_id": "optional conversation UUID to continue existing conversation",
  "metadata": {
    "client_timestamp": "ISO 8601 timestamp of client request",
    "device_info": "optional device information"
  }
}
```

#### Response
```json
{
  "conversation_id": "UUID of the conversation",
  "message_id": "UUID of the AI response message",
  "response": "AI-generated response text",
  "intent": {
    "type": "create_task|update_task|delete_task|view_tasks|search_tasks|mark_complete|mark_incomplete|unknown",
    "confidence": 0.85,
    "action_taken": "description of action taken if applicable"
  },
  "timestamp": "ISO 8601 timestamp of server response",
  "next_action": "follow_up|required_input|completed"
}
```

#### Example Request
```bash
curl -X POST http://localhost:8000/api/123e4567-e89b-12d3-a456-426614174000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "message": "Add a task to buy groceries tomorrow",
    "metadata": {
      "client_timestamp": "2026-02-01T10:00:00Z"
    }
  }'
```

#### Response Codes
- `200 OK`: Successful chat interaction
- `400 Bad Request`: Invalid request format or parameters
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User attempting to access another user's conversation
- `404 Not Found`: Conversation ID provided but not found
- `422 Unprocessable Entity`: Invalid message content or parameters
- `500 Internal Server Error`: AI service or database error

---

### GET /api/{user_id}/conversations

Retrieve list of user's conversations with pagination support.

#### Parameters
- `{user_id}` (path): The ID of the authenticated user. Must match JWT token.
- `page` (query, optional): Page number for pagination (default: 1)
- `limit` (query, optional): Number of results per page (default: 10, max: 50)
- `sort_by` (query, optional): Field to sort by (default: "updated_at")
- `order` (query, optional): Sort order (asc|desc, default: "desc")

#### Response
```json
{
  "conversations": [
    {
      "id": "UUID of conversation",
      "title": "Conversation title",
      "created_at": "ISO 8601 timestamp",
      "updated_at": "ISO 8601 timestamp",
      "is_active": true,
      "message_count": 15
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "pages": 3
  }
}
```

#### Response Codes
- `200 OK`: Successfully retrieved conversations
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User attempting to access another user's conversations
- `422 Unprocessable Entity`: Invalid query parameters
- `500 Internal Server Error`: Database error

---

### GET /api/{user_id}/conversations/{conversation_id}/messages

Retrieve messages for a specific conversation with pagination support.

#### Parameters
- `{user_id}` (path): The ID of the authenticated user
- `{conversation_id}` (path): The ID of the conversation
- `page` (query, optional): Page number for pagination (default: 1)
- `limit` (query, optional): Number of results per page (default: 20, max: 100)

#### Response
```json
{
  "messages": [
    {
      "id": "UUID of message",
      "role": "user|assistant|system|tool",
      "content": "Message content",
      "created_at": "ISO 8601 timestamp",
      "metadata": {
        "intent": "create_task|update_task|...",
        "confidence": 0.85
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 15,
    "pages": 1
  }
}
```

#### Response Codes
- `200 OK`: Successfully retrieved messages
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User not authorized to access this conversation
- `404 Not Found`: Conversation not found
- `422 Unprocessable Entity`: Invalid query parameters
- `500 Internal Server Error`: Database error

## Error Response Format

All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Optional additional error details"
  }
}
```

## Common Error Codes

- `INVALID_JWT_TOKEN`: JWT token is invalid or expired
- `USER_MISMATCH`: Provided user_id doesn't match JWT token user_id
- `CONVERSATION_NOT_FOUND`: Requested conversation doesn't exist
- `MESSAGE_TOO_LONG`: Message exceeds maximum length
- `INVALID_CONVERSATION_ID`: Conversation ID is not a valid UUID
- `AI_SERVICE_UNAVAILABLE`: OpenAI service is temporarily unavailable
- `RATE_LIMIT_EXCEEDED`: User has exceeded rate limits