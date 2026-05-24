---
name: コード実行と問題修正
skill_id: 5b17eaca-f5c5-4870-ba47-447f1b858662
version: 1.0.0
category: コマンド実行と問題修正
status: public
source_count: 5
unique_user_count: 3
variables:
- command
- issue_description
- target_files
- investigation_focus
- expected_outcome
triggers:
- このコマンドを実行して
- 実行して問題を修正して
- なぜか動かない、原因を調べて
- この処理を全ての〜に対して実行して
- 実装を調査して
---

# コード実行と問題修正

**説明**: コマンド実行指示とエラー調査・修正を依頼するスキル
**ステータス**: ✅ 公開中 | **ソース数**: 5 件 | **ユニークユーザー**: 3 人 | **カテゴリ**: コマンド実行と問題修正

---

## テンプレートプロンプト

```
以下のタスクを実行してください：

【実行コマンド】
{command}

【問題の説明】
{issue_description}

【調査対象ファイル】
{target_files}

【調査の焦点】
{investigation_focus}

【期待する成果】
{expected_outcome}
```

## 変数一覧

- `{{command}}`: 実行するコマンド（例: python src/regen_summary.py）
- `{{issue_description}}`: 発生している問題や実行したい処理の説明（例: 既存エピソードの再生成を全て実行したい）
- `{{target_files}}`: 調査・修正が必要なファイルパス（例: src/indexer.py, src/loaders.py）
- `{{investigation_focus}}`: 調査の具体的な焦点や確認ポイント（例: インデックス構築フロー、永続化戦略）
- `{{expected_outcome}}`: 期待する成果や完了条件（例: 問題の原因特定と修正案の提示）

## 活用シーン

- スクリプトを実行してエラーが出たので原因調査と修正を依頼する
- 既存の全データに対してバッチ処理を実行するよう指示する
- 特定のモジュールの実装を調査し、別モジュールに適用できるか検討する

## トリガーフレーズ

- `このコマンドを実行して`
- `実行して問題を修正して`
- `なぜか動かない、原因を調べて`
- `この処理を全ての〜に対して実行して`
- `実装を調査して`

---

## 具体インスタンス

### インスタンス 1: エピソード再生成実行

> 元プロンプト: *既存エピソードの再生成は    python src/regen_summary.py　これを全ての既存エピソードに対して実行して*

**変数の値**
  - `command`: python src/regen_summary.py
  - `issue_description`: 既存エピソードの再生成を全ての既存エピソードに対して実行したい
  - `target_files`: （特になし）
  - `investigation_focus`: （特になし）
  - `expected_outcome`: 全ての既存エピソードに対して再生成が実行されること

**実際のプロンプト**
```
以下のタスクを実行してください：

【実行コマンド】
python src/regen_summary.py

【問題の説明】
既存エピソードの再生成を全ての既存エピソードに対して実行したい

【調査対象ファイル】
（特になし）

【調査の焦点】
（特になし）

【期待する成果】
全ての既存エピソードに対して再生成が実行されること
```

---

### インスタンス 2: サーバー起動エラー調査

> 元プロンプト: *.envでLOCALDOCSPATHは指定しているんやけど、server.pyを起動してもなぜかNoneになってるらしい　なんでやろ*

**変数の値**
  - `command`: uv run src/server.py
  - `issue_description`: .envでLOCALDOCSPATHは指定しているのに、server.pyを起動してもNoneになってしまう。原因を調査して修正してほしい。
  - `target_files`: src/server.py, .env
  - `investigation_focus`: 環境変数LOCALDOCSPATHが正しく読み込まれない原因。.envの読み込み処理、server.py内での環境変数参照箇所。
  - `expected_outcome`: 問題の原因特定と修正案の提示、または修正コードの提供

**実際のプロンプト**
```
以下のタスクを実行してください：

【実行コマンド】
uv run src/server.py

【問題の説明】
.envでLOCALDOCSPATHは指定しているのに、server.pyを起動してもNoneになってしまう。原因を調査して修正してほしい。

【調査対象ファイル】
src/server.py, .env

【調査の焦点】
環境変数LOCALDOCSPATHが正しく読み込まれない原因。.envの読み込み処理、server.py内での環境変数参照箇所。

【期待する成果】
問題の原因特定と修正案の提示、または修正コードの提供
```

---

### インスタンス 3: インデックス構築フロー調査

> 元プロンプト: *探索タスク：LocalFileIndexerの現在のインデックス構築プロセスを理解する  以下を調査してください： 1. LocalFileIndexer.build_index()メソッドの完全な実装 2. どのようにファイルを読み込み、*

**変数の値**
  - `command`: （調査のみ、コマンド実行不要）
  - `issue_description`: LocalFileIndexerの現在のインデックス構築プロセスを理解するため、以下の調査を実施してください。
  - `target_files`: src/indexer.py (LocalFileIndexerクラス)
src/loaders.py
  - `investigation_focus`: 1. LocalFileIndexer.build_index()メソッドの完全な実装
2. どのようにファイルを読み込み、インデックスを構築しているか
3. ChromaDBとBM25インデックスをどのように扱っているか
4. 現在の永続化戦略（何が保存され、何が毎回再構築されるか）
5. loaders.pyのload_local_files()関数の実装
  - `expected_outcome`: 現在のインデックス構築フローを完全に理解したドキュメントまたは説明

**実際のプロンプト**
```
以下のタスクを実行してください：

【実行コマンド】
（調査のみ、コマンド実行不要）

【問題の説明】
LocalFileIndexerの現在のインデックス構築プロセスを理解するため、以下の調査を実施してください。

【調査対象ファイル】
src/indexer.py (LocalFileIndexerクラス)
src/loaders.py

【調査の焦点】
1. LocalFileIndexer.build_index()メソッドの完全な実装
2. どのようにファイルを読み込み、インデックスを構築しているか
3. ChromaDBとBM25インデックスをどのように扱っているか
4. 現在の永続化戦略（何が保存され、何が毎回再構築されるか）
5. loaders.pyのload_local_files()関数の実装

【期待する成果】
現在のインデックス構築フローを完全に理解したドキュメントまたは説明
```
