---
name: コードベース探索
skill_id: a4d27e8a-c481-46e2-8230-42d9d2dd4670
version: 1.0.0
category: コードベース探索
status: public
source_count: 10
unique_user_count: 8
variables:
- project_path
- language
- focus_area
- config_files
- framework
- technology
triggers:
- コードベースを探索して
- プロジェクト構造を教えて
- リポジトリの全体像を把握したい
- このプロジェクトを調査して
- コードの構成を理解したい
---

# コードベース探索

**説明**: プロジェクト構造を徹底調査し全体像を把握する
**ステータス**: ✅ 公開中 | **ソース数**: 10 件 | **ユニークユーザー**: 8 人 | **カテゴリ**: コードベース探索

---

## テンプレートプロンプト

```
Explore the codebase at {project_path} thoroughly. I need to understand:
1. The overall project structure (all files and directories)
2. Any existing {language} code, especially {focus_area}-related code
3. Any configuration files ({config_files})
4. Any existing documentation or MD files
5. Any {framework} or {technology}-related code

Give me a complete picture of what exists in this repo.
```

## 変数一覧

- `{{project_path}}`: 調査対象のプロジェクトの絶対パスまたは相対パス
- `{{language}}`: プロジェクトで使われているプログラミング言語（例: Python, TypeScript, Go）
- `{{focus_area}}`: 特に注目したい領域（例: agent, CLI, data processing）
- `{{config_files}}`: 確認すべき設定ファイルのカンマ区切りリスト（例: pyproject.toml, requirements.txt, package.json）
- `{{framework}}`: 使用されているフレームワーク名（例: LangGraph, LangChain, React, Django）
- `{{technology}}`: 関連技術名（例: AI, browser automation, cron）

## 活用シーン

- 新規メンバーがプロジェクトに参加した際のコードベース理解
- リファクタリング前の現状把握と依存関係の洗い出し
- 新機能追加前に既存のパターンや規約を確認するため

## トリガーフレーズ

- `コードベースを探索して`
- `プロジェクト構造を教えて`
- `リポジトリの全体像を把握したい`
- `このプロジェクトを調査して`
- `コードの構成を理解したい`

---

## 具体インスタンス

### インスタンス 1: Multiagents探索

> 元プロンプト: *Explore the codebase at {project_path} thoroughly. I need to understand: 1. The overall project structure (all files and*

**変数の値**
  - `project_path`: {project_path}
  - `language`: Python
  - `focus_area`: agent
  - `config_files`: pyproject.toml, requirements.txt, etc.
  - `framework`: LangGraph, LangChain
  - `technology`: AI

**実際のプロンプト**
```
Explore the codebase at {project_path} thoroughly. I need to understand:
1. The overall project structure (all files and directories)
2. Any existing Python code, especially agent-related code
3. Any configuration files (pyproject.toml, requirements.txt, etc.)
4. Any existing documentation or MD files
5. Any LangGraph, LangChain, or AI-related code

Give me a complete picture of what exists in this repo.
```

---

### インスタンス 2: cc-trace詳細調査

> 元プロンプト: *Explore the {project_path} codebase thoroughly. I need to understand: 1. The overall project structure (languages, frame*

**変数の値**
  - `project_path`: {project_path}
  - `language`: Python
  - `focus_area`: sync/cron
  - `config_files`: pyproject.toml, requirements, etc.
  - `framework`: CLI
  - `technology`: browser automation, web scraping

**実際のプロンプト**
```
Explore the {project_path} codebase thoroughly. I need to understand:
1. The overall project structure (languages, frameworks, build tools)
2. How the existing sync/cron functionality works
3. What data sources are currently supported (Claude, Gemini, etc.)
4. How conversations are stored/exported (file format, directory structure)
5. Any existing browser automation or web scraping code
6. The CLI entry points and command structure
7. Dependencies (pyproject.toml, requirements, etc.)

Be very thorough - check all source files, config files, and test files.
```

---

### インスタンス 3: Claudeディレクトリ調査

> 元プロンプト: *Explore the {project_path} directory to understand its structure. I need to know: 1. What files and subdirectories exist*

**変数の値**
  - `project_path`: {project_path}
  - `language`: JSON
  - `focus_area`: session log
  - `config_files`: N/A
  - `framework`: N/A
  - `technology`: JSONL, schema analysis

**実際のプロンプト**
```
Explore the {project_path} directory to understand its structure. I need to know:
1. What files and subdirectories exist in {project_path}/
2. Where session logs (JSON files) are stored
3. The structure of a recent session log file - what keys exist, how messages are structured, what tool_use blocks look like, etc.

Use `ls -la {project_path}/` and recursively explore subdirectories. Find JSON log files and read a sample to understand the schema. Focus on understanding the message format, content blocks, tool_use blocks, and any metadata (tokens, model, timestamps).

Be thorough - check for projects/, sessions/, logs/ or similar subdirectories. The logs might be in JSONL format (one JSON object per line) rather than a single JSON array.
```
