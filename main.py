import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from src.skill_hub.agents.extractor import ExtractorAgent
from src.skill_hub.agents.anonymizer import AnonymizerAgent
from src.skill_hub.catalog import SkillCatalog
from src.skill_hub.output import skill_to_markdown, save_markdown
from src.skill_hub.mcpify import export_yamls
from src.skill_hub.log_readers import FolderLogReader, ClaudeCodeLogReader

load_dotenv()


def build_log_reader():
    """LOG_SOURCE 環境変数でログ入力を切り替える。

    LOG_SOURCE=claude_code                   → ~/.claude/projects/ を全走査
    LOG_SOURCE=claude_code+/p1:/p2           → 複数ディレクトリ（+区切り）
    LOG_SOURCE=claude_code+/p1:/p2@myproj   → プロジェクトフィルタ付き
    LOG_SOURCE=<path>                        → JSON ファイルまたはフォルダ
    未設定                                   → data/synthetic_logs.json
    """
    source = os.environ.get("LOG_SOURCE", "")
    if source.startswith("claude_code"):
        rest = source[len("claude_code"):]
        project_filter = None
        dirs = "~/.claude/projects"
        if rest.startswith("+"):
            rest = rest[1:]
            if "@" in rest:
                dirs, project_filter = rest.split("@", 1)
            else:
                dirs = rest
        return ClaudeCodeLogReader(projects_dir=dirs, project_filter=project_filter)
    elif source:
        return FolderLogReader(source)
    else:
        return FolderLogReader(str(Path(__file__).parent / "data" / "synthetic_logs.json"))


def build_client() -> tuple[OpenAI, str]:
    endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT")
    api_key = os.environ.get("AZURE_FOUNDRY_API_KEY")
    deployment = os.environ.get("AZURE_FOUNDRY_DEPLOYMENT", "DeepSeek-V4-Flash")

    if not endpoint or not api_key:
        print("Error: AZURE_FOUNDRY_ENDPOINT and AZURE_FOUNDRY_API_KEY must be set in .env", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(base_url=endpoint, api_key=api_key)
    return client, deployment


def push_catalog() -> None:
    """catalog/ と output/skills/ を GitHub に push する。
    CATALOG_PUSH=true のときだけ実行。
    CATALOG_REMOTE_DIR が設定されている場合はそのディレクトリで git 操作する（別リポジトリ運用）。
    """
    repo_dir = os.environ.get("CATALOG_REMOTE_DIR", str(Path(__file__).parent))
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "catalog/", "output/skills/"],
            cwd=repo_dir, capture_output=True, text=True
        )
        if not result.stdout.strip():
            print("  [GitHub] 変更なし、push をスキップ")
            return

        subprocess.run(["git", "add", "catalog/skills.json", "output/skills/"],
                       cwd=repo_dir, check=True)
        subprocess.run(
            ["git", "commit", "-m", "skill-hub: update catalog"],
            cwd=repo_dir, check=True
        )
        subprocess.run(["git", "push"], cwd=repo_dir, check=True)
        print("  [GitHub] catalog pushed ✓")
    except subprocess.CalledProcessError as e:
        print(f"  [GitHub] push 失敗: {e}", file=sys.stderr)


def main() -> None:
    reader = build_log_reader()
    source_label = os.environ.get("LOG_SOURCE", "synthetic")
    print(f"Log source: {source_label}")
    logs = reader.read()
    print(f"Loaded {len(logs)} logs")

    client, deployment = build_client()
    catalog = SkillCatalog()

    # Step 1: Extract
    print("\n[Step 1] Extracting skill patterns...")
    extractor = ExtractorAgent(client=client, model=deployment)
    raw_skills = extractor.run(logs)
    print(f"  → {len(raw_skills)} skill(s) extracted")

    # Step 2: Anonymize
    print("\n[Step 2] Anonymizing...")
    anonymizer = AnonymizerAgent(client=client, model=deployment)
    skills = anonymizer.run(raw_skills)

    # Step 3: k=3 gate + save to catalog
    print("\n[Step 3] k=3 gate + saving to catalog...")
    if not os.environ.get("KEEP_CATALOG"):
        catalog.clear()
        print("  [Catalog] cleared (set KEEP_CATALOG=true to retain previous skills)")
    public_count = 0
    for skill in skills:
        catalog.save(skill)
        md_path = save_markdown(skill)
        status = "✅ PUBLIC" if skill.status.value == "public" else "🔒 PENDING"
        print(f"  {status} [{skill.category}] {skill.name} → {md_path}")
        if skill.status.value == "public":
            public_count += 1

    # Step 4: Auto-MCPify → Copilot Studio YAML
    print("\n[Step 4] Auto-MCPify: Copilot Studio YAML 生成...")
    public_skills = catalog.get_public()
    yaml_paths = export_yamls(public_skills)
    for p in yaml_paths:
        print(f"  📄 {p}")

    # Step 5: GitHub に push（CATALOG_PUSH=true のとき）
    if os.environ.get("CATALOG_PUSH"):
        print("\n[Step 5] Pushing catalog to GitHub...")
        push_catalog()

    # Summary
    stats = catalog.stats()
    print(f"\n{'='*50}")
    print(f"Catalog stats: {stats['total']} total / {stats['public']} public / {stats['pending']} pending")
    print(f"Output: output/skills/")
    if skills:
        print(f"\n--- Sample output ---")
        print(skill_to_markdown(skills[0]))


if __name__ == "__main__":
    main()
