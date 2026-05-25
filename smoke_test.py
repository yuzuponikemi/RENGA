"""E2E smoke test — main.py パイプライン + API 全エンドポイントを検証する。"""
import json
import subprocess
import sys
import time
import httpx
from pathlib import Path

BASE = "http://localhost:8000"
PASS = "✅"
FAIL = "❌"


def check(label: str, ok: bool, detail: str = "") -> bool:
    mark = PASS if ok else FAIL
    print(f"  {mark} {label}" + (f": {detail}" if detail else ""))
    return ok


def run_pipeline() -> bool:
    print("\n[1/3] パイプライン実行 (main.py)...")
    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True, text=True, timeout=300
    )
    ok = result.returncode == 0
    if not ok:
        print(result.stderr[-500:])
    return ok


def check_outputs() -> bool:
    print("\n[2/3] 出力ファイル確認...")
    all_ok = True
    all_ok &= check("catalog/skills.json 存在", Path("catalog/skills.json").exists())
    skills = json.loads(Path("catalog/skills.json").read_text())
    all_ok &= check("スキル数 >= 1", len(skills) >= 1, f"{len(skills)} 件")
    public = [s for s in skills if s["status"] == "public"]
    all_ok &= check("公開スキル >= 1", len(public) >= 1, f"{len(public)} 件")
    md_files = list(Path("output/skills").glob("*/SKILL.md"))
    all_ok &= check("Markdown ファイル生成", len(md_files) >= 1, f"{len(md_files)} 件")
    yaml_files = list(Path("output/copilot_topics").glob("*.yaml"))
    all_ok &= check("Copilot Studio YAML 生成", len(yaml_files) >= 1, f"{len(yaml_files)} 件")
    return all_ok


def check_api() -> bool:
    print("\n[3/3] API エンドポイント確認...")
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api:app", "--port", "8000", "--log-level", "error"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(3)
    all_ok = True
    try:
        r = httpx.get(f"{BASE}/stats", timeout=10)
        all_ok &= check("GET /stats", r.status_code == 200, str(r.json()))

        r = httpx.get(f"{BASE}/skills", timeout=10)
        all_ok &= check("GET /skills", r.status_code == 200, f"{len(r.json())} 件")

        r = httpx.post(f"{BASE}/recommend", json={"query": "メール整理", "user_id": "smoketest"}, timeout=30)
        all_ok &= check("POST /recommend", r.status_code == 200, f"{len(r.json())} 件返答")

        r = httpx.get(f"{BASE}/dashboard", timeout=10)
        all_ok &= check("GET /dashboard (HTML)", r.status_code == 200 and "Skill Hub" in r.text)

        r = httpx.post(f"{BASE}/mcpify", timeout=10)
        all_ok &= check("POST /mcpify", r.status_code == 200)

        r = httpx.get(f"{BASE}/openapi.json", timeout=10)
        all_ok &= check("GET /openapi.json (Copilot Studio 用)", r.status_code == 200)
    finally:
        server.terminate()
    return all_ok


def main() -> None:
    print("=" * 50)
    print("Skill Hub Agent — E2E Smoke Test")
    print("=" * 50)

    results = []
    results.append(run_pipeline())
    results.append(check_outputs())
    results.append(check_api())

    print("\n" + "=" * 50)
    if all(results):
        print(f"{PASS} ALL CHECKS PASSED — デプロイ準備完了")
        sys.exit(0)
    else:
        print(f"{FAIL} SOME CHECKS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
