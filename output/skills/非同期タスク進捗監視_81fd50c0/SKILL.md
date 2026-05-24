---
name: 非同期タスク進捗監視
skill_id: 81fd50c0-e541-46cd-b545-b37aaf6dc3b4
version: 1.0.0
category: 非同期タスク進捗監視
status: pending
source_count: 22
unique_user_count: 2
variables:
- task_id
- task_description
- stage1_name
- stage2_name
- time_threshold
- short_interval
- long_interval
- output_path
triggers:
- タスクの進捗を確認して
- バックグラウンドジョブの状態をチェック
- 処理が終わったか見てきて
- パイプラインの状況を教えて
- タスク完了を監視して
---

# 非同期タスク進捗監視

**説明**: バックグラウンドタスクの状態を確認し、完了までポーリングする
**ステータス**: 🔒 審査中 | **ソース数**: 22 件 | **ユニークユーザー**: 2 人 | **カテゴリ**: 非同期タスク進捗監視

---

## テンプレートプロンプト

```
Check the status of background task {task_id} ({task_description}). Use TaskOutput with block=false to see current progress. If {stage1_name} is still running and under {time_threshold} min, schedule another wakeup in {short_interval}s. If {stage1_name} is over {time_threshold} min or {stage2_name} started, schedule {long_interval}s wakeup. If the full pipeline finished or failed, read {output_path} for full details, summarize, and push a notification to the user.
```

## 変数一覧

- `{{task_id}}`: 監視対象のバックグラウンドタスクID
- `{{task_description}}`: タスクの簡単な説明
- `{{stage1_name}}`: 最初の処理ステージ名
- `{{stage2_name}}`: 2番目の処理ステージ名
- `{{time_threshold}}`: 最初のステージの経過時間しきい値（分）
- `{{short_interval}}`: 短いウェイクアップ間隔（秒）
- `{{long_interval}}`: 長いウェイクアップ間隔（秒）
- `{{output_path}}`: タスク出力ファイルのフルパス

## 活用シーン

- 長時間の音声認識パイプラインの完了を待つ
- バッチデータ処理ジョブの進捗を定期的に確認する
- 機械学習モデルのトレーニング完了を監視する

## トリガーフレーズ

- `タスクの進捗を確認して`
- `バックグラウンドジョブの状態をチェック`
- `処理が終わったか見てきて`
- `パイプラインの状況を教えて`
- `タスク完了を監視して`

---

## 具体インスタンス

### インスタンス 1: ポッドキャストパイプライン監視

> 元プロンプト: *Check the status of background task {task_id} ({task_description}). Use TaskOutput with block=false to see current progr*

**変数の値**
  - `task_id`: {task_id}
  - `task_description`: {task_description}
  - `stage1_name`: {stage1_name}
  - `stage2_name`: {stage2_name}
  - `time_threshold`: {time_threshold}
  - `short_interval`: {short_interval}
  - `long_interval`: {long_interval}
  - `output_path`: {output_path}

**実際のプロンプト**
```
Check the status of background task {task_id} ({task_description}). Use TaskOutput with block=false to see current progress. If {stage1_name} is still running and under {time_threshold} min, schedule another wakeup in {short_interval}s. If {stage1_name} is over {time_threshold} min or {stage2_name} started, schedule {long_interval}s wakeup. If the full pipeline finished or failed, read {output_path} for full details, summarize, and push a notification to the user.
```

---

### インスタンス 2: 合成結果の品質評価

> 元プロンプト: *Check if synthesis is done ({output_path} exists and has content), then evaluate quality. If synthesis is still running *

**変数の値**
  - `task_id`: {task_id}
  - `task_description`: {task_description}
  - `stage1_name`: {stage1_name}
  - `stage2_name`: {stage2_name}
  - `time_threshold`: {time_threshold}
  - `short_interval`: {short_interval}
  - `long_interval`: {long_interval}
  - `output_path`: {output_path}
  - `number_of_items`: {number_of_items}
  - `prompt_name`: {prompt_name}

**実際のプロンプト**
```
Check if synthesis is done ({output_path} exists and has content), then evaluate quality. If synthesis is still running wait more. Once done: 1) read the output and assess quality, 2) decide whether to re-run batch extraction for all {number_of_items} items with improved {prompt_name} prompt, 3) if re-extraction needed, run it in background.
```

---

### インスタンス 3: リジェンモードパイプライン監視

> 元プロンプト: *Check the status of background task {task_id} ({task_description}). Use TaskOutput with block=false. {stage1_name} shoul*

**変数の値**
  - `task_id`: {task_id}
  - `task_description`: {task_description}
  - `stage1_name`: {stage1_name}
  - `stage2_name`: {stage2_name}
  - `time_threshold`: {time_threshold}
  - `short_interval`: {short_interval}
  - `long_interval`: {long_interval}
  - `output_path`: {output_path}
  - `directory_name`: {directory_name}
  - `stage1_regen_marker`: {stage1_regen_marker}
  - `stage2_marker`: {stage2_marker}

**実際のプロンプト**
```
Check the status of background task {task_id} ({task_description}). Use TaskOutput with block=false. {stage1_name} should be skipped immediately (transcript exists in {directory_name} dir). Watch for {stage1_regen_marker} lines and {stage2_marker} lines. If {stage2_name} is running, report and schedule {long_interval}s wakeup. If {stage1_name} started running instead of being skipped, that means the fix didn't work — report it. If pipeline finished or failed, read {output_path} for full details, summarize, and push notification to user.
```
