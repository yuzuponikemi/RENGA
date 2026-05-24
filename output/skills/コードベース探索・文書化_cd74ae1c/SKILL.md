---
name: コードベース探索・文書化
skill_id: cd74ae1c-587e-4c10-916b-f61b47265708
version: 1.0.0
category: コードベース探索・文書化
status: public
source_count: 6
unique_user_count: 5
variables:
- project_path
- language
- language_ext
- source_dir
- config_dir
- entry_file
- dependency_file
- design_pattern_examples
triggers:
- プロジェクトのコードを全部調べて
- コードベースを探索して文書化して
- アーキテクチャを調査して
- プロジェクトの全体像を教えて
- コードの構造を分析して
---

# コードベース探索・文書化

**説明**: プロジェクトのコードベースを徹底調査し、構造・フローを文書化する
**ステータス**: ✅ 公開中 | **ソース数**: 6 件 | **ユニークユーザー**: 5 人 | **カテゴリ**: コードベース探索・文書化

---

## テンプレートプロンプト

```
Thoroughly explore the {project_path} codebase. I need to document this project comprehensively in {language}.

Please gather:
1. All {language_ext} source files and their purposes (under {source_dir}/)
2. All config files ({config_dir}/ directory)
3. The full pipeline flow in {entry_file} — every stage, what it does, what it outputs
4. All CLI arguments and their descriptions
5. All external dependencies ({dependency_file})
6. The data flow: what each stage receives as input, produces as output, and saves to disk
7. Key design patterns used (e.g., {design_pattern_examples})

Be very thorough — read the key files to understand their internal structure. I need enough detail to write architecture documentation.
```

## 変数一覧

- `{{project_path}}`: 調査対象のプロジェクトの絶対パス
- `{{language}}`: 文書化に使用する言語（例: Japanese, English）
- `{{language_ext}}`: ソースコードの拡張子（例: Python → .py）
- `{{source_dir}}`: ソースコードが格納されているディレクトリ名（例: src）
- `{{config_dir}}`: 設定ファイルが格納されているディレクトリ名（例: config）
- `{{entry_file}}`: パイプラインのエントリーポイントファイル名（例: main.py）
- `{{dependency_file}}`: 依存関係が記載されたファイル名（例: requirements.txt）
- `{{design_pattern_examples}}`: 注目すべきデザインパターンの例（例: state dict accumulation, thinking_log）

## 活用シーン

- 新規参画メンバー向けにプロジェクト全体のアーキテクチャ文書を作成する
- リファクタリング前にコードベース全体の依存関係とデータフローを把握する
- 既存プロジェクトの技術的負債を評価するための基礎資料を作成する

## トリガーフレーズ

- `プロジェクトのコードを全部調べて`
- `コードベースを探索して文書化して`
- `アーキテクチャを調査して`
- `プロジェクトの全体像を教えて`
- `コードの構造を分析して`

---

## 具体インスタンス

### インスタンス 1: book-research完全調査

> 元プロンプト: *Thoroughly explore the Project Cogito codebase at {project_path}. I need to document this project comprehensively in Jap*

**変数の値**
  - `project_path`: {project_path}
  - `language`: Japanese
  - `language_ext`: Python
  - `source_dir`: src
  - `config_dir`: config
  - `entry_file`: main.py
  - `dependency_file`: requirements.txt
  - `design_pattern_examples`: state dict accumulation, thinking_log

**実際のプロンプト**
```
Thoroughly explore the {project_path} codebase. I need to document this project comprehensively in Japanese.

Please gather:
1. All Python source files and their purposes (under src/)
2. All config files (config/ directory)
3. The full pipeline flow in main.py — every stage, what it does, what it outputs
4. All CLI arguments and their descriptions
5. All external dependencies (requirements.txt)
6. The data flow: what each stage receives as input, produces as output, and saves to disk
7. Key design patterns used (e.g., state dict accumulation, thinking_log)

Be very thorough — read the key files to understand their internal structure. I need enough detail to write architecture documentation.
```

---

### インスタンス 2: LLM呼び出し箇所調査

> 元プロンプト: *Thoroughly explore the {project_path} project. I need:  1. List ALL files in the docs/ folder and read each one complete*

**変数の値**
  - `project_path`: {project_path}
  - `language`: English
  - `language_ext`: Python
  - `source_dir`: src
  - `config_dir`: config
  - `entry_file`: main.py
  - `dependency_file`: requirements.txt
  - `design_pattern_examples`: ChatOllama, .invoke(, .ainvoke(, .stream(, llm(, llm., model., ChatOpenAI, requests.post (for VOICEVOX), tavily, ddgs

**実際のプロンプト**
```
Thoroughly explore the {project_path} project. I need:

1. List ALL files in the docs/ folder and read each one completely
2. List ALL Python source files in src/ recursively
3. Read main.py completely
4. Read all config files in config/
5. For every Python file in src/, search for LLM call patterns: ChatOllama, .invoke(, .ainvoke(, .stream(, llm(, llm., model., ChatOpenAI, requests.post (for VOICEVOX), tavily, ddgs
6. Identify all prompt templates and system prompts used in LLM calls

Return a comprehensive report with:
- Complete list of existing docs and a summary of each
- Complete file tree of the project (src/, config/, docs/)
- Every LLM call location with file path, line number, model used, input/output format
- Every prompt template location
- Every external API call (VOICEVOX, Tavily, DuckDuckGo)
- The flow of data between pipeline stages (what each stage reads and writes)
- Configuration files and their structure
```

---

### インスタンス 3: ドキュメント更新調査

> 元プロンプト: *Find all documentation files (README, .md files in root or docs/) in {project_path} that describe the project's CLI usag*

**変数の値**
  - `project_path`: {project_path}
  - `language`: English
  - `language_ext`: Python
  - `source_dir`: src
  - `config_dir`: config
  - `entry_file`: main.py
  - `dependency_file`: requirements.txt
  - `design_pattern_examples`: CLI usage, pipeline, setup

**実際のプロンプト**
```
Find all documentation files (README, .md files in root or docs/) in {project_path} that describe the project's CLI usage, pipeline, or setup. I need to know which files to update for a new --trace flag feature. Quick search.
```
