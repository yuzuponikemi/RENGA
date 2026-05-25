---
name: 環境構築・トラブル解決
skill_id: da252363-50f3-4728-9916-7216554158dd
version: 1.0.0
category: 操作手順の質問
status: public
source_count: 15
unique_user_count: 1
variables:
- OS
- プロジェクト名
- 現在の状況
- 発生している問題
- 希望する解決方法
- 追加情報
triggers:
- モジュールがインストールできない
- venvの作り方教えて
- エラーが出たので見てほしい
- uvで環境構築したい
- docker composeの設定を確認して
---

# 環境構築・トラブル解決

**説明**: Python環境構築やエラー解決の手順を質問するスキル
**ステータス**: ✅ 公開中 | **ソース数**: 15 件 | **ユニークユーザー**: 1 人 | **カテゴリ**: 操作手順の質問

---

## テンプレートプロンプト

```
私は{OS}で{プロジェクト名}を開発しています。{現在の状況}という状態です。{発生している問題}を解決したいです。{希望する解決方法}で対応してください。{追加情報}
```

## 変数一覧

- `{{OS}}`: 使用しているOS（例: macOS, Windows, Linux）
- `{{プロジェクト名}}`: 作業中のプロジェクト名（例: あなたのプロジェクト名）
- `{{現在の状況}}`: 現在の環境や実行中のコマンド（例: venv内でアプリを実行中）
- `{{発生している問題}}`: 具体的なエラーや問題（例: ModuleNotFoundError, コマンドが見つからない）
- `{{希望する解決方法}}`: 希望する解決手段（例: uvを使ってvenv作成、requirements.txtのインストール）
- `{{追加情報}}`: その他の補足情報（例: エラーログ、バージョン情報）

## 活用シーン

- Pythonモジュールのインストールエラーが発生したとき
- 仮想環境の作成方法がわからないとき
- Dockerやデータベースのセットアップ手順を確認したいとき

## トリガーフレーズ

- `モジュールがインストールできない`
- `venvの作り方教えて`
- `エラーが出たので見てほしい`
- `uvで環境構築したい`
- `docker composeの設定を確認して`

---

## 具体インスタンス

### インスタンス 1: モジュール不足エラー解決

> 元プロンプト: *(venv) {ユーザー名}@{ホスト名} {プロジェクト名} % python app.py       /{パス}/venv/lib/python3.9/site-packages/urllib3/__init__.py:35: Not*

**変数の値**
  - `OS`: macOS
  - `プロジェクト名`: {プロジェクト名}
  - `現在の状況`: venv内でpython app.pyを実行中
  - `発生している問題`: ModuleNotFoundError: No module named 'langchain_text_splitters'
  - `希望する解決方法`: uvを使って必要なモジュールをインストール
  - `追加情報`: エラーログは以下です：
(venv) {ユーザー名}@{ホスト名} {プロジェクト名} % python app.py      
/{パス}/venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
Traceback (most recent call last):
  File "/{パス}/app.py", line 6, in <module>
    from document_processor.file_handler import DocumentProcessor
  File "/{パス}/document_processor/file_handler.py", line 8, in <module>
    from langchain_text_splitters import MarkdownHeaderTextSplitter
ModuleNotFoundError: No module named 'langchain_text_splitters'

**実際のプロンプト**
```
私はmacOSで{プロジェクト名}を開発しています。venv内でpython app.pyを実行中という状態です。ModuleNotFoundError: No module named 'langchain_text_splitters'という問題を解決したいです。uvを使って必要なモジュールをインストールしてください。エラーログは以下です：
(venv) {ユーザー名}@{ホスト名} {プロジェクト名} % python app.py      
/{パス}/venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
Traceback (most recent call last):
  File "/{パス}/app.py", line 6, in <module>
    from document_processor.file_handler import DocumentProcessor
  File "/{パス}/document_processor/file_handler.py", line 8, in <module>
    from langchain_text_splitters import MarkdownHeaderTextSplitter
ModuleNotFoundError: No module named 'langchain_text_splitters'
```

---

### インスタンス 2: uvでvenv作成

> 元プロンプト: *{ユーザー名}@{ホスト名} {プロジェクト名} % python -m venv .venv zsh: command not found: python {ユーザー名}@{ホスト名} {プロジェクト名} %   can you crea*

**変数の値**
  - `OS`: macOS
  - `プロジェクト名`: {プロジェクト名}
  - `現在の状況`: python -m venv .venvを実行したらzsh: command not found: python
  - `発生している問題`: pythonコマンドが見つからない
  - `希望する解決方法`: uvを使ってvenvを作成
  - `追加情報`: なし

**実際のプロンプト**
```
私はmacOSで{プロジェクト名}を開発しています。python -m venv .venvを実行したらzsh: command not found: pythonという状態です。pythonコマンドが見つからない問題を解決したいです。uvを使ってvenvを作成してください。追加情報はありません。
```

---

### インスタンス 3: Docker+Neo4j設定確認

> 元プロンプト: *okay now docker is running and compose up done, but can you re-check my s.env file settings, is it okay as is? I think w*

**変数の値**
  - `OS`: macOS
  - `プロジェクト名`: {プロジェクト名}
  - `現在の状況`: docker compose upが完了した
  - `発生している問題`: s.envファイルの設定が正しいか確認したい
  - `希望する解決方法`: ユーザー名やURLを修正する必要があるかもしれません
  - `追加情報`: Dockerファイルとws.envファイルも作成済みで、Neo4jをセットアップしています

**実際のプロンプト**
```
私はmacOSで{プロジェクト名}を開発しています。docker compose upが完了したという状態です。s.envファイルの設定が正しいか確認したいです。ユーザー名やURLを修正する必要があるかもしれません。Dockerファイルとws.envファイルも作成済みで、Neo4jをセットアップしています。
```
