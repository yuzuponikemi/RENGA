"""E2E テスト: 個人スケールから組織スケールまでの一気通貫を検証する。

検証フロー:
  Step 1. 個人モード (Layer 1)
    - PersonalSkillCatalog で catalog/skills.json を読める
    - get_public() がスキルを返す
  Step 2. Cosmos スキーマ確認 (Layer 2 基盤)
    - 5 コンテナがすべて存在する
  Step 3. Aggregator 動作確認 (Layer 2 書き込み)
    - aggregator function_app の _aggregate() を直接呼ぶ
    - Cosmos の skills コンテナにスキルが入る
  Step 4. 組織モード read (Layer 2 読み出し)
    - CosmosSkillCatalog.get_public() でスキルを取得できる
    - increment_usage() で usage_events に append される

使い方:
  export COSMOS_ENDPOINT=...
  export COSMOS_KEY=...
  export RENGA_GITHUB_REPOS=yuzuponikemi/RENGA
  export RENGA_GITHUB_TOKEN=<PAT>
  uv run --extra org python scripts/e2e_test.py
"""
import os
import sys
from pathlib import Path

# プロジェクトルートを sys.path に追加（functions/aggregator から import するため）
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "functions" / "aggregator"))

PASS = "✅"
FAIL = "❌"
SKIP = "⏭️"


def check(label: str, ok: bool, detail: str = "") -> bool:
    mark = PASS if ok else FAIL
    print(f"  {mark} {label}" + (f": {detail}" if detail else ""))
    return ok


def step_personal_mode() -> bool:
    print("\n[Step 1] Layer 1: Personal mode")
    os.environ["RENGA_MODE"] = "personal"
    from src.skill_hub.storage import make_catalog, SkillCatalogProtocol

    cat = make_catalog()
    ok = isinstance(cat, SkillCatalogProtocol)
    if not check("make_catalog() returns SkillCatalogProtocol", ok, type(cat).__name__):
        return False
    public = cat.get_public()
    if not check("get_public() returns skills", len(public) > 0, f"{len(public)} 件"):
        return False
    return True


def step_cosmos_schema() -> bool:
    print("\n[Step 2] Layer 2: Cosmos schema check")
    if not os.environ.get("COSMOS_ENDPOINT") or not os.environ.get("COSMOS_KEY"):
        print(f"  {SKIP} COSMOS_ENDPOINT / COSMOS_KEY 未設定でスキップ")
        return True

    try:
        from azure.cosmos import CosmosClient
    except ImportError:
        print(f"  {SKIP} azure-cosmos 未インストール（uv sync --extra org）")
        return True

    client = CosmosClient(os.environ["COSMOS_ENDPOINT"], os.environ["COSMOS_KEY"])
    db = client.get_database_client(os.environ.get("COSMOS_DB", "skill-hub"))
    expected = ["skills", "contributor_mappings", "usage_events",
                "contributor_reports", "gift_events"]
    all_ok = True
    for name in expected:
        try:
            c = db.get_container_client(name)
            c.read()
            check(f"container '{name}' exists", True)
        except Exception as e:
            all_ok = check(f"container '{name}' exists", False, str(e)[:80])
    return all_ok


def step_aggregate() -> bool:
    print("\n[Step 3] Layer 2: Aggregator dry run")
    if not os.environ.get("COSMOS_ENDPOINT"):
        print(f"  {SKIP} COSMOS_ENDPOINT 未設定でスキップ")
        return True
    if not os.environ.get("RENGA_GITHUB_REPOS") and not os.environ.get("RENGA_LOCAL_CATALOG_PATHS"):
        print(f"  {SKIP} RENGA_GITHUB_REPOS / RENGA_LOCAL_CATALOG_PATHS 未設定でスキップ")
        return True

    # functions/aggregator/core.py から _aggregate を呼ぶ（azure.functions に依存しない）
    try:
        from core import _aggregate
    except ImportError as e:
        return check("import aggregator core", False, str(e))

    result = _aggregate()
    print(f"     result: {result}")
    return check("aggregate() returned status=ok",
                 result.get("status") == "ok",
                 f"merged={result.get('merged')}, inserted={result.get('inserted')}")


def step_org_mode_read() -> bool:
    print("\n[Step 4] Layer 2: Org mode read + usage event")
    if not os.environ.get("COSMOS_ENDPOINT"):
        print(f"  {SKIP} COSMOS_ENDPOINT 未設定でスキップ")
        return True

    os.environ["RENGA_MODE"] = "org"
    # キャッシュリセット（factory は import-time に評価しないので OK）
    from src.skill_hub.storage import make_catalog

    try:
        cat = make_catalog()
    except RuntimeError as e:
        return check("CosmosSkillCatalog instantiated", False, str(e))

    public = cat.get_public()
    if not check("get_public() from Cosmos", len(public) > 0, f"{len(public)} 件"):
        return False

    # usage_events への append
    target = public[0]
    try:
        cat.increment_usage(target.skill_id)
        check(f"increment_usage('{target.skill_id[:8]}...') succeeded", True)
    except Exception as e:
        return check("increment_usage", False, str(e))
    return True


def main() -> None:
    print("=" * 60)
    print("Skill Hub — E2E Test (Layer 1 → Layer 2)")
    print("=" * 60)

    results = [
        step_personal_mode(),
        step_cosmos_schema(),
        step_aggregate(),
        step_org_mode_read(),
    ]

    print("\n" + "=" * 60)
    if all(results):
        print(f"{PASS} ALL CHECKS PASSED")
        sys.exit(0)
    else:
        print(f"{FAIL} SOME CHECKS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
