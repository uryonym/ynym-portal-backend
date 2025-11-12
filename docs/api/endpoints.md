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

## Tasks

### GET /api/tasks

タスク一覧を取得します。

**説明:**

ユーザーのすべてのタスクを取得します。タスクは以下のルールに従ってソートされます：

1. **期日昇順 (最も近い期日が最初)**: `due_date ASC NULLS LAST`
2. **期日なしのタスク**: 期日ありのタスク後に表示
3. **同一グループ内での作成日時昇順**: `created_at ASC`

**Query Parameters:**

| Parameter | Type    | Default | Description                     |
| --------- | ------- | ------- | ------------------------------- |
| skip      | integer | 0       | スキップするレコード数          |
| limit     | integer | 100     | 取得するレコード数（最大 1000） |

**Response (200 OK):**

```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "550e8400-e29b-41d4-a716-446655440001",
      "title": "期日ありのタスク",
      "description": "これはタスクの説明です",
      "is_completed": false,
      "completed_at": null,
      "due_date": "2025-11-30",
      "order": 0,
      "created_at": "2025-11-12T10:30:00",
      "updated_at": "2025-11-12T10:30:00"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "user_id": "550e8400-e29b-41d4-a716-446655440001",
      "title": "期日なしのタスク",
      "description": "期日が設定されていません",
      "is_completed": false,
      "completed_at": null,
      "due_date": null,
      "order": 0,
      "created_at": "2025-11-12T11:00:00",
      "updated_at": "2025-11-12T11:00:00"
    }
  ],
  "message": "タスク一覧を取得しました"
}
```

**Response (500 Internal Server Error):**

```json
{
  "detail": "Internal server error"
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
