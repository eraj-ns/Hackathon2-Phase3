---
name: backend-routes-and-db
description: Design backend routes, handle requests and responses, and connect applications to databases. Use for building scalable server-side APIs.
---

# Backend Routes & Database Integration

## Instructions

1. **Route generation**
   - Define RESTful routes
   - Use proper HTTP methods (GET, POST, PUT, DELETE)
   - Organize routes by resource

2. **Request & response handling**
   - Validate incoming data
   - Handle query params and request body
   - Send structured JSON responses
   - Implement proper status codes

3. **Database connection**
   - Connect to SQL or NoSQL databases
   - Use environment variables for credentials
   - Handle connection errors gracefully
   - Perform CRUD operations

## Best Practices
- Keep routes modular and clean
- Use controllers/services pattern
- Always validate user input
- Handle errors centrally
- Secure sensitive data with environment variables

## Example Structure
```js
// routes/userRoutes.js
import express from "express";
import { getUsers, createUser } from "../controllers/userController.js";

const router = express.Router();

router.get("/", getUsers);
router.post("/", createUser);

export default router;
