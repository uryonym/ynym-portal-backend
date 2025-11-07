# API Endpoints

This page documents all available API endpoints.

## Health Check

### GET /api/health

Health check endpoint to verify the API is running.

**Response:**

```json
{
  "status": "ok",
  "environment": "development"
}
```

---

## Users

(Documentation to be added as endpoints are implemented)

---

## Items

(Documentation to be added as endpoints are implemented)

---

## Authentication

(Documentation to be added as authentication endpoints are implemented)

---

## Error Codes

| Code | Description           |
| ---- | --------------------- |
| 200  | OK                    |
| 201  | Created               |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 422  | Validation Error      |
| 500  | Internal Server Error |
