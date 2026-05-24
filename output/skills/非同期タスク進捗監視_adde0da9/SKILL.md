---
name: 非同期タスク進捗監視
skill_id: adde0da9-d55f-4498-a47c-8dacde1dc76b
version: 1.0.0
category: 非同期タスク進捗監視
status: public
source_count: 7
unique_user_count: 1
variables:
- task_id
- task_name
- wakeup_seconds
- output_path
triggers:
- タスクの進捗を確認して
- バックグラウンドジョブの状態をチェック
- 処理が終わったか見てきて
- 非同期タスクの状況を教えて
- パイプラインの進捗を監視して
---

# 非同期タスク進捗監視

**説明**: バックグラウンドタスクの進捗を確認し、結果を通知する
**ステータス**: ✅ 公開中 | **ソース数**: 7 件 | **ユニークユーザー**: 1 人 | **カテゴリ**: 非同期タスク進捗監視

---

## テンプレートプロンプト

```
Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. Report which iteration it's on and the current score if visible. If still running, schedule {wakeup_seconds}s wakeup. If pipeline finished or failed, read {output_path} for full details, summarize final score and key topics, and push notification to user.
```

## 変数一覧

- `{{task_id}}`: 監視対象のバックグラウンドタスクID（例: ランダムな英数字）
- `{{task_name}}`: タスクの名称や説明（例: データ処理パイプライン）
- `{{wakeup_seconds}}`: 再確認までの待機時間（秒）（例: 120）
- `{{output_path}}`: 完了時・失敗時に読み込む出力ファイルのフルパス（例: /tmp/tasks/output.txt）

## 活用シーン

- 長時間のデータ分析ジョブの進捗確認と結果通知
- バッチ処理のパイプライン監視と完了通知
- 機械学習モデルのトレーニング進捗確認とスコア報告

## トリガーフレーズ

- `タスクの進捗を確認して`
- `バックグラウンドジョブの状態をチェック`
- `処理が終わったか見てきて`
- `非同期タスクの状況を教えて`
- `パイプラインの進捗を監視して`

---

## 具体インスタンス

### インスタンス 1: ファクトチェック監視

> 元プロンプト: *Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. Report which iteration it'*

**変数の値**
  - `task_id`: {task_id}
  - `task_name`: {task_name}
  - `wakeup_seconds`: {wakeup_seconds}
  - `output_path`: {output_path}

**実際のプロンプト**
```
Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. Report which iteration it's on and the current score if visible. If still running, schedule {wakeup_seconds}s wakeup. If pipeline finished or failed, read {output_path} for full details, summarize final score and key topics, and push notification to user.
```

---

### インスタンス 2: 汎用タスク監視

> 元プロンプト: *Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. Report iteration number an*

**変数の値**
  - `task_id`: {task_id}
  - `task_name`: {task_name}
  - `wakeup_seconds`: {wakeup_seconds}
  - `output_path`: {output_path}

**実際のプロンプト**
```
Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false. Report which iteration it's on and the current score if visible. If still running, schedule {wakeup_seconds}s wakeup. If pipeline finished or failed, read {output_path} for full details, summarize final score and key topics, and push notification to user.
```
