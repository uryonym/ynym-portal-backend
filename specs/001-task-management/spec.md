# Feature Specification: Task Management

**Feature Branch**: `001-task-management`
**Created**: 2025-11-08
**Status**: Draft
**Input**: User description: "タスク管理機能を作ります。タスクを一覧で見ることができ、追加ボタンを押すとモーダルが開いて、タスク内容を入力し新規作成します。タスクの一覧をタップするとそのタスクを編集、または削除することができます。入力する内容はタスクタイトル、詳細、期日、完了したかどうかです。"

## User Scenarios & Testing _(mandatory)_

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - View All Tasks (Priority: P1)

ユーザーがタスク管理画面にアクセスして、すべてのタスクを一覧表示で確認できます。この基本的な表示機能がなければタスク管理は成立しないため、最高優先度とします。

**Why this priority**: タスク管理システムの最も基本的な機能。ユーザーが現在のタスク状況を把握できる最初のステップです。

**Independent Test**: ユーザーがアプリケーションを開くと、作成済みのタスクがすべてリスト形式で表示され、完了状態が視覚的に区別できることで検証できます。

**Acceptance Scenarios**:

1. **Given** タスクが 3 件作成されている, **When** ユーザーがタスク管理画面を開く, **Then** すべての 3 件のタスクが一覧表示される
2. **Given** 完了したタスクと未完了のタスクが混在している, **When** タスク一覧を確認する, **Then** 各タスクの完了状態が明確に表示される
3. **Given** タスクが 1 件もない, **When** タスク管理画面を開く, **Then** 「タスクはありません」などの空状態メッセージが表示される

---

### User Story 2 - Create New Task via Modal (Priority: P1)

ユーザーが追加ボタンを押すとモーダルが開き、タスク情報を入力して新規タスクを作成します。この機能はタスク管理システムの中核的な機能です。

**Why this priority**: タスクの作成機能なくしてタスク管理は成立しません。ユーザーが最初に必要とする操作です。

**Independent Test**: ユーザーが追加ボタンをクリック → モーダルが表示 → 必要な情報を入力 → 保存 → タスク一覧に新しいタスクが追加されることで検証できます。

**Acceptance Scenarios**:

1. **Given** タスク一覧画面が表示されている, **When** 追加ボタンを押す, **Then** 入力フォームを含むモーダルが開く
2. **Given** モーダルが開いている, **When** タスクタイトル「買い物」、詳細「牛乳を買う」、期日「2025-11-15」、完了状態「未完了」を入力して保存ボタンを押す, **Then** モーダルが閉じてタスク一覧に新しいタスクが表示される
3. **Given** 入力フォームが表示されている, **When** キャンセルボタンを押す, **Then** モーダルが閉じて一覧画面に戻る
4. **Given** モーダルが開いている, **When** 必須項目（タスクタイトル）を空のまま保存を押す, **Then** エラーメッセージが表示されて保存されない

---

### User Story 3 - Edit Existing Task (Priority: P2)

ユーザーがタスク一覧からタスクをタップして、そのタスクの内容を編集できます。情報更新は日常的な操作です。

**Why this priority**: タスク情報の更新はよく発生する操作ですが、作成・表示よりは優先度が低くなります。

**Independent Test**: ユーザーがタスクをタップ → 編集モーダルが表示 → 情報を変更 → 保存 → タスク一覧に反映されることで検証できます。

**Acceptance Scenarios**:

1. **Given** タスク一覧が表示されている, **When** 既存のタスクをタップする, **Then** 編集モーダルが開いて現在の情報が表示される
2. **Given** 編集モーダルが開いている, **When** タスクタイトルを「買い物」から「食材の買い物」に変更して保存する, **Then** タスク一覧で更新されたタイトルが表示される
3. **Given** 編集モーダルが開いている, **When** 期日を変更する, **Then** 新しい期日がタスク一覧に反映される
4. **Given** 編集モーダルが開いている, **When** 完了状態をトグルする, **Then** タスク一覧での表示状態が更新される

---

### User Story 4 - Delete Task (Priority: P2)

ユーザーが不要になったタスクを削除できます。タスク管理の効率性を維持するために必要な機能です。

**Why this priority**: 削除機能はタスク管理に必要ですが、作成・表示・編集よりは優先度が低くなります。

