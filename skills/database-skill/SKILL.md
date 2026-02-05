---
name: database-skill
description: Design and manage databases including tables, migrations, and schemas. Use for backend and data-driven applications.
---

# Database Design & Management

## Instructions

1. **Schema Design**
   - Identify entities and relationships
   - Normalize tables (avoid redundancy)
   - Define primary and foreign keys

2. **Table Creation**
   - Use appropriate data types
   - Apply constraints (NOT NULL, UNIQUE)
   - Add indexes for performance

3. **Migrations**
   - Version-controlled schema changes
   - Create up/down migration files
   - Never modify existing migrations

4. **Relationships**
   - One-to-One
   - One-to-Many
   - Many-to-Many using junction tables

## Best Practices
- Follow naming conventions (snake_case)
- Keep schemas simple and scalable
- Use migrations for all schema changes
- Avoid storing derived data
- Plan for future growth

## Example Structure
```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(200),
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
