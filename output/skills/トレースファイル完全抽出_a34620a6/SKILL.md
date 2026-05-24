---
name: トレースファイル完全抽出
skill_id: a34620a6-e78b-4033-832b-f368a58a6bc9
version: 1.0.0
category: トレースファイル完全抽出
status: public
source_count: 20
unique_user_count: 12
variables:
- trace_directory
- trace_file_list
triggers:
- トレースファイルを全部読んで
- 開発日誌用に詳細を抽出して
- このプロジェクトの全セッションをまとめて
- 会話ログから技術的決定を抽出して
- 全トレースファイルの詳細レポートを作成して
---

# トレースファイル完全抽出

**説明**: AI会話ログから全詳細を抽出し開発日誌用に整理する
**ステータス**: ✅ 公開中 | **ソース数**: 20 件 | **ユニークユーザー**: 12 人 | **カテゴリ**: トレースファイル完全抽出

---

## テンプレートプロンプト

```
Read the following trace files COMPLETELY and extract every detail. I'm writing a detailed developer diary and need verbatim user messages, exact error messages, exact technical decisions, and the reasoning behind each choice.

Files to read fully (all in "{trace_directory}"):
{trace_file_list}

For each file, I need:
1. Exact user messages (copy them verbatim)
2. What the AI decided to do and why (from thinking blocks)
3. Exact error messages encountered
4. What was created/changed (filenames, what the code does)
5. What was rejected or abandoned and why
6. Key architectural decisions made
7. Any interesting technical insights from the AI thinking blocks
8. Quantitative results (concept counts, file sizes, processing times etc.)

Be as detailed as possible. Include file names, function names, command outputs where significant.
```

## 変数一覧

- `{{trace_directory}}`: トレースファイルが保存されているディレクトリの絶対パス
- `{{trace_file_list}}`: 読み込むファイルの一覧（各行「- ファイル名.md」形式で列挙）

## 活用シーン

- 複数セッションにわたるAI開発ログを一気通貫で読み解き開発日誌を書く
- プロジェクトの技術的転換点や失敗原因をトレースから特定する
- 長期プロジェクトの意思決定履歴をチームメンバーに共有する

## トリガーフレーズ

- `トレースファイルを全部読んで`
- `開発日誌用に詳細を抽出して`
- `このプロジェクトの全セッションをまとめて`
- `会話ログから技術的決定を抽出して`
- `全トレースファイルの詳細レポートを作成して`

---

## 具体インスタンス

### インスタンス 1: researchプロジェクト前半

> 元プロンプト: *Read the following trace files COMPLETELY and extract every detail. I'm writing a detailed developer diary and need verb*

**変数の値**
  - `trace_directory`: {trace_directory}
  - `trace_file_list`: - {ファイル名1}
- {ファイル名2}
- {ファイル名3}
- {ファイル名4}
- {ファイル名5}
- {ファイル名6}
- {ファイル名7}
- {ファイル名8}

**実際のプロンプト**
```
Read the following trace files COMPLETELY and extract every detail. I'm writing a detailed developer diary and need verbatim user messages, exact error messages, exact technical decisions, and the reasoning behind each choice.

Files to read fully (all in "{trace_directory}"):
{trace_file_list}

For each file, I need:
1. Exact user messages (copy them verbatim)
2. What the AI decided to do and why (from thinking blocks)
3. Exact error messages encountered
4. What was created/changed (filenames, what the code does)
5. What was rejected or abandoned and why
6. Key architectural decisions made
7. Any interesting technical insights from the AI thinking blocks

Be as detailed as possible. Include file names, function names, command outputs where significant.
```

---

### インスタンス 2: researchプロジェクト後半

> 元プロンプト: *Read the following trace files COMPLETELY and extract every detail. I'm writing a detailed developer diary and need verb*

**変数の値**
  - `trace_directory`: {trace_directory}
  - `trace_file_list`: - {ファイル名9}
- {ファイル名10}
- {ファイル名11}
- {ファイル名12}
- {ファイル名13}
- {ファイル名14}
- {ファイル名15}
- {ファイル名16}
- {ファイル名17}

**実際のプロンプト**
```
Read the following trace files COMPLETELY and extract every detail. I'm writing a detailed developer diary and need verbatim user messages, exact error messages, exact technical decisions, and the reasoning behind each choice.

Files to read fully (all in "{trace_directory}"):
{trace_file_list}

For each file, I need:
1. Exact user messages (copy them verbatim)
2. What the AI decided to do and why (from thinking blocks)
3. Exact error messages encountered
4. What was created/changed (filenames, what the code does)
5. What was rejected or abandoned and why
6. Key architectural decisions made
7. Any interesting technical insights from the AI thinking blocks
8. Quantitative results (concept counts, file sizes, processing times etc.)

Be as detailed as possible. Include file names, function names, command outputs where significant.
```

---

### インスタンス 3: 全17セッション一括抽出

> 元プロンプト: *Read ALL of the following files completely and summarize their contents in detail. I need to understand the full develop*

**変数の値**
  - `trace_directory`: {trace_directory}
  - `trace_file_list`: - {ファイル名1}
- {ファイル名2}
- {ファイル名3}
- {ファイル名4}
- {ファイル名5}
- {ファイル名6}
- {ファイル名7}
- {ファイル名8}
- {ファイル名9}
- {ファイル名10}
- {ファイル名11}
- {ファイル名12}
- {ファイル名13}
- {ファイル名14}
- {ファイル名15}
- {ファイル名16}
- {ファイル名17}

**実際のプロンプト**
```
Read ALL of the following files completely and summarize their contents in detail. I need to understand the full development story of a project called "{プロジェクト名}" across {セッション数} sessions from {開始日} to {終了日}.

For each file, extract:
1. The date and session ID
2. ALL user messages (verbatim or close paraphrase)
3. Key decisions/changes made by the AI
4. Technical turning points, dead ends, pivots

Files to read (all in "{trace_directory}"):
{trace_file_list}

Please read every single file fully and give me a detailed chronological narrative of what happened across all sessions. Be thorough - this will be used to write a detailed development diary article.
```
