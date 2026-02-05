# Quickstart: Auth Integration Testing (Multi-User)

## Backend Standalone (curl/Postman)
1. Start backend: `cd backend && uvicorn src.main:app --reload`
2. Ensure users table has test users (signup via frontend or insert manually).
3. Mock JWTs (HS256, sub=user_id; generate with AUTH_SECRET):
   - User1: sub="1234567890", jwt1=...
   - User2: sub="0987654321", jwt2=...
4. Tests:
   ```
   # Test auth
   curl -H "Authorization: Bearer $jwt1" http://localhost:8000/test-auth
   # Expect: {"user_id": "1234567890", "email": "user1@example.com"}

   # List own tasks
   curl -H "Authorization: Bearer $jwt1" http://localhost:8000/api/tasks
   # Expect: tasks with user_id=1234567890 or []

   # Create task (User1)
   curl -X POST -H "Authorization: Bearer $jwt1" -H "Content-Type: application/json" \
     -d '{"title": "Task1", "description": "Desc1"}' http://localhost:8000/api/tasks

   # List User1 tasks: should see Task1
   curl -H "Authorization: Bearer $jwt1" http://localhost:8000/api/tasks

   # Access User1 task with User2 JWT: 403
   curl -H "Authorization: Bearer $jwt2" http://localhost:8000/api/tasks/<task1_id>
   # Expect: 403 "Access denied"

   # Invalid/missing token: 401
   curl http://localhost:8000/api/tasks
   curl -H "Authorization: Bearer invalid" http://localhost:8000/api/tasks
   ```

## Full Flow
1. Frontend: `npm run dev`
2. User1 signup/login → JWT1 → CRUD own tasks
3. User2 → sees only own tasks, cannot access User1 tasks (403)
