# アーキテクチャ図

Zenn 記事埋め込み用。Mermaid と説明文のセット。

## システム全体図

```mermaid
flowchart TD
    subgraph INPUT["入力層"]
        LOGS["合成 Copilot ログ\n(JSON 20件)\n実環境: Graph API"]
    end

    subgraph AGENTS["エージェント層 (Azure AI Agent Service)"]
        EXT["① Extractor Agent\n成功シグナル抽出\nパターンクラスタリング\nk=3 ゲート"]
        ANO["② Anonymizer Agent\n固有名詞 → 変数化\n一般化・抽象化"]
        REC["③ Recommender Agent\nユーザー文脈で検索\nスキル推薦"]
    end

    subgraph STORE["ストレージ層"]
        COSMOS[("Cosmos DB\nスキルカタログ")]
        SEARCH["Azure AI Search\nセマンティック検索"]
    end

    subgraph OUTPUT["出力層"]
        CS["Copilot Studio\nチャット UI\nスキル検索"]
        DASH["匿名ダッシュボード\n貢献者 #A1, #B3..."]
        YAML["Auto-MCPify\nCopilot Studio\nトピック YAML"]
    end

    subgraph INFRA["インフラ"]
        FUNC["Azure Functions\nTimer + HTTP trigger"]
        AOI["Azure OpenAI\ngpt-4o / DeepSeek"]
        ENT["Entra ID\n匿名ハンドル発行"]
    end

    LOGS --> EXT
    EXT -->|"抽出スキル"| ANO
    ANO -->|"匿名化スキル"| COSMOS
    COSMOS --> SEARCH
    SEARCH --> REC
    REC --> CS
    COSMOS --> DASH
    COSMOS --> YAML
    YAML --> CS
    EXT & ANO & REC --> AOI
    FUNC --> EXT
    ENT --> DASH
```

## データフロー詳細

```mermaid
sequenceDiagram
    participant U as ユーザー A
    participant C as Copilot
    participant OBS as Extractor Agent
    participant ANO as Anonymizer Agent
    participant CAT as Skill Catalog
    participant REC as Recommender Agent
    participant U2 as ユーザー B

    U->>C: プロンプト入力
    C->>U: 回答 (accepted=true)
    Note over OBS: 3人以上が類似パターン到達
    OBS->>OBS: 成功シグナル検出・クラスタリング
    OBS->>ANO: 生スキルテンプレート
    ANO->>ANO: 固有名詞 → {{変数}} に変換
    ANO->>CAT: 匿名スキル保存 (status=public)
    Note over CAT: contributor: #A1 (内部のみ)

    U2->>REC: 「メール整理したい」
    REC->>CAT: セマンティック検索
    CAT->>REC: 関連スキル
    REC->>U2: 「3人の同僚が解決しています。使いますか？」
```

## Microsoft スタック対応表

| コンポーネント | 技術 | 必須/推奨 |
|---|---|---|
| エージェント実行 | Azure AI Agent Service | 必須（Agentic 評価の主軸） |
| LLM | Azure OpenAI gpt-4o / DeepSeek | 必須 |
| スキルカタログ | **Azure Cosmos DB** | 推奨技術（加点） |
| セマンティック検索 | Azure AI Search | 必須（スキル発見） |
| 実行基盤 | **Azure Functions** HTTP+Timer | 必須要件クリア |
| ユーザー UI | **Copilot Studio** | 必須要件クリア |
| 認証 | **Microsoft Entra ID** | 推奨技術（加点） |
| CI/CD | **GitHub / GitHub Copilot** | 推奨技術（加点） |
