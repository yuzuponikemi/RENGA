---
name: コードベース探索
skill_id: 163d9fd3-c9ac-4e93-a7eb-fc4b5a915ecd
version: 1.0.0
category: コードベース探索
status: public
source_count: 4
unique_user_count: 4
variables:
- target_feature
- main_file_path
- integration_file_path
- parent_component
- config_file_path
- env_file_path
- base_class_file_path
- test_script_path
- external_service
triggers:
- このコードベースの〇〇を調査して
- 〇〇の実装を詳しく教えて
- 〇〇の統合方法を調べて
- 〇〇の設定方法をコードから確認して
- 〇〇の接続フローを解析して
---

# コードベース探索

**説明**: コードベース内の特定機能や実装を調査するスキル
**ステータス**: ✅ 公開中 | **ソース数**: 4 件 | **ユニークユーザー**: 4 人 | **カテゴリ**: コードベース探索

---

## テンプレートプロンプト

```
Explore the {target_feature} integration in this codebase. I need to understand:

1. Read {main_file_path} - the full implementation
2. Read {integration_file_path} - how {target_feature} is integrated into the {parent_component}
3. Read {config_file_path} - what {target_feature} configuration is expected
4. Read {env_file_path} if it exists - current {target_feature} configuration
5. Read {base_class_file_path} - the base class
6. Check {test_script_path} for {target_feature} testing capability

Report all the details about:
- How the {target_feature} connects to the {external_service} (stdio? command? args?)
- What environment variables are needed
- How the {parent_component} selects/uses {target_feature}
- What the search flow looks like
- Any configuration that needs to be set up
```

## 変数一覧

- `{{target_feature}}`: 調査対象の機能名（例: 検索プロバイダ、モデルクラス）
- `{{main_file_path}}`: 主要実装ファイルのパス
- `{{integration_file_path}}`: 統合部分のファイルパス
- `{{parent_component}}`: 機能が統合される親コンポーネント名
- `{{config_file_path}}`: 設定ファイルのパス
- `{{env_file_path}}`: 環境変数ファイルのパス
- `{{base_class_file_path}}`: 基底クラスのファイルパス
- `{{test_script_path}}`: テストスクリプトのパス
- `{{external_service}}`: 接続先の外部サービス名

## 活用シーン

- 新しい外部API連携機能のコードベース調査
- 既存のプロバイダー実装の理解と拡張
- 特定の設定や環境変数が必要な機能の導入準備

## トリガーフレーズ

- `このコードベースの〇〇を調査して`
- `〇〇の実装を詳しく教えて`
- `〇〇の統合方法を調べて`
- `〇〇の設定方法をコードから確認して`
- `〇〇の接続フローを解析して`

---

## 具体インスタンス

### インスタンス 1: MCPプロバイダ調査

> 元プロンプト: *Explore the MCP search provider integration in this codebase. I need to understand:  1. Read src/utils/search_providers/*

**変数の値**
  - `target_feature`: MCP search provider
  - `main_file_path`: src/utils/search_providers/mcp_provider.py
  - `integration_file_path`: src/utils/search_providers/provider_manager.py
  - `parent_component`: provider manager
  - `config_file_path`: .env.example
  - `env_file_path`: .env
  - `base_class_file_path`: src/utils/search_providers/base_provider.py
  - `test_script_path`: scripts/utils/check_search_providers.py
  - `external_service`: MCP server

**実際のプロンプト**
```
Explore the {target_feature} integration in this codebase. I need to understand:

1. Read {main_file_path} - the full implementation
2. Read {integration_file_path} - how {target_feature} is integrated into the {parent_component}
3. Read {config_file_path} - what {target_feature} configuration is expected
4. Read {env_file_path} if it exists - current {target_feature} configuration
5. Read {base_class_file_path} - the base class
6. Check {test_script_path} for {target_feature} testing capability

Report all the details about:
- How the {target_feature} connects to the {external_service} (stdio? command? args?)
- What environment variables are needed
- How the {parent_component} selects/uses {target_feature}
- What the search flow looks like
- Any configuration that needs to be set up
```

---

### インスタンス 2: deepevalパッケージ調査

> 元プロンプト: *Search the installed deepeval package for the OllamaModel class. I need to know: 1. The import path for OllamaModel 2. C*

**変数の値**
  - `target_feature`: OllamaModel
  - `main_file_path`: {venv_path}/lib/python*/site-packages/deepeval/models/ollama.py
  - `integration_file_path`: {venv_path}/lib/python*/site-packages/deepeval/metrics/answer_relevancy.py
  - `parent_component`: AnswerRelevancyMetric
  - `config_file_path`: {venv_path}/lib/python*/site-packages/deepeval/__init__.py
  - `env_file_path`: {venv_path}/lib/python*/site-packages/deepeval/models/__init__.py
  - `base_class_file_path`: {venv_path}/lib/python*/site-packages/deepeval/models/base_model.py
  - `test_script_path`: {venv_path}/lib/python*/site-packages/deepeval/metrics/faithfulness.py
  - `external_service`: Ollama server

**実際のプロンプト**
```
Explore the {target_feature} integration in this codebase. I need to understand:

1. Read {main_file_path} - the full implementation
2. Read {integration_file_path} - how {target_feature} is integrated into the {parent_component}
3. Read {config_file_path} - what {target_feature} configuration is expected
4. Read {env_file_path} if it exists - current {target_feature} configuration
5. Read {base_class_file_path} - the base class
6. Check {test_script_path} for {target_feature} testing capability

Report all the details about:
- How the {target_feature} connects to the {external_service} (stdio? command? args?)
- What environment variables are needed
- How the {parent_component} selects/uses {target_feature}
- What the search flow looks like
- Any configuration that needs to be set up
```
