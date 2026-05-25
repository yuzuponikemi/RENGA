# Cosmos DB スキーマ設計

組織レベル (Layer 2) のスキル循環を実現するための Cosmos DB スキーマ。

5 コンテナ構成。匿名性・重複検知・カウント集約・贈与イベント・系統樹クレジットを
すべて表現できるよう、初期スキーマで必要フィールドを確保する。

---

## データベース

- **DB 名**: `skill-hub`
- **アカウント**: `renga-skill-hub`（仮）
- **API**: Core (SQL)
- **整合性レベル**: Session（既定）
- **スループット**: 各コンテナ 400 RU/s（共有スループットでも可）

---

## コンテナ 1: `skills`

公開された抽象スキル。Layer 1 の個人 GitHub repo から Azure Function が集約。
書き込みは Function のみ、個人 PC は read-only。

### パーティションキー
`/category`

### ドキュメントスキーマ

```yaml
id: skill_uuid                          # Cosmos の id (= skill_id)
skill_id: skill_uuid

# 既存フィールド（ExtractedSkill モデル準拠）
name: "コードレビュー"
description: "..."
template_prompt: "..."
variables: ["..."]
variable_descriptions: { variable_name: "説明" }
example_use_cases: ["...", "...", "..."]
triggers: ["コードレビューして", "PR確認"]
category: "code_review"
status: "public" | "pending"

# 重複検知用（Function が計算）
embedding: [0.123, 0.456, ...]          # multilingual-E5-small 384 次元
content_hash: "sha256:abcd..."          # template_prompt の完全一致判定用

# 貢献者（Layer 1 から集約）
contributor_handles: ["#A1", "#B3"]     # 匿名ハンドルのみ
unique_user_count: 2                    # contributor_handles の len
source_count: 5                         # 抽出元ログの総件数（マージ時に加算）
first_contributor: "#A1"                # 最初に登録した人（名誉枠）
first_published_at: "2026-05-22T10:00:00Z"
last_updated_at: "2026-05-25T14:00:00Z"

# 系統樹（PICSY / 派生クレジット）
derived_from: ["parent_skill_uuid"]     # 親スキル（このスキルが派生したもとのスキル）
derived_to: ["child_skill_uuid"]        # 子スキル（クエリ高速化用の冗長保持）
lineage_depth: 0                        # ルートからの深さ（0 = オリジナル）

# 集計（usage_events から定期更新）
usage_count: 42                         # 累積利用回数
usage_by_team: { "eng": 30, "pm": 12 }  # クロスチーム加重計算用
last_used_at: "..."

# 具体インスタンス（オリジナルから引き継ぎ + マージ時に追加）
instances:
  - instance_id: "..."
    parent_skill_id: "skill_uuid"
    name: "..."
    filled_prompt: "..."
    variable_values: { ... }
    contributor_handle: "#A1"           # このインスタンスを提供した人
```

### マージロジック（Function が実装）

新規スキル受信 → embedding 計算 → 既存 `skills` に対してコサイン類似度検索:

| 類似度 | 動作 |
|---|---|
| `>= 0.92` | **完全マージ**: contributor_handles 追記、source_count 加算、instances 追加 |
| `0.75 - 0.92` | **派生扱い**: 新規 skill として登録、`derived_from` に類似スキルの id を設定 |
| `< 0.75` | **新規スキル**として独立登録 |

閾値はチューニング対象。最初は固定値で運用。

### インデックス

- `/contributor_handles/*` (Composite for handle queries)
- `/category` (default partition)
- `/status` (filter public/pending)
- `/usage_count` (sort)

---

## コンテナ 2: `contributor_mappings`

`user_id` ↔ `handle` 対応表。**最も機微な情報**。管理者 RBAC で保護。

### パーティションキー
`/handle`

### ドキュメントスキーマ

```yaml
id: "hash_of_user_id"                   # 平文 user_id は保存しない
user_id_hash: "sha256:..."              # 検索用に同じ値を持たせる
handle: "#A1"                           # 匿名ハンドル
team: "engineering"                     # クロスチーム加重用（任意）
github_repo: "github.com/alice/skills"  # Function が fetch 対象を知るため

joined_at: "2026-05-20T00:00:00Z"
last_activity_at: "..."

disclosed: false                        # 本人が「公表 OK」と切り替えた場合 true
                                        # → ダッシュボードで実名表示が可能になる
                                        # → デフォルトは false（匿名維持）

contribution_summary:                   # 軽量サマリー（高速応答用）
  total_skills: 12
  public_skills: 8
  total_usage_received: 145
```

