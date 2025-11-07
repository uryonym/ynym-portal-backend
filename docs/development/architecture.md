# Architecture

## Overview

The application follows a layered architecture:

```
┌─────────────────────────────────────┐
│        FastAPI Application          │
│    (app/main.py, app/api/...)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      API Layer (Endpoints)          │
│    (app/api/endpoints/...)          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Service Layer                  │
│    (app/services/...)               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Data Layer (Models)            │
│    (app/models/..., SQLModel)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        Database (PostgreSQL)        │
└─────────────────────────────────────┘
```

## Key Components

### API Layer (`app/api/`)

- Handles HTTP requests and responses
- Manages request validation and response serialization
- Uses Pydantic v2 schemas for validation
- Located in `app/api/endpoints/`

### Service Layer (`app/services/`)

- Contains business logic
- Orchestrates data operations
- Handles error handling and data transformations

### Data Layer (`app/models/`)

- Defines SQLModel models
- Represents database schema
- Handles database operations

### Security (`app/security/`)

- JWT token management
- Password hashing and verification
- Authentication and authorization logic

### Utils (`app/utils/`)

- Shared utilities
- Custom exceptions
- Logging configuration

### Configuration (`app/config.py`)

- Environment-based settings
- Uses Pydantic Settings
- Loads from `.env` file

### Database (`app/database.py`)

- Async PostgreSQL connection
- Session management
- Uses SQLModel and asyncpg

## Data Flow

1. **Request** → FastAPI receives HTTP request
2. **Validation** → Pydantic schema validates input
3. **Endpoint** → Handler processes request
4. **Service** → Business logic execution
5. **Database** → SQLModel/asyncpg executes queries
6. **Response** → Response schema serializes data
7. **Output** → FastAPI returns JSON response

## Error Handling

- Custom exceptions in `app/utils/exceptions.py`
- Global error handlers (to be implemented)
- Standard error response format
