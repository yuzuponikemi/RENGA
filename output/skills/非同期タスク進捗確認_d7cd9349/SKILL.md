---
name: 非同期タスク進捗確認
skill_id: d7cd9349-53ad-4f59-80f2-885a2d029c59
version: 1.0.0
category: 非同期タスク進捗確認
status: public
source_count: 7
unique_user_count: 1
variables:
- task_id
- task_name
- progress_check_instruction
- wakeup_seconds
- output_file_path
- result_summary_target
triggers:
- タスクの進捗を確認して
- バックグラウンドジョブの状態をチェック
- 非同期処理の完了を監視
- パイプラインの進捗レポート
- タスクが終わったら教えて
---

# 非同期タスク進捗確認

**説明**: バックグラウンドタスクの進捗を確認し、状況に応じて再スケジュールや結果通知を行う
**ステータス**: ✅ 公開中 | **ソース数**: 7 件 | **ユニークユーザー**: 1 人 | **カテゴリ**: 非同期タスク進捗確認

---

## テンプレートプロンプト

```
Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. {progress_check_instruction}. If still running, schedule {wakeup_seconds}s wakeup. If pipeline finished or failed, read {output_file_path} for full details, summarize {result_summary_target}, and push notification to user.
```

## 変数一覧

- `{{task_id}}`: バックグラウンドタスクのID（例: {タスクID}）
- `{{task_name}}`: タスクの表示名（例: {プロジェクト名} {処理内容}）
- `{{progress_check_instruction}}`: 進捗確認の具体的な指示（例: Report which pass/step it's on. If still on {ステップ名}, schedule {数値}s wakeup. If on {別のステップ名}, schedule {数値}s wakeup.）
- `{{wakeup_seconds}}`: 再スケジュールする秒数（例: {数値}）
- `{{output_file_path}}`: 結果ファイルのフルパス（例: {出力ディレクトリ}/tasks/{タスクID}.output）
- `{{result_summary_target}}`: 結果を要約する対象（例: {評価指標} and {主要コンテンツ}）

## 活用シーン

- 長時間かかる要約タスクの進捗を定期的に確認したい
- 複数ステップのパイプライン処理の完了を待って結果を通知したい
- バックグラウンドで実行中の非同期処理の各フェーズを監視したい

## トリガーフレーズ

- `タスクの進捗を確認して`
- `バックグラウンドジョブの状態をチェック`
- `非同期処理の完了を監視`
- `パイプラインの進捗レポート`
- `タスクが終わったら教えて`

---

## 具体インスタンス

### インスタンス 1: 要約+ファクトチェック進捗確認

> 元プロンプト: *Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. Report which pass/step it'*

**変数の値**
  - `task_id`: {task_id}
  - `task_name`: {task_name}
  - `progress_check_instruction`: Report which pass/step it's on. If still on summary, schedule 270s wakeup. If on factcheck, schedule 120s wakeup.
  - `wakeup_seconds`: 120
  - `output_file_path`: {output_file_path}
  - `result_summary_target`: score and key content

**実際のプロンプト**
```
Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. Report which pass/step it's on. If still on summary, schedule 270s wakeup. If on factcheck, schedule 120s wakeup. If pipeline finished or failed, read {output_file_path} for full details, summarize score and key content, and push notification to user.
```

---

### インスタンス 2: ファクトチェックイテレーション監視

> 元プロンプト: *Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. Look for iter 3 score (📊 ス*

**変数の値**
  - `task_id`: {task_id}
  - `task_name`: {task_name}
  - `progress_check_instruction`: Look for iter 3 score (📊 スコア: XX/100 after イテレーション 3/5). If still running, schedule 120s wakeup.
  - `wakeup_seconds`: 120
  - `output_file_path`: {output_file_path}
  - `result_summary_target`: final score and key topics

**実際のプロンプト**
```
Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. Look for iter 3 score (📊 スコア: XX/100 after イテレーション 3/5). If still running, schedule 120s wakeup. If pipeline finished or failed, read {output_file_path} for full details, summarize final score and key topics, and push notification to user.
```
