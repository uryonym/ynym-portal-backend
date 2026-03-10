# Note Categories Spec

## Purpose

ユーザーがノートをカテゴリで分類し管理できる機能の要件を定義する。

## Requirements

### Requirement: カテゴリ作成

システムは、`user_id` にひも付くカテゴリを作成できなければならない。`name` は必須とし、作成時に `created_at` と `updated_at` を設定しなければならない。

#### Scenario: カテゴリ作成

- **WHEN** `user_id` と `name` を指定して作成を要求する
- **THEN** カテゴリが作成され、`created_at` と `updated_at` が設定される

### Requirement: カテゴリ取得

システムは、`user_id` とカテゴリIDを指定してカテゴリを取得できなければならない。

#### Scenario: 単体取得

- **WHEN** `user_id` とカテゴリIDを指定して取得を要求する
- **THEN** 対象カテゴリが返される

### Requirement: カテゴリ一覧

システムは、`user_id` にひも付くカテゴリ一覧を取得できなければならない。既定の並び順は `name` の昇順とする。

#### Scenario: 既定順での一覧取得

- **WHEN** `user_id` を指定して一覧取得を要求する
- **THEN** カテゴリが `name` の昇順で返される

### Requirement: カテゴリ更新

システムは、カテゴリの `name` を更新できなければならない。更新時に `updated_at` を更新しなければならない。

#### Scenario: カテゴリ名の更新

- **WHEN** `name` を更新する
- **THEN** カテゴリが更新され、`updated_at` が更新される

### Requirement: カテゴリ削除

システムは、カテゴリを削除できなければならない。カテゴリ削除時、ひも付くノートは未分類（`category_id` が未設定）にならなければならない。

#### Scenario: カテゴリ削除

- **WHEN** カテゴリIDを指定して削除を要求する
- **THEN** カテゴリが削除され、ひも付くノートの `category_id` が未設定になる
