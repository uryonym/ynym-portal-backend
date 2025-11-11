# Research: Task Management Feature

**Date**: 2025-11-12
**Phase**: Phase 0 - Research & Clarification
**Purpose**: 技術的な不明点を解決し、設計フェーズへの準備を完了

## Research Questions & Decisions

### 1. UUID と datetime の JSON シリアライゼーション

**Question**: Pydantic v2 で UUID と datetime (特に timezone aware な datetime) をどのように JSON で表現するか？

**Decision**:

- **UUID**: RFC 4122 形式（ハイフン付き 8-4-4-4-12、例: `550e8400-e29b-41d4-a716-446655440000`）で JSON 出力
- **datetime**: ISO 8601 形式で JSON 出力（例: `2025-11-12T15:30:00+09:00`）
- Pydantic v2 は `ConfigDict` の `json_encoders` パラメータではなく、`field_serializer` デコレータを使用

**Rationale**:

- RFC 4122 は UUID の国際標準形式で相互運用性が高い
- ISO 8601 は datetime の国際標準形式で時刻の曖昧性がない
- Pydantic v2 でのベストプラクティスに従う

**Alternative Considered**:

- UUID を文字列そのままで扱う（トレーシング・ログ出力時は有効だが、API 応答形式に選んだ RFC 4122 で統一）
- datetime を Unix タイムスタンプで表現（機械可読性は高いが、人間が読みにくく、タイムゾーン情報が失われる）

---

### 2. Task ソート仕様の実装（期日 + 作成日時フォールバック）

**Question**: 「期日が近い順」かつ「期日なしは作成日時の古い順」をどのように SQL で実装するか？

**Decision**:

```python
# SQLModel/SQLAlchemy での実装例
from sqlalchemy import func, case, or_

# ソート順序の計算カラム
# 1. 期日ありのタスク: 期日で昇順（近い日時が最初）
# 2. 期日なしのタスク: 作成日時で昇順
sort_key = case(
    (Task.due_date.isnot(None), Task.due_date),  # 期日あり
    else_=func.to_timestamp('2099-12-31')  # 期日なしは無限遠に設定
)

query = (
    select(Task)
    .order_by(sort_key, Task.created_at)
    .where(Task.deleted_at.is_(None))  # 削除フラグ対応（将来）
)
```

**Rationale**:

- CASE ステートメントで条件付きソートが可能
- `func.to_timestamp()` で期日なしを無限遠（2099-12-31）に設定し、期日ありが先に表示される
- SQLAlchemy の ORM 構文で型安全性を保つ

**Alternative Considered**:

- アプリケーション層（Python）でソート（データベースの負荷軽減できるが、大規模データ時に効率が低い）
- SQL の `NULLS LAST` 句の組み合わせ（より簡潔だが、PostgreSQL 依存になる）

→ 本実装では PostgreSQL 依存で問題ないため、`NULLS LAST` を使用する方が簡潔

**修正版実装**:

```python
from sqlalchemy import desc, nulls_last

query = (
    select(Task)
    .order_by(nulls_last(Task.due_date.asc()), Task.created_at.asc())
    .where(Task.deleted_at.is_(None))
)
```

---

### 3. テスト用ユーザー ID の仮定

**Question**: ユーザー認証が後続実装のため、テストやシード データで固定ユーザー ID を使用するか？

**Decision**:

- テスト・シード データでは、固定の UUID を使用する（例: `550e8400-e29b-41d4-a716-446655440000`）
- Task モデルの `user_id` フィールドは現在 FK 制約なしで実装（ユーザーテーブル実装後に FK 追加）
- ユーザー認証実装時は、現在の API に認可ロジックを追加する

**Rationale**:

- 単一テストユーザーで開発を進めやすくなる
- 認証実装後に FK 制約追加時の影響が最小限

**Alternative Considered**:

- 現在から FK 制約を設定（ユーザーテーブルを先に作成必要 → スコープ外拡大）

---

### 4. 削除処理の実装方式

**Question**: タスクの削除は物理削除か論理削除か？

**Decision**:

初期バージョンは **物理削除** で実装。将来的に監査ログが必要になった場合に論理削除へ移行。

- `DELETE FROM task WHERE id = ?`

**Rationale**:

- 仕様書に「削除ボタン」の UI 記載があるが、削除後の履歴要件がない
- シンプルな実装で十分

**Alternative Considered**:

- 論理削除（`deleted_at` タイムスタンプを追加）→ 将来の監査要件に備える方が良いかもしれない

→ **修正**: 将来の拡張性を考慮して、論理削除対応ディレクトリ構造にしておく（`deleted_at` フィールド追加、ただしクエリには `WHERE deleted_at IS NULL` 条件を自動挿入）

---

### 5. 期日の時刻表現

**Question**: 期日は「日付のみ」か「日時」か？

**Decision**:

Pydantic スキーマでは **date 型を使用**（時刻部分は考慮しない）。DB には datetime で保存（時刻は 00:00:00 JST）。

**Rationale**:

- ユーザーが「2025-11-15 に完了したい」という日単位のタスク管理が一般的
- JSON API では `"due_date": "2025-11-15"` と日付形式で出力

**Alternative Considered**:

- datetime で時刻も指定可能にする（より柔軟だが、UI 実装が複雑になる）

---

### 6. バリデーション: 過去日付を期日に設定可能か

**Question**: 期日が過去日付（例: 今日より前の日付）を入力時にバリデーションエラーにするか？

**Decision**:

**バリデーションエラーにしない**。過去の日付設定を許可する。

**Rationale**:

- 仕様書に「期日が過ぎたタスク」の描画要件がある（→ 過去日付が存在可能性を示唆）
- ユーザーが誤って古い日付を入力した場合も修正できるべき

---

## Summary

### Technical Decisions Ratified

| 項目                          | 決定                             | 実装詳細                                                                  |
| ----------------------------- | -------------------------------- | ------------------------------------------------------------------------- |
| UUID シリアライゼーション     | RFC 4122 形式                    | JSON 出力: `550e8400-e29b-41d4-a716-446655440000`                         |
| datetime シリアライゼーション | ISO 8601 形式                    | JSON 出力: `2025-11-12T15:30:00+09:00`                                    |
| ソート実装                    | PostgreSQL の NULLS LAST 句      | `ORDER BY due_date ASC NULLS LAST, created_at ASC`                        |
| ユーザー ID                   | 固定 UUID テスト値               | `550e8400-e29b-41d4-a716-446655440000`                                    |
| 削除処理                      | 論理削除対応設計                 | `deleted_at` フィールド追加、クエリに `WHERE deleted_at IS NULL` 自動挿入 |
| 期日データ型                  | date（スキーマ）+ datetime（DB） | JSON: `"due_date": "2025-11-15"`                                          |
| 過去日付バリデーション        | 許可                             | 特にバリデーション制約なし                                                |

---

## Next Steps

→ **Phase 1** に進み、data-model.md と API contracts を設計・生成する
