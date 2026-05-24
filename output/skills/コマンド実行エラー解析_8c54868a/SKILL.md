---
name: コマンド実行エラー解析
skill_id: 8c54868a-d3a8-4f78-8247-6ba1b2773faf
version: 1.0.0
category: コマンド実行エラー解析
status: public
source_count: 6
unique_user_count: 5
variables:
- error_log
- username
- project_dir
- command
triggers:
- エラーが出たので見てください
- このエラーどうすればいい？
- 修正して
- エラー解析して
- エラーログを添付します
---

# コマンド実行エラー解析

**説明**: エラーログから原因を特定し修正方法を提案する
**ステータス**: ✅ 公開中 | **ソース数**: 6 件 | **ユニークユーザー**: 5 人 | **カテゴリ**: コマンド実行エラー解析

---

## テンプレートプロンプト

```
以下のエラーを解析して修正方法を提案してください。

エラー内容:
{error_log}

実行環境:
- ユーザー: {username}
- 作業ディレクトリ: {project_dir}
- 使用コマンド: {command}

エラーの原因を特定し、具体的な修正手順をステップバイステップで説明してください。
```

## 変数一覧

- `{{error_log}}`: エラーログ全文（例: Tracebackから始まるPythonエラーなど）
- `{{username}}`: ユーザー名（例: あなたのユーザー名）
- `{{project_dir}}`: プロジェクトディレクトリ名（例: あなたのプロジェクト名）
- `{{command}}`: 実行したコマンド（例: uv run プロジェクト名 cron --install）

## 活用シーン

- Pythonスクリプト実行時のImportErrorやAttributeErrorの解決
- 機械学習モデル読み込み時のpickleエラーの修正
- サーバー起動時のモジュールインポートエラーのデバッグ

## トリガーフレーズ

- `エラーが出たので見てください`
- `このエラーどうすればいい？`
- `修正して`
- `エラー解析して`
- `エラーログを添付します`

---

## 具体インスタンス

### インスタンス 1: AttributeError解析

> 元プロンプト: *了解です　{username}@{ホスト名} {プロジェクト名} % uv run {プロジェクト名} cron --install Traceback (most recent call last):   File "{ユーザーのホームデ*

**変数の値**
  - `error_log`: Traceback (most recent call last):
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/.venv/bin/{プロジェクト名}", line 10, in <module>
    sys.exit(main())
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/{プロジェクト名}/cli.py", line 47, in main
    _setup_logging(args.verbose)
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/{プロジェクト名}/cli.py", line 47, in main
    _setup_logging(args.verbose)
                   ^^^^^^^^^^^^
AttributeError: 'Namespace' object has no attribute 'verbose'
  - `username`: {username}
  - `project_dir`: {プロジェクト名}
  - `command`: uv run {プロジェクト名} cron --install

**実際のプロンプト**
```
以下のエラーを解析して修正方法を提案してください。

エラー内容:
Traceback (most recent call last):
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/.venv/bin/{プロジェクト名}", line 10, in <module>
    sys.exit(main())
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/{プロジェクト名}/cli.py", line 47, in main
    _setup_logging(args.verbose)
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/{プロジェクト名}/cli.py", line 47, in main
    _setup_logging(args.verbose)
                   ^^^^^^^^^^^^
AttributeError: 'Namespace' object has no attribute 'verbose'

実行環境:
- ユーザー: {username}
- 作業ディレクトリ: {プロジェクト名}
- 使用コマンド: uv run {プロジェクト名} cron --install

エラーの原因を特定し、具体的な修正手順をステップバイステップで説明してください。
```

---

### インスタンス 2: ImportError解析

> 元プロンプト: *{username}@{ホスト名} {プロジェクト名} % uv run src/server.py       Built {プロジェクト名} @ file://{ユーザーのホームディレクトリ}/source/personal/{プロジェ*

**変数の値**
  - `error_log`: Traceback (most recent call last):
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/server.py", line 11, in <module>
    from .indexer import WikiIndexer, LocalFileIndexer
ImportError: attempted relative import with no known parent package

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/server.py", line 13, in <module>
    from indexer import WikiIndexer, LocalFileIndexer
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/indexer.py", line 17, in <module>
    from .chunking import ChunkingStrategy, get_config_for_file, get_smart_config
ImportError: attempted relative import with no known parent package
  - `username`: {username}
  - `project_dir`: {プロジェクト名}
  - `command`: uv run src/server.py