### アクセス制御

- **書き込み**: Azure Function のみ（マネージドアイデンティティ）
- **読み取り**:
  - Function: 全件
  - 管理者: 全件 (Cosmos DB Built-in Data Contributor)
  - 個人 PC アプリ: **読み取り不可**（直接アクセスさせない）
  - 本人のハンドル参照: `/contributor/{handle}/report` API 経由のみ（後述）

### ガード

- `user_id_hash` は SHA-256 で固定塩 + ペッパー（環境変数 `HANDLE_SALT`）
- 同一人物が複数 user_id（複数 PC で git email 異なる等）を持つ場合の同定は出来ない
  → これは設計上の許容範囲（個人の意思で USER_ID 環境変数を統一すれば可能）

---

## コンテナ 3: `usage_events`

スキル利用の **不変ログ**。集計・贈与イベント生成・監査の素材。

### パーティションキー
`/skill_id`

### ドキュメントスキーマ

```yaml
id: "event_uuid"
event_type: "skill_used"                # 拡張余地: "skill_starred", "skill_forked", etc.
timestamp: "2026-05-25T14:30:00Z"
skill_id: "skill_uuid"
context: "mcp" | "copilot_studio" | "api"

user_handle: "#B3"                      # 使用者（読み取り側）

# 系統樹クレジット分配
# このスキルが parent から派生したものなら、parent の貢献者にも按分する
credit_distribution:
  "#A1": 0.7                            # 直接貢献者
  "#X9": 0.3                            # 親スキル貢献者（lineage 経由）

# クロスチーム加重
cross_team: true                        # 使用者と貢献者のチームが異なる
team_weight: 1.5                        # クロスチームインパクト係数

# 任意のメタデータ
metadata:
  client_version: "1.0.0"
  query: "コードをレビューしたい"          # （任意・プライバシー注意）
```

### TTL

90 日（または無期限）。集計済みデータは `contributor_reports` に残るので、
原データは TTL でクリーンアップしても再構築可能。

### アクセス制御

- **書き込み**: 個人 PC アプリ（API 経由・write-only）+ Function（集計時の付加）
- **読み取り**: Function（集計）+ 管理者
- 個人 PC からは直接読めない（PII 流出防止）

---

## コンテナ 4: `contributor_reports`

個人ビュー用の **集計キャッシュ**。`/contributor/{handle}/report` API のレスポンス源。
`usage_events` から Function が定期集計（毎日 / 毎時）。

### パーティションキー
`/handle`

### ドキュメントスキーマ

```yaml
id: "#A1"
handle: "#A1"

# 全期間集計
contributed_skills: 12                  # 貢献したスキル数
public_skills: 8
pending_skills: 4
total_usage_received: 145               # 累積利用回数（直接）
lineage_inheritance: 12.5               # 子スキル経由で受け取ったクレジット
weighted_credit: 178.3                  # クロスチーム加重後の総クレジット

# トップスキル
top_skills:
  - skill_id: "..."
    name: "コードレビュー"
    usage_count: 45
    category: "code_review"

# 月次内訳
monthly_breakdown:
  "2026-05": { usage: 23, new_contributions: 2 }
  "2026-04": { usage: 11, new_contributions: 5 }

# 贈与マイルストーン
milestones_reached:
  - milestone: "first_use"
    skill_id: "..."
    date: "..."
  - milestone: "milestone_10"
    skill_id: "..."
    date: "..."

last_computed_at: "2026-05-25T00:00:00Z"
```

### アクセス制御

- **書き込み**: Function のみ
- **読み取り**: `/contributor/{handle}/report` API 経由
  - ただし API は **「ハンドルを知っている本人」しか問い合わせ不可** という想定
  - Layer 2 では Entra ID 連携で本人確認するのが望ましい（加点要素）

---

## コンテナ 5: `gift_events`

