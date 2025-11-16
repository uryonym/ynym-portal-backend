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

### POST /api/tasks

新規タスクを作成します。

**説明:**

ユーザーが新しいタスクを作成します。タスク作成後、created_at と updated_at は自動的に現在の JST 時刻に設定されます。

**Request Body:**

| Field        | Type    | Required | Description                      |
| ------------ | ------- | -------- | -------------------------------- |
| title        | string  | Yes      | タスクのタイトル (1-255 文字)    |
| description  | string  | No       | タスクの説明 (0-2000 文字)       |
| due_date     | string  | No       | 期日 (ISO 8601 形式: YYYY-MM-DD) |
| is_completed | boolean | No       | 完了状態 (デフォルト: false)     |

**Example Request:**

```json
{
  "title": "新規タスク",
  "description": "これはテストタスクです",
  "due_date": "2025-12-31",
  "is_completed": false
}
```

**Response (201 Created):**

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "新規タスク",
    "description": "これはテストタスクです",
    "is_completed": false,
    "completed_at": null,
    "due_date": "2025-12-31",
    "order": 0,
    "created_at": "2025-11-14T20:54:07+09:00",
    "updated_at": "2025-11-14T20:54:07+09:00"
  },
  "message": "タスクが作成されました"
}
```

**Response (400 Bad Request):**

バリデーションエラーが発生した場合。

```json
{
  "errors": ["title: Field required"],
  "message": "入力データが正しくありません"
}
```

例：

- `title` が省略された場合: `"title: Field required"`
- `title` が空文字列の場合: `"title: String should have at least 1 character"`
- `title` が 255 文字を超える場合: `"title: String should have at most 255 characters"`
- `description` が 2000 文字を超える場合: `"description: String should have at most 2000 characters"`

**Response (500 Internal Server Error):**

サーバーエラーが発生した場合。

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