**実際のプロンプト**
```
以下のエラーを解析して修正方法を提案してください。

エラー内容:
Traceback (most recent call last):
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/server.py", line 11, in <module>
    from .indexer import WikiIndexer, LocalFileIndexer
ImportError: attempted relative import with no known parent package

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/server.py", line 13, in <module>
    from indexer import WikiIndexer, LocalFileIndexer
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/src/indexer.py", line 17, in <module>
    from .chunking import ChunkingStrategy, get_config_for_file, get_smart_config
ImportError: attempted relative import with no known parent package

実行環境:
- ユーザー: {username}
- 作業ディレクトリ: {プロジェクト名}
- 使用コマンド: uv run src/server.py

エラーの原因を特定し、具体的な修正手順をステップバイステップで説明してください。
```

---

### インスタンス 3: pickleエラー解析

> 元プロンプト: *{username}@{ホスト名} {プロジェクト名} % uv run python main.py  {ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/.venv/lib/python3.11/sit*

**変数の値**
  - `error_log`: Traceback (most recent call last):
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/ui/game_view.py", line 120, in _create_player
    strategy = NeuralPlayerFactory.create(
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/neural_player.py", line 324, in create
    cls._instance = NeuralPlayer(
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/neural_player.py", line 68, in __init__
    self._load_model()
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/neural_player.py", line 83, in _load_model
    checkpoint = torch.load(self._model_path, map_location=self._device)
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/.venv/lib/python3.11/site-packages/torch/serialization.py", line 1548, in load
    raise pickle.UnpicklingError(_get_wo_message(str(e))) from None
_pickle.UnpicklingError: Weights only load failed. This file can still be loaded, to do so you have two options, do those steps only if you trust the source of the checkpoint. 
        (1) In PyTorch 2.6, we changed the default value of the `weights_only` argument in `torch.load` from `False` to `True`. Re-running `torch.load` with `weights_only` set to `False` will likely succeed, but it can result in arbitrary code execution. Do it only if you got the file from a trusted source.
        (2) Alternatively, to load with `weights_only=True` please check the recommended steps in the following error message.
        WeightsUnpickler error: Unsupported global: GLOBAL model.GomokuGPTConfig was not an allowed global by default. Please use `torch.serialization.add_safe_globals([model.GomokuGPTConfig])` or the `torch.serialization.safe_globals([model.GomokuGPTConfig])` context manager to allowlist this global if you trust this class/function.
  - `username`: {username}
  - `project_dir`: {プロジェクト名}
  - `command`: uv run python main.py

**実際のプロンプト**
```
以下のエラーを解析して修正方法を提案してください。

エラー内容:
Traceback (most recent call last):
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/ui/game_view.py", line 120, in _create_player
    strategy = NeuralPlayerFactory.create(
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/neural_player.py", line 324, in create
    cls._instance = NeuralPlayer(
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/neural_player.py", line 68, in __init__
    self._load_model()
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/neural_player.py", line 83, in _load_model
    checkpoint = torch.load(self._model_path, map_location=self._device)
  File "{ユーザーのホームディレクトリ}/source/personal/{プロジェクト名}/.venv/lib/python3.11/site-packages/torch/serialization.py", line 1548, in load
    raise pickle.UnpicklingError(_get_wo_message(str(e))) from None
_pickle.UnpicklingError: Weights only load failed. This file can still be loaded, to do so you have two options, do those steps only if you trust the source of the checkpoint. 
        (1) In PyTorch 2.6, we changed the default value of the `weights_only` argument in `torch.load` from `False` to `True`. Re-running `torch.load` with `weights_only` set to `False` will likely succeed, but it can result in arbitrary code execution. Do it only if you got the file from a trusted source.
        (2) Alternatively, to load with `weights_only=True` please check the recommended steps in the following error message.
        WeightsUnpickler error: Unsupported global: GLOBAL model.GomokuGPTConfig was not an allowed global by default. Please use `torch.serialization.add_safe_globals([model.GomokuGPTConfig])` or the `torch.serialization.safe_globals([model.GomokuGPTConfig])` context manager to allowlist this global if you trust this class/function.

実行環境:
- ユーザー: {username}
- 作業ディレクトリ: {プロジェクト名}
- 使用コマンド: uv run python main.py

エラーの原因を特定し、具体的な修正手順をステップバイステップで説明してください。
```
