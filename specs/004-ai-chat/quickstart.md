# Quickstart Guide: AI Chat Agent & Conversation System

## Overview

This guide provides step-by-step instructions to set up and run the AI Chat Agent & Conversation System locally. The system integrates with the existing todo application to provide natural language processing for task management.

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm/yarn
- PostgreSQL (or Neon Serverless PostgreSQL connection)
- OpenAI API key
- Better Auth configuration

## Environment Setup

### Backend Setup

1. **Install Python Dependencies**
```bash
cd backend
pip install fastapi sqlmodel uvicorn openai python-multipart better-exceptions python-jose[cryptography] passlib[bcrypt] psycopg2-binary
```

2. **Configure Environment Variables**
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
OPENAI_API_KEY=your_openai_api_key_here
BETTER_AUTH_SECRET=your_jwt_secret_here
BETTER_AUTH_URL=http://localhost:8000
```

3. **Database Setup**
```bash
# Apply existing database migrations
python -c "from backend.database import create_db_and_tables; create_db_and_tables()"

# Create new tables for conversations and messages
# (These will be created by the new models)
```

### Frontend Setup

1. **Install JavaScript Dependencies**
```bash
cd frontend
npm install
```

2. **Configure Environment Variables**
Update `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Running the Application

### Start Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Start Frontend Server
```bash
cd frontend
npm run dev
```

## API Endpoints

Once running, the following endpoints will be available:

- `POST /api/{user_id}/chat` - Main chat endpoint for AI interactions
- `GET /api/{user_id}/conversations` - List user's conversations
- `GET /api/{user_id}/conversations/{conversation_id}/messages` - Get messages in a conversation

## Testing the Chat Functionality

### 1. Authentication
First, register and authenticate a user through the existing auth endpoints:
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login to get JWT token

### 2. Send a Chat Message
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a new task to buy groceries tomorrow"
  }'
```

### 3. View Conversations
```bash
curl -X GET http://localhost:8000/api/{user_id}/conversations \
  -H "Authorization: Bearer {jwt_token}"
```

## Development Workflow

### Adding New MCP Tools
1. Create new tool in `backend/mcp_tools/`
2. Register the tool with the OpenAI Assistant
3. Update the agent's instructions to use the new tool

### Updating the AI Agent
1. Modify the system prompt in `backend/agents/ai_chat_agent.py`
2. Adjust tool configurations as needed
3. Test the changes with sample conversations

### Frontend Integration
1. Add new chat UI components in `frontend/src/app/chat/`
2. Connect to backend API using existing auth patterns
3. Handle loading states and error cases appropriately

## Troubleshooting

### Common Issues

1. **OpenAI API Connection Errors**
   - Verify `OPENAI_API_KEY` is set correctly
   - Check network connectivity to OpenAI services

2. **Database Connection Issues**
   - Verify `DATABASE_URL` is correct
   - Ensure database server is running

3. **Authentication Failures**
   - Check JWT token validity
   - Verify `BETTER_AUTH_SECRET` matches backend

### Debugging Tips

1. Enable verbose logging in backend:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. Check the conversation and message tables after chat interactions to ensure persistence is working.

3. Monitor API response times to ensure the AI service is responding within acceptable limits.

## Next Steps

1. Implement the frontend chat UI components
2. Add conversation history display
3. Integrate with existing task management functionality
4. Add error handling and user feedback mechanisms