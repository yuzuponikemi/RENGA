---
name: 章立て調査結果確認
skill_id: ae5e160e-acf7-4c97-bd97-e0d33e1a3cd7
version: 1.0.0
category: 章立て調査結果確認
status: public
source_count: 7
unique_user_count: 1
variables:
- agent_name
- book_count
- task_ids
- book_names
- output_dir
- task_id_pattern
- reports_dir
- additional_instructions
triggers:
- 章立て調査の結果を確認して
- 調査の進捗を確認して
- レポートを確認して
- タスクの完了確認をして
- 調査結果をまとめて
---

# 章立て調査結果確認

**説明**: AI実行ログから章立て調査の完了確認と結果まとめ
**ステータス**: ✅ 公開中 | **ソース数**: 7 件 | **ユニークユーザー**: 1 人 | **カテゴリ**: 章立て調査結果確認

---

## テンプレートプロンプト

```
{agent_name} で実行した{book_count}冊の章立て調査結果を確認してください。タスクID: {task_ids}（{book_names}）。各出力ファイルは {output_dir}/tasks/{task_id_pattern}.output。また {reports_dir} も確認してください。{additional_instructions}
```

## 変数一覧

- `{{agent_name}}`: 実行エージェント名（例: 任意のエージェント名）
- `{{book_count}}`: 調査対象の書籍数（例: 3, 1）
- `{{task_ids}}`: タスクIDのリスト（例: 複数のタスクID）
- `{{book_names}}`: 書籍名のリスト（例: 書籍A, 書籍B）
- `{{output_dir}}`: 出力ファイルが格納されているディレクトリパス（例: /tmp/output/）
- `{{task_id_pattern}}`: タスクIDのファイル名パターン（例: {id}.output）
- `{{reports_dir}}`: レポートディレクトリのパス（例: ~/reports/）
- `{{additional_instructions}}`: 追加指示（例: 完了していれば結果をまとめてください、完了していなければ進捗を報告してください）

## 活用シーン

- 複数書籍の章立て調査の一括完了確認
- 単一書籍の章立て調査の進捗確認と結果まとめ
- 調査完了後の最終レポート確認と要約

## トリガーフレーズ

- `章立て調査の結果を確認して`
- `調査の進捗を確認して`
- `レポートを確認して`
- `タスクの完了確認をして`
- `調査結果をまとめて`

---

## 具体インスタンス

### インスタンス 1: 3冊一括確認

> 元プロンプト: *{agent_name} で実行した3冊の章立て調査結果を確認してください。タスクID: {task_id_1}（{book_name_1}）, {task_id_2}（{book_name_2}）, {task_id_3}（{book_n*

**変数の値**
  - `agent_name`: {agent_name}
  - `book_count`: 3
  - `task_ids`: {task_id_1}, {task_id_2}, {task_id_3}
  - `book_names`: {book_name_1}, {book_name_2}, {book_name_3}
  - `output_dir`: {output_dir}
  - `task_id_pattern`: {id}.output
  - `reports_dir`: {reports_dir}
  - `additional_instructions`: 

**実際のプロンプト**
```
{agent_name} で実行した3冊の章立て調査結果を確認してください。タスクID: {task_id_1}（{book_name_1}）, {task_id_2}（{book_name_2}）, {task_id_3}（{book_name_3}）。各出力ファイルは {output_dir}/tasks/{task_id_pattern}　また reports/ ディレクトリ {reports_dir} も確認してください。
```

---

### インスタンス 2: 単体完了確認

> 元プロンプト: *{agent_name} {book_name}の章立て調査の完了確認。tail -30 で出力末尾確認: {output_dir}/tasks/{task_id}.output。reports/ も確認。完了していれば章立て結果をまとめて*

**変数の値**
  - `agent_name`: {agent_name}
  - `book_count`: 1
  - `task_ids`: {task_id}
  - `book_names`: {book_name}
  - `output_dir`: {output_dir}
  - `task_id_pattern`: {id}.output
  - `reports_dir`: {reports_dir}
  - `additional_instructions`: tail -30 で出力末尾確認。完了していれば章立て結果をまとめてください。まだ Reflection 中であれば、context を 16384 に落として再実行するか提案してください。

**実際のプロンプト**
```
{agent_name} {book_name}の章立て調査の完了確認。tail -30 で出力末尾確認: {output_dir}/tasks/{task_id}.output。reports/ も確認。完了していれば章立て結果をまとめてください。まだ Reflection 中であれば、context を 16384 に落として再実行するか提案してください。
```