意味的な贈与イベント。「あなたの初めての利用者が現れました」「10回突破しました」など。
通知システムのトリガー、ピッチでの「贈与の文化を生む」を実装する象徴的なコンテナ。

### パーティションキー
`/giver_handle`

### ドキュメントスキーマ

```yaml
id: "gift_uuid"
timestamp: "..."
giver_handle: "#A1"                     # スキル提供者
receiver_handle: "#B3"                  # 利用者（任意・統計目的のみ）
skill_id: "..."
skill_name: "コードレビュー"
gift_kind: "first_use"                  # first_use / milestone_10 / milestone_100 / milestone_1000
                                        # cross_team_first / lineage_first 等の拡張余地

# 通知状態
notified_at: null                       # まだ通知してない
notification_channel: null              # "email" | "teams" | "copilot_studio" 等
acknowledged_at: null                   # 本人が確認した時刻

# メタ
generated_by: "aggregator-function-v1"
```

### TTL

180 日（通知済みかつ確認済みは早期削除しても良い）。

### Function 生成ロジック

`usage_events` への書き込みをトリガーに以下を判定:
- 新スキルへの初めての利用 → `first_use`
- 累積 10/100/1000 到達 → `milestone_*`
- 初めて他チームから使われた → `cross_team_first`

---

## まとめ表

| コンテナ | 主用途 | 書込元 | 読込先 | 機微度 |
|---|---|---|---|---|
| `skills` | 公開スキル | Function | 個人 PC / Copilot | 中（公開前提）|
| `contributor_mappings` | user_id ↔ handle 対応 | Function | Function / 管理者 | **最高（PII）** |
| `usage_events` | 利用ログ | 個人 PC / Function | Function / 管理者 | 高（行動履歴）|
| `contributor_reports` | 個人レポート集計 | Function | 本人 API | 中 |
| `gift_events` | 贈与イベント | Function | 通知システム / 本人 | 中 |

---

## 段階的実装

ハッカソン MVP では `skills` + `usage_events` のみ実装。
他のコンテナは **スキーマだけ用意** して、機能実装は後続段階で。

| 段階 | 実装範囲 |
|---|---|
| **MVP**（必須） | `skills` + `usage_events` + 重複マージロジック |
| **β** | + `contributor_reports` 集計 Function（日次）|
| **γ** | + `gift_events` 生成 Function + 通知メッセージ |
| **完全** | + 系統樹クレジット分配 + クロスチーム加重 |

スキーマは初期から全コンテナ作成しておく（後で migration 不要）。

---

## 設計上の決定事項

### Q1. なぜ user_id 平文を保存しないのか
管理者でも復号できない方が、内部リーク時の被害が小さい。`contributor_mappings.user_id_hash`
は同一人物の同定（複数 push でも同じ handle に集約）に使うだけで、平文は不要。

ただし**個人 PC ローカルの `catalog/.contributors.json`** は user_id ↔ handle を持つ。
これは本人 PC のみに存在するので問題なし。

### Q2. usage_events の TTL
原データは 90 日で消えるが、`contributor_reports` に集計済みなので問題なし。
監査要件で長期保持が必要な場合は `usage_events_archive` 別コンテナへ Function で移送。

### Q3. パーティションキーの選び方
- `skills` → `/category`: クエリの大半が「カテゴリ x 検索」なので分散しやすい
- `usage_events` → `/skill_id`: 集計が skill 単位なのでこれ
- `contributor_reports` → `/handle`: 個人レポート読み出しが handle 単位
- `gift_events` → `/giver_handle`: 通知配信が giver 単位

### Q4. 個人レベル（Layer 1）との対応
個人レベルでは `catalog/skills.json` だけで完結する。Layer 2 を使わない選択肢を残すため、
`SkillCatalog` インターフェースを以下のように共通化:

```python
class SkillCatalogProtocol(Protocol):
    def save(self, skill: ExtractedSkill) -> None: ...
    def get_public(self) -> list[ExtractedSkill]: ...
    def load_all(self) -> list[ExtractedSkill]: ...
    def increment_usage(self, skill_id: str) -> None: ...
    def stats(self) -> dict: ...
```

- `SkillCatalog`（既存）: ローカル JSON
- `CosmosSkillCatalog`（新規）: Cosmos DB read

環境変数 `RENGA_MODE=personal|org` で切り替え。
