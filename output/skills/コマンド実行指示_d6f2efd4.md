# 🔷 スキル定義: コマンド実行エラー解決

**説明**: コマンド実行時のエラーを分析・修正するスキル
**ステータス**: ✅ 公開中 | **ソース数**: 14 件 | **カテゴリ**: コマンド実行指示

---

## テンプレートプロンプト（抽象）

```
以下のエラーが発生しています。原因を特定し、修正方法を提案してください。

実行コマンド: {command}
エラーメッセージ: {error_message}

追加情報:
- プロジェクトディレクトリ: {project_dir}
- 実行環境: {environment}
- 試した解決策: {attempted_solutions}

期待する動作: {expected_behavior}
```

## 変数一覧

- `{{command}}`: 実行したコマンド（例: uv run src/server.py）
- `{{error_message}}`: エラーメッセージ全文（例: ImportError: attempted relative import with no known parent package）
- `{{project_dir}}`: プロジェクトのディレクトリパス（例: /Users/username/project）
- `{{environment}}`: 実行環境の詳細（例: Python 3.11, uv, macOS）
- `{{attempted_solutions}}`: 既に試した解決策（例: パッケージの再インストール、パスの確認）
- `{{expected_behavior}}`: 期待する正常な動作（例: サーバーが起動してリクエストを受け付ける）

## 活用シーン

- スクリプト実行時のImportError解決
- CLIツールのコマンド実行エラー修正
- 環境変数が正しく読み込まれない問題のデバッグ

---

# 🔶 具体インスタンス

### インスタンス 1: ImportError修正

> 元プロンプト: *ユーザー環境でコマンドを実行した際のエラー出力*

**変数の値**
  - `command`: uv run src/server.py
  - `error_message`: ImportError: attempted relative import with no known parent package
  - `project_dir`: {project_dir}
  - `environment`: Python 3.11, uv, macOS
  - `attempted_solutions`: なし
  - `expected_behavior`: サーバーが正常に起動し、ローカル検索機能を提供する

**実際のプロンプト**
```
以下のエラーが発生しています。原因を特定し、修正方法を提案してください。

実行コマンド: uv run src/server.py
エラーメッセージ: Traceback (most recent call last):
  File "{project_dir}/src/server.py", line 11, in <module>
    from .indexer import WikiIndexer, LocalFileIndexer
ImportError: attempted relative import with no known parent package

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "{project_dir}/src/server.py", line 13, in <module>
    from indexer import WikiIndexer, LocalFileIndexer
  File "{project_dir}/src/indexer.py", line 17, in <module>
    from .chunking import ChunkingStrategy, get_config_for_file, get_smart_config
ImportError: attempted relative import with no known parent package

追加情報:
- プロジェクトディレクトリ: {project_dir}
- 実行環境: Python 3.11, uv, macOS
- 試した解決策: なし

期待する動作: サーバーが正常に起動し、ローカル検索機能を提供する
```

---

### インスタンス 2: 環境変数None問題

> 元プロンプト: *ユーザーからの質問: .envで環境変数を指定しているが、起動時にNoneになる問題*

**変数の値**
  - `command`: uv run src/server.py
  - `error_message`: .envで{環境変数名}は指定しているんやけど、server.pyを起動してもなぜかNoneになってるらしい
  - `project_dir`: {project_dir}
  - `environment`: Python 3.11, uv, macOS
  - `attempted_solutions`: .envファイルの確認、環境変数の読み込み方法の確認
  - `expected_behavior`: {環境変数名}環境変数が正しく読み込まれ、サーバーがドキュメントパスを認識する

**実際のプロンプト**
```
以下のエラーが発生しています。原因を特定し、修正方法を提案してください。

実行コマンド: uv run src/server.py
エラーメッセージ: .envで{環境変数名}は指定しているんやけど、server.pyを起動してもなぜかNoneになってるらしい

追加情報:
- プロジェクトディレクトリ: {project_dir}
- 実行環境: Python 3.11, uv, macOS
- 試した解決策: .envファイルの確認、環境変数の読み込み方法の確認

期待する動作: {環境変数名}環境変数が正しく読み込まれ、サーバーがドキュメントパスを認識する
```

---

### インスタンス 3: データセットスキップ確認

> 元プロンプト: *ユーザー環境でコマンドを実行した際のログ出力*

**変数の値**
  - `command`: uv run src/server.py
  - `error_message`: これは、すでに小さいデータセットダウンロードしてあるので、本番用データセットのダウンロードをスキップしてないか？
  - `project_dir`: {project_dir}
  - `environment`: Python 3.11, uv, macOS
  - `attempted_solutions`: データセットのダウンロード状態の確認
  - `expected_behavior`: 本番用データセットが正しくダウンロードされ、サーバーがフル機能で動作する

**実際のプロンプト**
```
以下のエラーが発生しています。原因を特定し、修正方法を提案してください。

実行コマンド: uv run src/server.py
エラーメッセージ: これは、すでに小さいデータセットダウンロードしてあるので、本番用データセットのダウンロードをスキップしてないか？

追加情報:
- プロジェクトディレクトリ: {project_dir}
- 実行環境: Python 3.11, uv, macOS
- 試した解決策: データセットのダウンロード状態の確認

期待する動作: 本番用データセットが正しくダウンロードされ、サーバーがフル機能で動作する
```
