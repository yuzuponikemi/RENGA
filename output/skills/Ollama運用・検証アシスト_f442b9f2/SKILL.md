---
name: Ollama運用・検証アシスト
skill_id: f442b9f2-8422-4a27-8490-91a30e971356
version: 1.0.0
category: 技術選定・実装検討
status: public
source_count: 16
unique_user_count: 9
variables:
- ollama_action
- model_name
- environment
- additional_requirements
- notes
triggers:
- ollamaでベンチマークして
- ollamaのログ診断して
- モデルをプルして
- ollamaの設定確認して
- ollama再起動して
---

# Ollama運用・検証アシスト

**説明**: Ollamaのモデル管理、ベンチマーク、ログ診断、設定確認を支援する
**ステータス**: ✅ 公開中 | **ソース数**: 16 件 | **ユニークユーザー**: 9 人 | **カテゴリ**: 技術選定・実装検討

---

## テンプレートプロンプト

```
以下のOllama関連タスクを実行してください。
- {ollama_action}（例: モデルプル、ベンチマーク実行、ログ診断）
- 対象モデル: {model_name}（例: gemma4:31b-coding-mtp-bf16）
- 使用環境: {environment}（例: macOS, MLX）
- 追加要件: {additional_requirements}（例: コンテキスト設定確認、OllamaProx経由確認）
- 注意点: {notes}（例: 他のジョブが実行中なら待つ、再起動が必要なら実行）
```

## 変数一覧

- `{{ollama_action}}`: 実行してほしい具体的なアクション（例: モデルをプルする、ベンチマークコードを書く、ログを診断する）
- `{{model_name}}`: 対象のOllamaモデル名（例: gemma4:31b-coding-mtp-bf16, llama3）
- `{{environment}}`: 実行環境の詳細（例: macOS, MLX, Linux）
- `{{additional_requirements}}`: 追加の要件や確認事項（例: コンテキスト設定が正しいか確認、OllamaProx経由かトレース）
- `{{notes}}`: 注意点や制約（例: 他のジョブが実行中なら待つ、再起動が必要なら実行）

## 活用シーン

- Ollamaモデルのベンチマークを実行し、性能レポートを生成する
- Ollamaのログを診断して回答が得られない原因を特定する
- OllamaProxの設定確認や再起動を依頼する

## トリガーフレーズ

- `ollamaでベンチマークして`
- `ollamaのログ診断して`
- `モデルをプルして`
- `ollamaの設定確認して`
- `ollama再起動して`

---

## 具体インスタンス

### インスタンス 1: モデルプル依頼

> 元プロンプト: *ollama run {model_name} これつかうと{environment}では速くなるらしいので、プルしておいてもらえますか*

**変数の値**
  - `ollama_action`: モデルをプルする（ollama run {model_name}）
  - `model_name`: {model_name}
  - `environment`: {environment}（MLX対応で高速化）
  - `additional_requirements`: なし
  - `notes`: 他のcronジョブが実行中なら待つ、必要ならOllamaを再起動する

**実際のプロンプト**
```
以下のOllama関連タスクを実行してください。
- アクション: モデルをプルする（ollama run {model_name}）
- 対象モデル: {model_name}
- 使用環境: {environment}（MLX対応で高速化）
- 追加要件: なし
- 注意点: 他のcronジョブが実行中なら待つ、必要ならOllamaを再起動する
```

---

### インスタンス 2: ベンチマーク実行依頼

> 元プロンプト: *今ollamaでたくさんモデル持っているのですが、このPCでそれぞれどういう性能が出るのかを調べたいです ベンチマーク用のコードを書いて、結果をリポートしてくれますか*

**変数の値**
  - `ollama_action`: ベンチマークコードを書いて実行し、性能レポートを生成する
  - `model_name`: 現在PCにインストールされている全モデル
  - `environment`: 現在のPC環境
  - `additional_requirements`: 各モデルの性能（速度、応答品質など）をレポート形式で出力
  - `notes`: なし

**実際のプロンプト**
```
以下のOllama関連タスクを実行してください。
- アクション: ベンチマークコードを書いて実行し、性能レポートを生成する
- 対象モデル: 現在PCにインストールされている全モデル
- 使用環境: 現在のPC環境
- 追加要件: 各モデルの性能（速度、応答品質など）をレポート形式で出力
- 注意点: なし
```

---

### インスタンス 3: ログ診断依頼

> 元プロンプト: *ollamaモードで回答が得られなかったので、ちょっろログ見て診断してくれる？*

**変数の値**
  - `ollama_action`: ログを診断して回答が得られなかった原因を特定する
  - `model_name`: ollamaモードで使用中のモデル
  - `environment`: 現在の環境
  - `additional_requirements`: コンテキスト設定が正しいか確認し、問題があれば修正提案
  - `notes`: ログを確認してから診断結果を報告する

**実際のプロンプト**
```
以下のOllama関連タスクを実行してください。
- アクション: ログを診断して回答が得られなかった原因を特定する
- 対象モデル: ollamaモードで使用中のモデル
- 使用環境: 現在の環境
- 追加要件: コンテキスト設定が正しいか確認し、問題があれば修正提案
- 注意点: ログを確認してから診断結果を報告する
```