**Independent Test**: ユーザーがタスクを選択して削除操作 → 確認ダイアログ → 確認後にタスク一覧から消えることで検証できます。

**Acceptance Scenarios**:

1. **Given** タスク一覧が表示されている, **When** タスクをタップして編集モーダルを開く, **Then** 削除ボタンが表示される
2. **Given** 削除ボタンが表示されている, **When** 削除ボタンをクリックする, **Then** 「このタスクを削除しますか？」という確認ダイアログが表示される
3. **Given** 確認ダイアログが表示されている, **When** 「削除」を選択する, **Then** タスクが削除されてタスク一覧から消える
4. **Given** 確認ダイアログが表示されている, **When** 「キャンセル」を選択する, **Then** タスクは削除されずにモーダルが閉じる

### Edge Cases

- タスクタイトルが空の状態で保存しようとした場合、エラーメッセージが表示される
- タスクタイトルが非常に長い場合（例：500 文字以上）、一覧表示で適切に省略される
- 期日がない場合（オプション）、「期日なし」と表示される
- 複数のタスクが同じ期日を持つ場合、一覧に正しく表示される
- タスクは期日が近い順に表示される。期日が設定されていないタスクは、作成日時の古い順に表示される
- 期日が過ぎたタスクについて、特別な視覚表現は行わない。期日情報を正確に表示し、ユーザーが「期日を過ぎています」というテキスト表示で判断できるようにする

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST display all tasks in a list format on the task management screen
- **FR-002**: System MUST allow users to create a new task by clicking an add button that opens a modal form
- **FR-003**: System MUST require users to enter a task title (mandatory field) to create or update a task
- **FR-004**: System MUST allow users to enter an optional task description
- **FR-005**: System MUST allow users to set a due date for each task (optional field)
- **FR-006**: System MUST allow users to mark a task as complete or incomplete
- **FR-007**: System MUST enable users to edit an existing task by tapping it in the list and modifying its details
- **FR-008**: System MUST persist all task changes (create, edit, delete) in the database
- **FR-009**: System MUST allow users to delete a task with a confirmation dialog
- **FR-010**: System MUST display appropriate validation error messages when required fields are missing
- **FR-011**: System MUST close the modal after successful task creation or update
- **FR-012**: System MUST display an empty state message when no tasks exist
- **FR-013**: System MUST show the complete/incomplete status visually distinct for each task in the list
- **FR-014**: System MUST sort tasks by due date in ascending order (nearest due date first). Tasks without a due date MUST be sorted by creation date in ascending order and displayed after tasks with due dates
- **FR-015**: System MUST display overdue status information through text labels (e.g., "期日を過ぎています") without special visual styling like colors or warning icons

### Key Entities

- **Task**: Represents a single task item with the following attributes:
  - **Task ID**: Unique identifier for the task
  - **Title**: The name/subject of the task (required)
  - **Description**: Detailed information about the task (optional)
  - **Due Date**: The deadline for completing the task (optional)
  - **Complete Status**: Boolean flag indicating whether the task is completed
  - **Created Date**: Timestamp when the task was created
  - **Updated Date**: Timestamp when the task was last modified

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users can create a new task and see it appear in the list within 2 seconds
- **SC-002**: Users can complete the full task lifecycle (create, view, edit, delete) within 5 minutes for all basic operations
- **SC-003**: The task list displays all existing tasks with 100% accuracy
- **SC-004**: Users can distinguish between completed and incomplete tasks visually on the first view without additional interaction
- **SC-005**: System supports at least 1000 tasks in a single list without performance degradation
- **SC-006**: Task creation and modification operations complete successfully 99% of the time
- **SC-007**: Users successfully complete their intended task operation on the first attempt at least 95% of the time

## Assumptions

- タスク完了状態はシンプルなトグル（完了/未完了）の 2 値型です
- 複数ユーザー間でのタスク共有は初期バージョンでは不要と仮定します
- タスクには所有者（作成ユーザー）が自動的に関連付けられます
- 期日は日付形式（YYYY-MM-DD）で保存されます
- タスク一覧は同期的に更新される（リアルタイム更新は初期バージョンでは不要）
- ブラウザのローカルストレージまたはバックエンド DB でタスクが永続化されます
