# Skill Hub Agent

**社内AIスキル循環エージェント** — Microsoft Agent Hackathon 2026 提出作品

> 個人の善意を、AIが代わりに可視化する。

## コンセプト

組織のAI利用ログを観察し、繰り返し成功しているパターンを **匿名で・自動で・再利用可能なスキル** として抽出・流通させる Agentic レイヤー。

| 新規性 | 内容 |
|---|---|
| ボトムアップ自動抽出 | 人が登録するのではなく、利用ログから自動で発見 |
| 匿名公開 | 提供側・利用側双方の心理障壁を解除 |
| 貢献者評価 | 利用回数は内部で創作者に紐付き、評価面談時に可視化 |

## アーキテクチャ

```
[Copilot Logs] → ① Extractor Agent → ② Anonymizer Agent
                                              ↓
                                       [Cosmos DB + Azure AI Search]
                                              ↓
                              ③ Recommender Agent → Copilot Studio UI
                                              ↓
                                       Auto-MCPify → トピック YAML
```

詳細は [docs/architecture.md](docs/architecture.md) 参照。

## Microsoft スタック

- **Azure AI Agent Service** — 3エージェント実行基盤
- **Azure OpenAI / DeepSeek** — LLM
- **Azure Cosmos DB** — スキルカタログ永続化（推奨技術）
- **Azure Functions** — HTTP + Timer trigger（必須要件）
- **Copilot Studio** — ユーザー向けUI（必須要件）
- **Microsoft Entra ID** — 匿名ハンドル認証（推奨技術）

## セットアップ

> 📘 別 PC からの参加手順（マルチユーザー登録・組織連携を含む）は [docs/getting_started.md](docs/getting_started.md) を参照してください。

```bash
# 依存パッケージのインストール
uv sync

# 環境変数の設定
cp .env.example .env
# .env を編集して Azure 認証情報を入力

# パイプライン実行（ログ → スキル抽出 → カタログ保存 → YAML生成）
uv run python main.py

# API サーバー起動
uv run uvicorn api:app --reload

# スキル推薦 CLI
uv run python recommend.py "メールを整理したい"

# デモ（3分シナリオ）
uv run python demo.py

# E2E テスト
uv run python smoke_test.py
```

## API エンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| `POST` | `/recommend` | スキル推薦（Copilot Studio から呼ぶ） |
| `GET` | `/skills` | 公開スキル一覧 |
| `GET` | `/stats` | カタログ統計 |
| `GET` | `/dashboard` | 匿名コントリビューションダッシュボード |
| `POST` | `/mcpify` | Copilot Studio トピック YAML 自動生成 |
| `GET` | `/openapi.json` | OpenAPI スキーマ（Copilot Studio 連携用） |

## ハッカソン情報

- **名称**: Microsoft Agent Hackathon powered by Tokyo Electron Device
- **主催**: クラスメソッド株式会社
- **提出締切**: 2026年6月1日 23:59
- **審査期間**: 6月2日〜18日（デプロイ稼働維持が必要）
