---
name: MCP導入・テスト依頼
skill_id: e421b111-c176-4d94-a68e-48a79fed514c
version: 1.0.0
category: MCP導入・テスト依頼
status: public
source_count: 3
unique_user_count: 3
variables:
- mcp_name
- mcp_path
- branch_or_pr
triggers:
- MCPを導入してテストして
- このMCPを動かしてみて
- MCPの設定を確認して
- MCPの動作検証をお願い
- 新しいMCPを試したい
---

# MCP導入・テスト依頼

**説明**: MCPサーバーの導入設定と動作テストを依頼するスキル
**ステータス**: ✅ 公開中 | **ソース数**: 3 件 | **ユニークユーザー**: 3 人 | **カテゴリ**: MCP導入・テスト依頼

---

## テンプレートプロンプト

```
以下のMCPサーバーを導入・テストしたいです。

導入対象MCP: {mcp_name}
リポジトリ/パス: {mcp_path}
関連ブランチ/PR: {branch_or_pr}

まずは変更内容を確認し、MCPの起動方法を調べて、グラフワークフローから起動できるか設定を確認してください。その後、適当なクエリで動作検証をお願いします。
```

## 変数一覧

- `{{mcp_name}}`: 導入するMCPサーバーの名前（例: local-search-mcp）
- `{{mcp_path}}`: MCPサーバーのローカルパスまたはリポジトリURL（例: /Users/yourname/source/your-repo）
- `{{branch_or_pr}}`: 関連するブランチ名やPRのURL（例: https://github.com/your-org/your-repo/pull/32）

## 活用シーン

- 新しいMCPサーバーを導入して動作確認したいとき
- 既存のワークフローにMCPを組み込んでテストしたいとき
- 複数のMCPサーバーを同時にセットアップしてほしいとき

## トリガーフレーズ

- `MCPを導入してテストして`
- `このMCPを動かしてみて`
- `MCPの設定を確認して`
- `MCPの動作検証をお願い`
- `新しいMCPを試したい`

---

## 具体インスタンス

### インスタンス 1: local-search導入テスト

> 元プロンプト: *今回このブランチでは、local-searchというmcpを使用するための変更を行いました　これを実際に使用してワークフローを動かしてみて、動作をテストしたいです*

**変数の値**
  - `mcp_name`: local-search-mcp
  - `mcp_path`: /Users/{ユーザー名}/source/personal/localsearch-mcp
  - `branch_or_pr`: https://github.com/{組織名}/{リポジトリ名}/pull/32

**実際のプロンプト**
```
以下のMCPサーバーを導入・テストしたいです。

導入対象MCP: local-search-mcp
リポジトリ/パス: /Users/{ユーザー名}/source/personal/localsearch-mcp
関連ブランチ/PR: https://github.com/{組織名}/{リポジトリ名}/pull/32

まずは変更内容を確認し、MCPの起動方法を調べて、グラフワークフローから起動できるか設定を確認してください。その後、適当なクエリで動作検証をお願いします。
```

---

### インスタンス 2: 複数MCP一括導入

> 元プロンプト: *とりあえず　cctraceとlocalsearch-mcpの2つはページつくってみて*

**変数の値**
  - `mcp_name`: cctraceとlocalsearch-mcp
  - `mcp_path`: （未指定）
  - `branch_or_pr`: （未指定）

**実際のプロンプト**
```
以下のMCPサーバーを導入・テストしたいです。

導入対象MCP: cctraceとlocalsearch-mcp
リポジトリ/パス: （未指定）
関連ブランチ/PR: （未指定）

まずは変更内容を確認し、MCPの起動方法を調べて、グラフワークフローから起動できるか設定を確認してください。その後、適当なクエリで動作検証をお願いします。
```
