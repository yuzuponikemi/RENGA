"""3分デモ CLI — ハッカソン審査員向けターミナルデモ。
設計書のデモシナリオ (Section 10) に沿って進行する。
"""
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PURPLE = "\033[95m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def wait(msg: str = "", secs: float = 0.8) -> None:
    if msg:
        print(msg)
    time.sleep(secs)


def section(title: str) -> None:
    print(f"\n{BOLD}{PURPLE}{'─'*55}{RESET}")
    print(f"{BOLD}{PURPLE}  {title}{RESET}")
    print(f"{BOLD}{PURPLE}{'─'*55}{RESET}\n")


def step(text: str) -> None:
    print(f"{CYAN}▶ {text}{RESET}")


def result(text: str) -> None:
    print(f"{GREEN}{text}{RESET}")


def highlight(text: str) -> None:
    print(f"{YELLOW}{BOLD}{text}{RESET}")


def main() -> None:
    print(f"\n{BOLD}Skill Hub Agent — 3分デモ{RESET}")
    print("Press Enter to advance each step.\n")
    input("  → スタート [Enter]")

    # ── Scene 1: 問題提起 (0:00-0:20) ─────────────────────────────────
    section("Scene 1: 同じAIがあるのに、なぜ差がつくのか？")
    step("社員 A: Copilot を使いこなして1時間の仕事を10分で完了")
    step("社員 B: 同じ Copilot を持っているが、うまく使えず1時間かかる")
    wait()
    highlight("  → ノウハウが個人の中に隠れている。組織のAI ROI が頭打ちに。")
    input("\n  [Enter] →")

    # ── Scene 2: ログ観察 (0:20-0:50) ─────────────────────────────────
    section("Scene 2: エージェントが利用ログを観察する")
    step("合成 Copilot ログ 20件を読み込み...")
    logs_path = Path("data/synthetic_logs.json")
    logs = json.loads(logs_path.read_text())
    success = [l for l in logs if l["accepted"] and l["follow_up_count"] <= 1]
    print(f"  総ログ: {len(logs)} 件 / 成功シグナル: {len(success)} 件")
    wait(secs=1)

    from collections import Counter
    cats = Counter(l["task_category"] for l in success)
    step("カテゴリ別クラスタ検出:")
    for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
        bar = "█" * n
        mark = f"{GREEN}✓ k≥3{RESET}" if n >= 3 else f"{YELLOW}pending{RESET}"
        print(f"  {bar} {cat}: {n}件  {mark}")
    input("\n  [Enter] →")

    # ── Scene 3: スキル抽出 (0:50-1:30) ───────────────────────────────
    section("Scene 3: 3パターン → 1スキルへ自動抽出・匿名化")
    from src.skill_hub.catalog import SkillCatalog
    catalog = SkillCatalog()
    public = catalog.get_public()

    if not public:
        print("  (カタログが空です。先に python main.py を実行してください)")
        sys.exit(1)

    skill = next((s for s in public if "email" in s.category), public[0])
    step(f"抽出されたスキル: 「{skill.name}」")
    print(f"  ソース: {skill.source_count} 件の成功ログから")
    print(f"  ステータス: {GREEN}PUBLIC{RESET} (k={skill.source_count} ≥ 3 ✓)")
    wait(secs=0.5)
    step("匿名化テンプレート:")
    print(f"\n  {CYAN}{skill.template_prompt}{RESET}")
    print(f"\n  変数: {', '.join(f'{{{{{v}}}}}' for v in skill.variables)}")
    wait(secs=0.5)
    highlight("  → 貢献者は匿名のまま。「誰が作ったか」は内部にのみ記録。")
    input("\n  [Enter] →")

    # ── Scene 4: 推薦 (1:30-2:10) ─────────────────────────────────────
    section("Scene 4: 別のユーザーがスキルを発見する")
    query = "メールの整理をしたい"
    step(f"ユーザー B の入力: 「{query}」")
    wait(secs=0.5)

    endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT")
    api_key  = os.environ.get("AZURE_FOUNDRY_API_KEY")
    deployment = os.environ.get("AZURE_FOUNDRY_DEPLOYMENT", "DeepSeek-V4-Flash")

    if endpoint and api_key:
        from src.skill_hub.agents.recommender import RecommenderAgent
        client = OpenAI(base_url=endpoint, api_key=api_key)
        agent = RecommenderAgent(client=client, model=deployment, catalog=catalog)
        print("  (推薦エンジン実行中...)", end="", flush=True)
        recs = agent.recommend(query)
        print(" 完了")
        if recs:
            r = recs[0]
            result(f"\n  💡 「{r['name']}」— {r['reason']}")
            print(f"\n  使用プロンプト例:\n  {CYAN}{r['adapted_prompt']}{RESET}")
            catalog.increment_usage(r["skill_id"])
    else:
        result(f"\n  💡 「{skill.name}」")
        result(f"  3人の同僚が同じ問題を解決しています。このスキルを使いますか？")

    highlight("\n  → ユーザー B は1クリックでノウハウを得た。")
    input("\n  [Enter] →")

    # ── Scene 5: ダッシュボード (2:10-2:40) ───────────────────────────
    section("Scene 5: 匿名コントリビューションダッシュボード")
    step("コントリビューター #A1 への通知（月次）:")
    stats = catalog.stats()
    print(f"""
  ┌─────────────────────────────────────┐
  │  🔮 Skill Hub — あなたの貢献レポート  │
  ├─────────────────────────────────────┤
  │  あなたのスキルが利用されました        │
  │  利用回数:  {stats['total_usage']:>3} 回                  │
  │  公開スキル: {stats['public']:>3} 件                  │
  │  あなたの識別子: #A1 (内部のみ)      │
  └─────────────────────────────────────┘""")
    highlight("\n  → 本人には記録される。外からは #A1 しか見えない。")
    input("\n  [Enter] →")

    # ── Scene 6: アーキテクチャ (2:40-3:00) ───────────────────────────
    section("Scene 6: アーキテクチャ")
    print("""
  [Copilot Logs]
       │
       ▼
  ① Extractor Agent  ──→  成功パターン抽出 (k≥3)
       │
       ▼
  ② Anonymizer Agent ──→  固有名詞 → {{変数}}
       │
       ▼
  [Cosmos DB]  ←─→  Azure AI Search
       │
  ③ Recommender Agent ──→  Copilot Studio UI
       │
  Auto-MCPify ─────────→  トピック YAML 自動生成
    """)
    highlight("「個人の善意を、AIが代わりに可視化する。」")
    highlight("「贈与の負担を解除しながら、贈与の文化を生む。」")
    print(f"\n{GREEN}{BOLD}  ── デモ終了 (約3分) ──{RESET}\n")


if __name__ == "__main__":
    main()
