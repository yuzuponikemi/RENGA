---
name: バックグラウンドタスク進捗確認
skill_id: 2a6738a7-6827-4b5a-bf7d-c7ca88bf5010
version: 1.0.0
category: バックグラウンドタスク進捗確認
status: public
source_count: 12
unique_user_count: 1
variables:
- task_id
- task_name
- step1_name
- step2_name
triggers:
- タスクの進捗を確認して
- バックグラウンドジョブの状況を教えて
- 処理の進行状況はどう？
- パイプラインの状態をチェックして
- ジョブの進捗レポート
---

# バックグラウンドタスク進捗確認

**説明**: 非同期パイプラインの進捗を確認し、状態に応じてアクションを実行する
**ステータス**: ✅ 公開中 | **ソース数**: 12 件 | **ユニークユーザー**: 1 人 | **カテゴリ**: バックグラウンドタスク進捗確認

---

## テンプレートプロンプト

```
Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false to see current progress. If {step1_name} is still running, schedule another wakeup. If {step1_name} finished and {step2_name} started, report progress. If the full pipeline finished, read the output, summarize results, and push a notification to the user.
```

## 変数一覧

- `{{task_id}}`: バックグラウンドタスクのID（例: 英数字の文字列）
- `{{task_name}}`: タスクの説明（例: 特定のパイプライン名と処理手法）
- `{{step1_name}}`: 最初の処理ステップ名（例: 特定のツール名）
- `{{step2_name}}`: 2番目の処理ステップ名（例: 特定の処理名）

## 活用シーン

- 音声処理パイプラインの進捗確認
- 動画変換処理の進捗確認
- データ分析ジョブの進捗確認と結果通知

## トリガーフレーズ

- `タスクの進捗を確認して`
- `バックグラウンドジョブの状況を教えて`
- `処理の進行状況はどう？`
- `パイプラインの状態をチェックして`
- `ジョブの進捗レポート`

---

## 具体インスタンス

### インスタンス 1: ポッドキャストパイプライン進捗確認

> 元プロンプト: *Check the status of background task b8jje7otp (ep347 podcast pipeline with pyannote diarization). Use TaskOutput with bl*

**変数の値**
  - `task_id`: b8jje7otp
  - `task_name`: ep347 podcast pipeline with pyannote diarization
  - `step1_name`: Whisper
  - `step2_name`: diarization

**実際のプロンプト**
```
Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false to see current progress. If {step1_name} is still running, schedule another wakeup. If {step1_name} finished and {step2_name} started, report progress. If the full pipeline finished, read the output, summarize results, and push a notification to the user.
```

---

### インスタンス 2: 動画エンコード進捗確認

> 元プロンプト: *Check the status of background task abc123xyz (video encode pipeline with H.264 compression). Use TaskOutput with block=*

**変数の値**
  - `task_id`: abc123xyz
  - `task_name`: video encode pipeline with H.264 compression
  - `step1_name`: FFmpeg
  - `step2_name`: thumbnail generation

**実際のプロンプト**
```
Check the status of background task {task_id} ({task_name}). Use TaskOutput with block=false to see current progress. If {step1_name} is still running, schedule another wakeup. If {step1_name} finished and {step2_name} started, report progress. If the full pipeline finished, read the output, summarize results, and push a notification to the user.
```
