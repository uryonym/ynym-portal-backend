# Implementation Plan: Task Management

**Branch**: `001-task-management` | **Date**: 2025-11-12 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-task-management/spec.md`

## Summary

タスク管理機能の実装計画。ユーザーがタスク一覧を表示・作成・編集・削除できるバックエンド API と、対応する Pydantic スキーマを設計する。Task エンティティは単一で、ユーザー認証は後続機能として扱う。

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: FastAPI, SQLModel, asyncpg, Pydantic v2
**Storage**: PostgreSQL 12+ (asyncpg ドライバ)
**Testing**: pytest, pytest-asyncio
**Target Platform**: Linux/Web API server
**Project Type**: Backend Web API (single project structure `app/`)
**Performance Goals**: 1000 req/s, <200ms p95 レスポンス時間
**Constraints**: 1000 タスク以上をリスト表示時にも性能劣化なし
**Scale/Scope**: 初期バージョンは単一ユーザー想定、将来的に マルチユーザー対応

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

✅ **I. 非同期優先 (Async-First)**: FastAPI + asyncpg で完全非同期対応
✅ **II. 型安全性**: Python 3.12 型ヒント、mypy strict mode、Pydantic v2
✅ **III. テスト駆動**: pytest ユニット・統合テスト体制
✅ **IV. レイヤー分離**: API → Schema → Service → Model 層の厳密分離
✅ **V. コード品質**: ruff + mypy 自動検証
✅ **VI. ドキュメント**: Docstring + MkDocs 整備
✅ **VII. エラーハンドリング**: カスタム例外クラス (`ValidationException`, `NotFoundException`)
✅ **UUID 戦略**: Task.id は UUID (RFC 4122) で実装

## Project Structure

### Documentation (this feature)

```text
specs/001-task-management/
├── plan.md              # This file (実装計画)
├── spec.md              # 機能仕様書
├── research.md          # Phase 0 出力 (技術リサーチ結果)
├── data-model.md        # Phase 1 出力 (データモデル設計)
├── quickstart.md        # Phase 1 出力 (開発クイックスタート)
├── contracts/           # Phase 1 出力 (API コントラクト)
│   └── task_api.openapi.yaml
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
app/
├── models/
│   ├── __init__.py
│   ├── base.py          # UUIDModel ベースクラス（タイムスタンプ、UUID PK）
│   └── task.py          # Task モデル（NEW）
├── schemas/
│   ├── __init__.py
│   └── task.py          # TaskCreate, TaskUpdate, TaskResponse スキーマ（NEW）
├── services/
│   ├── __init__.py
│   └── task_service.py  # タスク CRUD ビジネスロジック（NEW）
├── api/
│   ├── __init__.py
│   ├── router.py        # ルータ登録（メイン）
│   └── endpoints/
│       ├── __init__.py
│       └── tasks.py     # GET /tasks, POST /tasks, PUT /tasks/{id}, DELETE /tasks/{id}（NEW）
├── config.py
├── database.py
└── main.py

tests/
├── unit/
│   ├── test_task_service.py     # TaskService のユニットテスト（NEW）
│   └── test_task_schemas.py     # Pydantic スキーマバリデーション（NEW）
└── integration/
    └── test_task_endpoints.py   # API エンドポイント統合テスト（NEW）
```

**Structure Decision**: 単一プロジェクト構造。既存の app/ ディレクトリに Task 関連機能を集約。ユーザー認証は後続実装のため、現在はスコープ外。

## Phase 0: Research & Clarification

**Status**: 進行中

### 技術的な明確化項目

1. **JSON シリアライゼーション**: UUID と datetime の JSON 表現方法の確認
2. **ソート仕様の実装**: 期日ソート + 作成日時フォールバックの SQL/ORM 実装方法
3. **テスト用固定値**: ユーザー ID（将来 FK として参照）の仮定値

### 研究結果

_Phase 0 完了後に詳細を追加_
