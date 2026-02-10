## ADDED Requirements

### Requirement: ノート作成
システムは、`user_id` にひも付くノートを作成できなければならない。`title` と `body` は必須とし、`category_id` は任意とする。作成時に `created_at` と `updated_at` を設定しなければならない。

#### Scenario: 必須項目での作成
- **WHEN** `user_id`、`title`、`body` を指定して作成を要求する
- **THEN** ノートが作成され、`created_at` と `updated_at` が設定される

### Requirement: ノート取得
システムは、`user_id` とノートIDを指定してノートを取得できなければならない。

#### Scenario: 単体取得
- **WHEN** `user_id` とノートIDを指定して取得を要求する
- **THEN** 対象ノートが返される

### Requirement: ノート一覧
システムは、`user_id` にひも付くノート一覧を取得できなければならない。既定の並び順は「カテゴリ名の昇順、次にタイトルの昇順」とし、カテゴリ未設定のノートは末尾に並べなければならない。

#### Scenario: 既定順での一覧取得
- **WHEN** `user_id` を指定して一覧取得を要求する
- **THEN** ノートがカテゴリ名、次にタイトルの昇順で返され、カテゴリ未設定のノートは末尾に並ぶ

### Requirement: ノート更新
システムは、ノートの `title`、`body`、`category_id` を更新できなければならない。更新時に `updated_at` を更新しなければならない。

#### Scenario: タイトルと本文の更新
- **WHEN** `title` と `body` を更新する
- **THEN** ノートが更新され、`updated_at` が更新される

### Requirement: ノート削除
システムは、ノートを削除できなければならない。

#### Scenario: ノート削除
- **WHEN** ノートIDを指定して削除を要求する
- **THEN** ノートが削除され、再取得時に存在しないことが示される
