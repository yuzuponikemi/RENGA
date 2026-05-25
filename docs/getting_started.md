# 始め方 — 別 PC からスキルを登録する

このドキュメントは、**新しい PC や別の開発者として Skill Hub Agent に参加** する手順を説明します。すでに 1 つの PC で動かしている本人が「複数 PC で同じ自分として参加」したい場合と、「別の人として参加」したい場合の両方をカバーします。

## 全体像

```
あなたの PC
  ├─ Claude Code or VSCode Copilot Chat のログを溜める
  └─ uv run python main.py
        ↓ HDBSCAN + LLM 抽出 + 匿名化
        catalog/skills.json + output/skills/*/SKILL.md を生成
        ↓ CATALOG_PUSH=true
        個人 GitHub repo に push
              ↓
        Azure Function (skill-hub-api) が毎時 fetch
              ↓ content_hash でマージ
        Cosmos DB に集約 (handle のみ、匿名)
```

---

## 前提

### ハード／OS
- macOS / Linux / Windows いずれか
- Python 3.11 以上

### 必須ツール
- `git`
- `uv`（Python パッケージマネージャ）
    - インストール: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - Windows: <https://docs.astral.sh/uv/#installation>

### 用意するもの
- **Azure AI Foundry の endpoint + API key**（LLM 推論に必須）
- **ログソース**: 以下の少なくとも 1 つ
    - Claude Code（`~/.claude/projects/` にセッションログがあれば OK）
    - VSCode + GitHub Copilot Chat 拡張（チャット履歴があれば OK）
    - 既存の合成 JSON（`data/synthetic_logs.json` 同形式）
- **GitHub アカウント**（カタログを push したい場合）
- **Cosmos DB 接続情報**（組織モードで Cosmos を直接読みたい場合のみ。書き込みは Azure Function 経由なので不要）

---

## ステップ 1: リポジトリを取得

```bash
git clone https://github.com/yuzuponikemi/RENGA.git
cd RENGA
```

組織で運用する場合は管理者から **専用の private fork** を案内されるはずなので、それを clone してください。fork に push したスキルだけが Azure Function の集約対象になります。

---

## ステップ 2: 依存をインストール

**個人モード（ローカル完結・Cosmos 不要）:**
```bash
uv sync
```

**組織モード（Cosmos からスキルを read したい）:**
```bash
uv sync --extra org
```

初回は `sentence-transformers` のモデルダウンロードに 2〜3 分かかります（500 MB 程度）。

---

## ステップ 3: `.env` を作成

```bash
cp .env.example .env
```

`.env` を開いて、最低限以下を埋めます:

```bash
# 必須: Azure AI Foundry の LLM
AZURE_FOUNDRY_ENDPOINT=https://<resource>.openai.azure.com/openai/v1
AZURE_FOUNDRY_API_KEY=<Foundry の API キー>
AZURE_FOUNDRY_DEPLOYMENT=DeepSeek-V4-Flash
```

組織モードを使う場合はさらに:

```bash
RENGA_MODE=org
COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
COSMOS_KEY=<読み取り権限のキー推奨>
COSMOS_DB=skill-hub
USER_HANDLE=#A1
```

---

## ステップ 4: 自分が誰かを決める（USER_ID）

これが **「別 PC を別人として登録するか、同じ人として登録するか」の分岐点** です。

### 自動解決ロジック（優先順位）

1. `.env` の `USER_ID` 環境変数
2. `git config user.email` の SHA-256 先頭 8 桁
3. Claude Code セッション ID の先頭 8 桁（後方互換、推奨しない）

### ケース別の設定

| シナリオ | 設定 | 結果 |
|---|---|---|
| **同じ人が複数 PC で使う**（推奨）| 何もしない（`USER_ID` 未設定）| 全 PC の git email が同じなら自動的に **同一人物扱い** |
| **別人として登録**（k=3 ゲート検証など）| `.env` に `USER_ID=alice` のような明示値 | **別の handle が発行される** |
| **組織展開で社員固定 ID** | `.env` に `USER_ID=社員番号` など | 全社員の handle が安定 |

