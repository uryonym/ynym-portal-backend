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

## (Documentation to be added as authentication endpoints are implemented)

## Vehicles

### GET /api/vehicles

所有する車一覧を取得します。

**説明:**

ユーザーが所有するすべての車を取得します。作成日時の新しい順でソートされて返されます。

**クエリパラメータ:**

| パラメータ | デフォルト | 説明                           |
| ---------- | ---------- | ------------------------------ |
| skip       | 0          | スキップするレコード数         |
| limit      | 100        | 取得するレコード数 (最大 1000) |

**成功レスポンス (200):**

```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "マイカー",
      "seq": "MG-001",
      "maker": "Toyota",
      "model": "Prius",
      "year": 2023,
      "number": "東京 123あ 1234",
      "tank_capacity": 50.0,
      "created_at": "2025-11-16T16:00:00+09:00",
      "updated_at": "2025-11-16T16:00:00+09:00"
    }
  ],
  "message": "車一覧を取得しました"
}
```

---

### POST /api/vehicles

新規車を作成します。

**説明:**

ユーザーが所有する新しい車を作成します。

**リクエストボディ:**

```json
{
  "name": "マイカー",
  "seq": "MG-001",
  "maker": "Toyota",
  "model": "Prius",
  "year": 2023,
  "number": "東京 123あ 1234",
  "tank_capacity": 50.0
}
```

**バリデーション:**

- `name`: 必須、1-255 文字
- `seq`: 必須、1-100 文字
- `maker`: 必須、1-100 文字
- `model`: 必須、1-100 文字
- `year`: オプション
- `number`: オプション、1-50 文字
- `tank_capacity`: オプション、正の数

**成功レスポンス (201):**

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "マイカー",
    "seq": "MG-001",
    "maker": "Toyota",
    "model": "Prius",
    "year": 2023,
    "number": "東京 123あ 1234",
    "tank_capacity": 50.0,
    "created_at": "2025-11-16T16:00:00+09:00",
    "updated_at": "2025-11-16T16:00:00+09:00"
  },
  "message": "車が作成されました"
}
```

**エラーレスポンス (400):**

```json
{
  "errors": ["name: 車名は必須項目です"],
  "message": "入力データが正しくありません"
}
```

---

### GET /api/vehicles/{vehicle_id}

特定の車を取得します。

**説明:**

指定した車 ID の車情報を取得します。

**パスパラメータ:**

- `vehicle_id`: 車 ID (UUID)

**成功レスポンス (200):**

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "マイカー",
    "seq": "MG-001",
    "maker": "Toyota",
    "model": "Prius",
    "year": 2023,
    "number": "東京 123あ 1234",
    "tank_capacity": 50.0,
    "created_at": "2025-11-16T16:00:00+09:00",
    "updated_at": "2025-11-16T16:00:00+09:00"
  },
  "message": "車が取得されました"
}
```

**エラーレスポンス (404):**

```json
{
  "error": "車 ID 550e8400-e29b-41d4-a716-446655440099 が見つかりません",
  "message": "車が見つかりません"
}
```

---

### PUT /api/vehicles/{vehicle_id}

車情報を更新します。

**説明:**

指定した車 ID の車情報を更新します。指定されたフィールドのみが更新されます（部分更新対応）。

**パスパラメータ:**

- `vehicle_id`: 車 ID (UUID)

**リクエストボディ（すべてのフィールドはオプション）:**

```json
{
  "name": "新しい名前",
  "year": 2024
}
```

**成功レスポンス (200):**

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "新しい名前",
    "seq": "MG-001",
    "maker": "Toyota",
    "model": "Prius",
    "year": 2024,
    "number": "東京 123あ 1234",
    "tank_capacity": 50.0,
    "created_at": "2025-11-16T16:00:00+09:00",
    "updated_at": "2025-11-16T16:05:00+09:00"
  },
  "message": "車が更新されました"
}
```

**エラーレスポンス (404):**

```json
{
  "error": "車 ID 550e8400-e29b-41d4-a716-446655440099 が見つかりません",
  "message": "車が見つかりません"
}
```

---

### DELETE /api/vehicles/{vehicle_id}

車を削除します。

**説明:**

指定した車 ID の車を削除します。

**パスパラメータ:**

- `vehicle_id`: 車 ID (UUID)

**成功レスポンス (204):**

レスポンスボディなし

**エラーレスポンス (404):**

```json
{
  "error": "車 ID 550e8400-e29b-41d4-a716-446655440099 が見つかりません",
  "message": "車が見つかりません"
}
```

---

## Error Codes

| Code | Description           |
| ---- | --------------------- |
| 200  | OK                    |
| 201  | Created               |
| 204  | No Content            |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 422  | Validation Error      |
| 500  | Internal Server Error |
