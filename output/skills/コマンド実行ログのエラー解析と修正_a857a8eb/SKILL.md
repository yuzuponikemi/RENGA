---
name: コマンド実行ログのエラー解析と修正
skill_id: a857a8eb-a2c1-4734-a0ce-14b49e438c47
version: 1.0.0
category: コマンド実行ログ
status: pending
source_count: 4
unique_user_count: 2
variables:
- command
- execution_log
- error_message
- additional_instructions
triggers:
- このエラーを解析して
- ビルドエラーの原因を教えて
- コマンド実行ログを見て
- エラーログを分析して
- 修正方法を提案して
---

# コマンド実行ログのエラー解析と修正

**説明**: コマンド実行ログからエラーを特定し、修正方法を提案する
**ステータス**: 🔒 審査中 | **ソース数**: 4 件 | **ユニークユーザー**: 2 人 | **カテゴリ**: コマンド実行ログ

---

## テンプレートプロンプト

```
以下のコマンド実行ログを分析し、エラーの原因と修正方法を特定してください。

コマンド: {command}

実行ログ:
{execution_log}

エラー内容:
{error_message}

修正手順:
1. エラーの原因を特定
2. 修正方法を提案
3. 修正後の確認手順を提示

追加の指示: {additional_instructions}
```

## 変数一覧

- `{{command}}`: 実行したコマンド（例: ビルドコマンド、ログインコマンドなど）
- `{{execution_log}}`: コマンド実行時の完全なログ出力
- `{{error_message}}`: エラーメッセージの要約（例: カテゴリが許可リストにない、特定のマーカーが見つからない）
- `{{additional_instructions}}`: 追加の指示や質問（例: 修正後の確認手順やコミット・プッシュの流れをメモリに登録する指示）

## 活用シーン

- CI/CDパイプラインのビルドエラー解析
- デプロイスクリプトのエラー修正
- ローカル開発環境でのビルドエラー対応

## トリガーフレーズ

- `このエラーを解析して`
- `ビルドエラーの原因を教えて`
- `コマンド実行ログを見て`
- `エラーログを分析して`
- `修正方法を提案して`

---

## 具体インスタンス

### インスタンス 1: MkDocsビルドエラー解析

> 元プロンプト: *Run uv run mkdocs build --strict   │  ⚠  Warning from the Material for MkDocs team  │  │  MkDocs 2.0, the underlying fra*

**変数の値**
  - `command`: uv run mkdocs build --strict
  - `execution_log`: INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: {ビルド出力先パス}
ERROR   -  Error reading categories of post '{ブログ記事パス}' in 'docs': category '{カテゴリ名}' not in allow list

Aborted with a BuildError!
Error: Process completed with exit code 1.
  - `error_message`: category '{カテゴリ名}' not in allow list
  - `additional_instructions`: 修正したらコミットして、ローカルでビルド完了できるか確認してから、Pushするような流れをメモリに登録しておいてください

**実際のプロンプト**
```
以下のコマンド実行ログを分析し、エラーの原因と修正方法を特定してください。

コマンド: {command}

実行ログ:
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: {ビルド出力先パス}
ERROR   -  Error reading categories of post '{ブログ記事パス}' in 'docs': category '{カテゴリ名}' not in allow list

Aborted with a BuildError!
Error: Process completed with exit code 1.

エラー内容: category '{カテゴリ名}' not in allow list

修正手順:
1. エラーの原因を特定
2. 修正方法を提案
3. 修正後の確認手順を提示

追加の指示: 修正したらコミットして、ローカルでビルド完了できるか確認してから、Pushするような流れをメモリに登録しておいてください
```

---

### インスタンス 2: MkDocsビルド成功確認

> 元プロンプト: *Run uv run mkdocs build --strict   │  ⚠  Warning from the Material for MkDocs team  │  │  MkDocs 2.0, the underlying fra*

**変数の値**
  - `command`: uv run mkdocs build --strict
  - `execution_log`: INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: {ビルド出力先パス}
INFO    -  Doc file '{ドキュメントファイル名}' contains an absolute link '{リンク先パス}', it was left as is.
（多数のINFOメッセージ）
ERROR   -  Error reading page '{ブログ記事パス}':
ERROR   -  Couldn't find '{マーカー文字列}' in post '{ブログ記事パス}' in 'docs'

Aborted with a BuildError!
  - `error_message`: Couldn't find '{マーカー文字列}' in post
  - `additional_instructions`: 修正したらコミットして、ローカルでビルド完了できるか確認してから、Pushするような流れをメモリに登録しておいてください

**実際のプロンプト**
```
以下のコマンド実行ログを分析し、エラーの原因と修正方法を特定してください。

コマンド: {command}

実行ログ:
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: {ビルド出力先パス}
INFO    -  Doc file '{ドキュメントファイル名}' contains an absolute link '{リンク先パス}', it was left as is.
（多数のINFOメッセージ）
ERROR   -  Error reading page '{ブログ記事パス}':
ERROR   -  Couldn't find '{マーカー文字列}' in post '{ブログ記事パス}' in 'docs'

Aborted with a BuildError!

エラー内容: Couldn't find '{マーカー文字列}' in post

修正手順:
1. エラーの原因を特定
2. 修正方法を提案
3. 修正後の確認手順を提示

追加の指示: 修正したらコミットして、ローカルでビルド完了できるか確認してから、Pushするような流れをメモリに登録しておいてください
```

---

### インスタンス 3: Azureログイン成功確認

> 元プロンプト: *ikmx@Yusukis-MacBook-Pro RENGA %   ! /opt/homebrew/bin/az login A web browser has been opened at https://login.microsoft*

**変数の値**
  - `command`: /opt/homebrew/bin/az login
  - `execution_log`: A web browser has been opened at {認証URL}. Please continue the login in the web browser. If no web browser is available or if the web browser fails to open, use device code flow with `az login --use-device-code`.

Retrieving tenants and subscriptions for the selection...

[Tenant and subscription selection]

No     Subscription name     Subscription ID                       Tenant
-----  --------------------  ------------------------------------  -----------------
[1] *  {サブスクリプション名}  {サブスクリプションID}  {テナント名}

The default is marked with an *; the default tenant is '{テナント名}' and subscription is '{サブスクリプション名}' ({サブスクリプションID}).

Select a subscription and tenant (Type a number or Enter for no changes): 

Tenant: {テナント名}
Subscription: {サブスクリプション名} ({サブスクリプションID})
  - `error_message`: エラーなし（正常終了）
  - `additional_instructions`: なし

**実際のプロンプト**
```
以下のコマンド実行ログを分析し、エラーの原因と修正方法を特定してください。

コマンド: {command}

実行ログ:
A web browser has been opened at {認証URL}. Please continue the login in the web browser. If no web browser is available or if the web browser fails to open, use device code flow with `az login --use-device-code`.

Retrieving tenants and subscriptions for the selection...

[Tenant and subscription selection]

No     Subscription name     Subscription ID                       Tenant
-----  --------------------  ------------------------------------  -----------------
[1] *  {サブスクリプション名}  {サブスクリプションID}  {テナント名}

The default is marked with an *; the default tenant is '{テナント名}' and subscription is '{サブスクリプション名}' ({サブスクリプションID}).

Select a subscription and tenant (Type a number or Enter for no changes): 

Tenant: {テナント名}
Subscription: {サブスクリプション名} ({サブスクリプションID})

エラー内容: エラーなし（正常終了）

修正手順:
1. エラーの原因を特定
2. 修正方法を提案
3. 修正後の確認手順を提示

追加の指示: なし
```
