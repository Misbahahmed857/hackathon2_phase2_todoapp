---
name: database-skill
description: Design and manage databases with proper schema, tables, and migrations. Use for backend and full-stack projects.
---

# Database Design & Migrations

## Instructions

1. **Schema Design**
   - Identify entities and relationships
   - Normalize data (avoid redundancy)
   - Define primary and foreign keys

2. **Table Creation**
   - Use clear, meaningful table names
   - Define appropriate data types
   - Add constraints (NOT NULL, UNIQUE, DEFAULT)

3. **Migrations**
   - Create versioned migration files
   - Support up and down migrations
   - Never modify old migrations after production

4. **Relationships**
   - One-to-One
   - One-to-Many
   - Many-to-Many (junction tables)

## Best Practices
- Use snake_case for table and column names
- Always index foreign keys
- Keep migrations small and reversible
- Document schema changes clearly
- Avoid storing derived or duplicate data

## Example Structure

### SQL Table Example
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