> 💡 k=3 ゲート（3 人の異なる人間が同じパターンを共有したら自動 PUBLIC 化）を試したい場合は、**別 PC で別の `USER_ID` を明示**してください。同じ git email のままだとフォールバックゲート（1 人 + 3 プロンプト以上）でしか PUBLIC 化されません。

---

## ステップ 5: ログソースを選ぶ

`.env` の `LOG_SOURCE` を設定:

```bash
# 単一ソース
LOG_SOURCE=claude_code                     # Claude Code セッション全件
LOG_SOURCE=vscode_copilot                  # VSCode の GitHub Copilot Chat 全件

# フィルタ
LOG_SOURCE=claude_code@RENGA               # プロジェクト名にRENGAを含むものだけ
LOG_SOURCE=vscode_copilot@infoseeker       # ワークスペース名にinfoseekerを含むものだけ

# パス指定
LOG_SOURCE=claude_code+/custom/path        # カスタムディレクトリ
LOG_SOURCE=vscode_copilot+/path/to/Code/User/workspaceStorage

# マルチソース（カンマ区切り）
LOG_SOURCE=claude_code,vscode_copilot

# 未設定 → data/synthetic_logs.json を使う（動作確認用）
```

### VSCode Copilot Chat のログがどこにあるか

- **macOS**: `~/Library/Application Support/Code/User/workspaceStorage/`
- **Linux**: `~/.config/Code/User/workspaceStorage/`
- **Windows**: `%APPDATA%\Code\User\workspaceStorage\`

各ワークスペース配下の `chatSessions/*.json` が読まれます。**会社で VSCode の Copilot Chat を使っているなら、それが既にスキル抽出の素材になります**。

---

## ステップ 6: パイプラインを実行

```bash
uv run python main.py
```

ログ量に応じて 1〜10 分。出力:

- `catalog/skills.json` — スキル本体（JSON）
- `output/skills/<スキル名>_<id8>/SKILL.md` — gstack 形式ドキュメント
- `output/copilot_topics/*.yaml` — Copilot Studio インポート用 YAML

### よくある実行オプション

| 環境変数 | 効果 |
|---|---|
| `KEEP_CATALOG=true` | 既存スキルを保持して追加（既定は毎回 clear）|
| `CATALOG_PUSH=true` | 実行後に GitHub に自動 push |
| `CLUSTER_STRATEGY=step2` | クラスタリング戦略の切替（既定 step2 で十分）|

---

## ステップ 7: GitHub に push（組織連携する場合）

```bash
CATALOG_PUSH=true uv run python main.py
```

または `.env` に `CATALOG_PUSH=true` を入れて常時 push。

push 先の repo は **必ず private** にしてください。public だと匿名性が崩れます（git commit author が見えるため）。

### 別 repo に push したい

`.env` で `CATALOG_REMOTE_DIR=/path/to/separate/repo` を指定すると、その別 repo の `catalog/` 配下に書き込んで push します。

---

## ステップ 8: Cosmos への集約を確認

組織モードで Function App が稼働している場合:

```bash
# 手動トリガー（Timer は毎時 0 分に自動実行）
curl -X POST https://skill-hub-api-ayafcsgedugba8eh.canadacentral-01.azurewebsites.net/api/aggregate
```

結果:
```json
{"status":"ok","sources":1,"fetched":N,"merged":M,"inserted":K,"errors":0}
```

- `merged`: 既存スキルと content_hash 一致 → 貢献者 handle が追記される
- `inserted`: 新規スキルとして登録
- `errors`: 解析エラー（通常 0）

### k=3 ゲートが Cosmos 側で発火する瞬間

別 PC（別 `USER_ID`）から同じ意味のプロンプトが集まり、`contributor_handles` の長さが 3 以上になると、Function 側の `_merge` ロジックが自動的に `status` を `public` に昇格させます。

---

## ステップ 9: 自分の貢献を確認

```bash
# 自分のハンドル（USER_HANDLE）を知っている本人だけが叩ける
curl "https://skill-hub-api-.../api/contributor/%23A1/report"
```

> `#` は URL エンコードで `%23`

レスポンス:
```json
{
  "handle": "#A1",
  "found": true,
  "contributed_skills": 12,
  "public_skills": 8,
  "total_usage": 145,
  "top_skills": [...]
}
```

API URL は組織管理者から共有されたものを使ってください。

---

## ステップ 10: Claude Code から MCP 経由で呼ぶ

ローカル MCP サーバを `.mcp.json` に登録すれば、Claude Code が直接スキルを検索できます。`RENGA` 配下に `.mcp.json` が同梱されているので、Claude Code を再起動するだけで以下のツールが使えるようになります:

- `search_skills(query, top_k)` — 自然言語でスキル検索
- `get_skill(skill_id)` — スキル詳細取得
- `list_skill_categories()` — カテゴリ一覧

組織モードに切り替えると Cosmos 全件から検索されます:

```bash
RENGA_MODE=org uv run python -m src.skill_hub
```

---

## よくあるトラブル

### LLM が JSON を返さず `JSONDecodeError`
- LLM の応答キャパシティ問題。`main.py` 内のエラー件数が増えるだけで他は動きます
- 別の deployment（gpt-4o など）に切り替えると改善することが多い

### k=3 ゲートが発火しない
- 1 人で動かしている限り、フォールバック（同一人物 + 3 プロンプト以上）でしか PUBLIC 化しません
- 別 PC で `USER_ID=alice` を明示し、別人としてログを溜めれば k=3 が発火します
- 検証目的なら `K_THRESHOLD` 環境変数を 2 にして試すのもアリ

### `sentence-transformers` のモデル DL が遅い
- 初回だけ 500 MB ダウンロード。`HF_TOKEN` を設定するとレート制限が緩和されます
- 一度落としたモデルは `~/.cache/huggingface/` にキャッシュされ、以降は不要

### GitHub push が失敗する
- `git remote -v` で push 先が自分の write 権限を持つ repo か確認
- private repo に push する場合、`gh auth login` か HTTPS の credential helper が必要

### VSCode Copilot Chat のログが見つからない
- VSCode を 1 度でも開いて Copilot Chat を起動したことがあるか確認
- `ls "~/Library/Application Support/Code/User/workspaceStorage/" | head` で workspace hash が見えるか
- 拡張機能 `GitHub.copilot-chat` が有効か

---

## 別 PC から登録するときの最短ハッピーパス

```bash
# 新 PC で
git clone <your-fork-url> RENGA
cd RENGA
uv sync

cp .env.example .env
# .env を編集（最低限）:
#   AZURE_FOUNDRY_ENDPOINT, AZURE_FOUNDRY_API_KEY を埋める
#   USER_ID=bob  ← 別人として登録したいなら明示
#   LOG_SOURCE=claude_code,vscode_copilot  ← 両方使うなら
#   CATALOG_PUSH=true                       ← GitHub 経由で組織反映するなら

uv run python main.py

# 組織連携を即時反映したい場合:
curl -X POST https://skill-hub-api-ayafcsgedugba8eh.canadacentral-01.azurewebsites.net/api/aggregate
```

これで新 PC から `bob` というハンドルで貢献が記録されます。同じパターンを `alice` (自分の元 PC) と `bob` (新 PC) の両方から登録すれば、k=3 までもう 1 人で PUBLIC 昇格が発火します。

---

## さらに知りたいなら

- 全体アーキテクチャ: [`docs/architecture.md`](architecture.md)
- Cosmos スキーマ詳細: [`docs/db_schema.md`](db_schema.md)
- 設計思想（なぜ匿名にしたか）: [Homupe の提出記事](https://homupe.pages.dev/blog/2026/05/25/skill-hub-agent--個人スケールから組織スケールへagentic-に育つスキル循環インフラ/)
