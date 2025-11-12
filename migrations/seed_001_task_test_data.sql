-- Test Data for Task Management
-- ファイル: migrations/seed_001_task_test_data.sql
-- 説明: テスト用タスクデータを挿入（開発/テスト環境用）
-- 注意: 本番環境では実行しないでください

-- UUID 生成用ユーザー ID（固定値）
-- 実装時に User テーブルが完成したら、実際のユーザー ID に置き換える
DO $$
DECLARE
    v_user_id UUID := '550e8400-e29b-41d4-a716-446655440000';
    v_task1_id UUID;
    v_task2_id UUID;
    v_task3_id UUID;
    v_now TIMESTAMP WITH TIME ZONE := CURRENT_TIMESTAMP;
BEGIN
    -- テスト用タスク 1: 期日あり、未完了
    INSERT INTO "task" (user_id, title, description, is_completed, due_date, "order", created_at, updated_at)
    VALUES (
        v_user_id,
        '初期設定を完了する',
        'プロジェクト初期設定タスク: 環境変数設定、依存関係インストール、ローカル起動確認',
        FALSE,
        CURRENT_DATE + INTERVAL '7 days',
        1,
        v_now,
        v_now
    ) RETURNING id INTO v_task1_id;

    -- テスト用タスク 2: 期日なし、未完了
    INSERT INTO "task" (user_id, title, description, is_completed, due_date, "order", created_at, updated_at)
    VALUES (
        v_user_id,
        'API エンドポイント実装',
        'REST API エンドポイント実装: GET /tasks, POST /tasks, PUT /tasks/{id}, DELETE /tasks/{id}',
        FALSE,
        NULL,  -- 期日なし
        2,
        v_now,
        v_now
    ) RETURNING id INTO v_task2_id;

    -- テスト用タスク 3: 期日あり、完了済み
    INSERT INTO "task" (user_id, title, description, is_completed, completed_at, due_date, "order", created_at, updated_at)
    VALUES (
        v_user_id,
        'データベース設計ドキュメント作成',
        'Task テーブルのデータモデル設計とドキュメント化',
        TRUE,
        v_now - INTERVAL '2 days',  -- 2日前に完了
        CURRENT_DATE - INTERVAL '3 days',  -- 3日前が期日
        3,
        v_now - INTERVAL '5 days',  -- 5日前作成
        v_now
    ) RETURNING id INTO v_task3_id;

    -- 確認メッセージ
    RAISE NOTICE 'テストデータ挿入完了:';
    RAISE NOTICE '  - Task 1 (ID: %): 期日あり、未完了', v_task1_id;
    RAISE NOTICE '  - Task 2 (ID: %): 期日なし、未完了', v_task2_id;
    RAISE NOTICE '  - Task 3 (ID: %): 期日あり、完了済み', v_task3_id;
END $$;

-- 挿入されたデータを確認
SELECT
    id,
    user_id,
    title,
    is_completed,
    due_date,
    completed_at,
    created_at,
    updated_at
FROM "task"
ORDER BY "order", created_at ASC;
