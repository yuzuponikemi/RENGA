---
name: 実行ログ記録と分析
skill_id: 14dbc528-e715-42bb-8c34-a31ad309a856
version: 1.0.0
category: 実行ログの記録
status: public
source_count: 5
unique_user_count: 4
variables:
- システム名
- 実行ログ全文
- 注目すべきポイント
triggers:
- このログを分析して
- 実行結果を確認して
- エラーの原因を調べて
- ログを解析して問題点を教えて
- テスト結果をレビューして
---

# 実行ログ記録と分析

**説明**: 実行ログを記録し、問題点を分析・報告するスキル
**ステータス**: ✅ 公開中 | **ソース数**: 5 件 | **ユニークユーザー**: 4 人 | **カテゴリ**: 実行ログの記録

---

## テンプレートプロンプト

```
以下は{システム名}の実行ログです。

{実行ログ全文}

上記のログを分析し、以下の観点で報告してください：
1. 実行の概要（何を実行したか）
2. 発生した問題・エラー
3. 問題の原因
4. 推奨される修正方法

特に{注目すべきポイント}に注目して分析してください。

出力形式：
- 実行概要
- 問題点リスト
- 原因分析
- 修正提案
```

## 変数一覧

- `{{システム名}}`: 実行したシステムやツールの名前（例: 検索サーバー、CI/CDツール、テストフレームワーク）
- `{{実行ログ全文}}`: ターミナルやログファイルから取得した実行ログの全文
- `{{注目すべきポイント}}`: 特に分析してほしい観点（例: エラーメッセージ、パフォーマンス、データの整合性）

## 活用シーン

- 自動化パイプラインの実行ログ分析
- サーバー起動時のエラーログ解析
- テストスイートの失敗原因調査

## トリガーフレーズ

- `このログを分析して`
- `実行結果を確認して`
- `エラーの原因を調べて`
- `ログを解析して問題点を教えて`
- `テスト結果をレビューして`

---

## 具体インスタンス

### インスタンス 1: MCPサーバーログ分析

> 元プロンプト: *ユーザー端末のプロンプトからサーバー起動コマンドを実行 [日時] INFO     Anonymized telemetry       posthog.py:22                              enabled.*

**変数の値**
  - `システム名`: 検索サーバー
  - `実行ログ全文`: ユーザー端末のプロンプトからサーバー起動コマンドを実行
[日時] INFO     Anonymized telemetry       posthog.py:22
                             enabled. See                            
                             https://docs.trychroma.com              
                             /telemetry for more                     
                             information.                            
[日時] INFO     Load          SentenceTransformer.py:227
                             pretrained                              
                             SentenceTrans                           
                             former:                                 
                             モデル名                               
                             -v2                                     
Starting 検索サーバー...
Loading BM25 index from data/wiki_index.pkl...
BM25 index loaded. 1000000 documents available.
Loading vector index from data/chroma_db...
Vector index not found, will be built on next index build: Collection [wikipedia] does not exist
Server ready! このようにベクトルデータベースができていないっぽいです
  - `注目すべきポイント`: ベクトルデータベースの初期化状態

**実際のプロンプト**
```
以下は{システム名}の実行ログです。

{実行ログ全文}

上記のログを分析し、以下の観点で報告してください：
1. 実行の概要（何を実行したか）
2. 発生した問題・エラー
3. 問題の原因
4. 推奨される修正方法

特にベクトルデータベースの初期化状態に注目して分析してください。

出力形式：
- 実行概要
- 問題点リスト
- 原因分析
- 修正提案
```

---

### インスタンス 2: CI/CDテスト失敗分析

> 元プロンプト: *📋 This test suite is designed for CI/CD environments    It tests indexing and search functionality without requiring LLM*

**変数の値**
  - `システム名`: 検索サーバー
  - `実行ログ全文`: 📋 This test suite is designed for CI/CD environments
   It tests indexing and search functionality without requiring LLM
======================================================================
検索サーバー - CI/CD Test Suite
======================================================================
Test documents path: /home/runner/work/プロジェクト名/プロジェクト名/test_docs
Found 6 test documents
✅ PASS: MCP Connection
   Found 3 tools
