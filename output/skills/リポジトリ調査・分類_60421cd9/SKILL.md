---
name: リポジトリ調査・分類
skill_id: 60421cd9-bb2c-4cd5-bf20-04844e5c6e71
version: 1.0.0
category: リポジトリ調査・分類
status: public
source_count: 3
unique_user_count: 3
variables:
- workspace_path
- config_file_list
- repo_list
triggers:
- リポジトリを分類して
- プロジェクトを調査して
- フォルダ内のリポジトリを一覧して
- コードベースを棚卸しして
- リポジトリの状態を教えて
---

# リポジトリ調査・分類

**説明**: 複数リポジトリの内容を読み取り、分類・レポートするスキル
**ステータス**: ✅ 公開中 | **ソース数**: 3 件 | **ユニークユーザー**: 3 人 | **カテゴリ**: リポジトリ調査・分類

---

## テンプレートプロンプト

```
The workspace at {workspace_path} contains many GitHub repositories. I need to classify each one. For every subdirectory, read:
1. README.md (or readme.md, README)
2. CLAUDE.md if it exists
3. {config_file_list} (just the name/description fields) if no README

Repos to check (all subdirs of {workspace_path}):
{repo_list}

For each repo, provide:
- Name
- One-line description (what it does)
- Tech stack (main language/framework)
- Apparent status (active/experiment/archived/template)
- Category guess (e.g., AI/ML tool, game, web app, agent framework, MCP server, data pipeline, etc.)

Be thorough but concise per repo. Read actual file contents, don't guess.
```

## 変数一覧

- `{{workspace_path}}`: 調査対象のリポジトリが格納されている親ディレクトリの絶対パス
- `{{config_file_list}}`: プロジェクト設定ファイルの候補リスト（例: package.json / pyproject.toml / go.mod）
- `{{repo_list}}`: 調査・分類するリポジトリ名のカンマ区切りリスト

## 活用シーン

- 個人のGitHubリポジトリ群を棚卸しして、プロジェクトの種類や状態を把握したい
- チーム内の複数プロジェクトを一括で調査し、技術スタックやメンテナンス状況をレポートする
- 新しく参加した組織のリポジトリを素早く理解するための初期調査

## トリガーフレーズ

- `リポジトリを分類して`
- `プロジェクトを調査して`
- `フォルダ内のリポジトリを一覧して`
- `コードベースを棚卸しして`
- `リポジトリの状態を教えて`

---

## 具体インスタンス

### インスタンス 1: 個人リポジトリ分類

> 元プロンプト: *The workspace at {workspace_path} contains many GitHub repositories. I need to classify each one. For every subdirectory*

**変数の値**
  - `workspace_path`: /Users/{username}/source/personal
  - `config_file_list`: package.json / pyproject.toml / go.mod
  - `repo_list`: {repo_list_placeholder}

**実際のプロンプト**
```
The workspace at {workspace_path} contains many GitHub repositories. I need to classify each one. For every subdirectory, read:
1. README.md (or readme.md, README)
2. CLAUDE.md if it exists
3. {config_file_list} (just the name/description fields) if no README

Repos to check (all subdirs of {workspace_path}):
{repo_list}

For each repo, provide:
- Name
- One-line description (what it does)
- Tech stack (main language/framework)
- Apparent status (active/experiment/archived/template)
- Category guess (e.g., AI/ML tool, game, web app, agent framework, MCP server, data pipeline, etc.)

Be thorough but concise per repo. Read actual file contents, don't guess.
```

---

### インスタンス 2: 特定リポジトリ詳細調査

> 元プロンプト: *Explore the repository at {workspace_path}/{repo_name} and give me a concise report covering: 1. What search sources are*

**変数の値**
  - `workspace_path`: /Users/{username}/source/personal
  - `config_file_list`: package.json / pyproject.toml / go.mod
  - `repo_list`: {repo_name}

**実際のプロンプト**
```
Explore the repository at {workspace_path}/{repo_name} and give me a concise report covering:
1. What search sources are implemented (Wikipedia, local files, etc.)
2. The MCP tool interface — what tools are exposed, their parameters and return format
3. Any Wikipedia-specific search capability: how it queries Wikipedia, what fields are returned (title, summary, URL, ID, etc.)
4. Whether there's any entity linking or canonical name resolution
5. The overall architecture (how the MCP server is structured)

Be thorough but concise. Focus on what's actually implemented, not what could be done.
```

---

### インスタンス 3: セットアップ手順調査

> 元プロンプト: *Explore the {repo_name} project at {workspace_path}/{repo_name} thoroughly. I need to understand:  1. How to start the M*

**変数の値**
  - `workspace_path`: /Users/{username}/source/personal
  - `config_file_list`: package.json / pyproject.toml / go.mod
  - `repo_list`: {repo_name}

**実際のプロンプト**
```
Explore the {repo_name} project at {workspace_path}/{repo_name} thoroughly. I need to understand:

1. How to start the MCP server (README, pyproject.toml, main entry point)
2. What the server.py file looks like (src/server.py or wherever it is)
3. What tools are available (search_wikipedia, etc.)
4. What data/indexes it needs - does it need Wikipedia data downloaded first?
5. Any setup/initialization steps required before first use
6. How to verify the server is working
7. Check if there's any data directory, index files, or downloaded Wikipedia content already present

Be very thorough - check README.md, pyproject.toml, src/ directory, any data/ or indexes/ directories, any scripts/ for setup.
```
