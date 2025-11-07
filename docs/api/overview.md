# API Overview

This is the API for the ynym Portal Backend system.

## Base URL

- Development: `http://localhost:8000/api`
- Production: (To be configured)

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

All protected endpoints require an `Authorization` header:

```
Authorization: Bearer <token>
```

## Response Format

### Success Response (2xx)

```json
{
  "data": {},
  "message": "Success"
}
```

### Error Response (4xx, 5xx)

```json
{
  "detail": "Error message",
  "status_code": 400,
  "error_type": "ValidationException"
}
```

## Endpoints

See [endpoints.md](endpoints.md) for detailed endpoint documentation.