❌ FAIL: Local Document Indexing
   Results too short or missing content
❌ FAIL: Search Results Quality
   Only 0/3 queries passed. Failed: ['Machine Learning topic', 'Database topic', 'Web Development topic']
❌ FAIL: Incremental Indexing
   Failed to detect changes: initial=True, modified=True, new=False
✅ PASS: Search Strategies
   Both keyword and hybrid strategies work
======================================================================
Test Summary
======================================================================
✅ MCP Connection
❌ Local Document Indexing
❌ Search Results Quality
❌ Incremental Indexing
✅ Search Strategies
Results: 2/5 tests passed
======================================================================
⚠️  3 test(s) failed これ治して
  - `注目すべきポイント`: テスト失敗の原因と修正方法

**実際のプロンプト**
```
以下は{システム名}の実行ログです。

{実行ログ全文}

上記のログを分析し、以下の観点で報告してください：
1. 実行の概要（何を実行したか）
2. 発生した問題・エラー
3. 問題の原因
4. 推奨される修正方法

特にテスト失敗の原因と修正方法に注目して分析してください。

出力形式：
- 実行概要
- 問題点リスト
- 原因分析
- 修正提案
```

---

### インスタンス 3: Ollama統合テスト分析

> 元プロンプト: *ユーザー端末のプロンプトから統合テストスクリプトを実行 ============================================================ 検索サーバー - 統合テスト ================*

**変数の値**
  - `システム名`: 検索サーバー
  - `実行ログ全文`: ユーザー端末のプロンプトから統合テストスクリプトを実行
============================================================
検索サーバー - 統合テスト
============================================================

ℹ️  This requires 外部サービス to be running with モデル名 model
   Use --simple flag to test MCP connection only

🤖 Starting MCP Client and connecting to 検索サーバー...
[日時] INFO     Anonymized telemetry       posthog.py:22
                             enabled. See                            
                             https://docs.trychroma.com              
                             /telemetry for more                     
                             information.                            
[日時] INFO     Load          SentenceTransformer.py:227
                             pretrained                              
                             SentenceTrans                           
                             former:                                 
                             モデル名                               
                             -v2                                     
Starting 検索サーバー...
Loading BM25 index from data/wiki_index.pkl...
BM25 index loaded. 1000000 documents available.
Loading vector index from data/chroma_db...
Vector index loaded. 1000000 documents in vector store.
Server ready!

[日時] INFO     Processing request of type ListToolsRequest           server.py:713
✅ Connected. Available tools: ['search_wikipedia']

👤 User Query: プログラミング言語の歴史について、簡潔に教えて

🔄 Calling 外部サービス...

🛠️  Agent requested 1 tool call(s)
   → Tool: search_wikipedia
   → Args: {'query': 'history of python programming', 'strategy': 'hybrid', 'top_k': '3'}
[日時] INFO     Processing request of type CallToolRequest            server.py:713
Batches: 100%|████████████████████████████████████████████████████| 1/1 [00:00<00:00, 62.04it/s]
   → Output length: 2417 chars
   → Output: [Result 1]
Title: VPython
...

🔄 Generating final answer...

🤖 Agent Answer:
Pythonは、1980年代後半にオランダのコーネル大学の大学院生だったGuido van Rossum氏によって開発されました。...

こういう感じで、hybrid検索のどっちの結果なのかがわかりにくい　top_K * 2件だと使う側が困惑するので、うまくtop_Kの数だけ返すようにしないとね
  - `注目すべきポイント`: hybrid検索の結果件数とユーザー体験

**実際のプロンプト**
```
以下は{システム名}の実行ログです。

{実行ログ全文}

上記のログを分析し、以下の観点で報告してください：
1. 実行の概要（何を実行したか）
2. 発生した問題・エラー
3. 問題の原因
4. 推奨される修正方法

特にhybrid検索の結果件数とユーザー体験に注目して分析してください。

出力形式：
- 実行概要
- 問題点リスト
- 原因分析
- 修正提案
```
