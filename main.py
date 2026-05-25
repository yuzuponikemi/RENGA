import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from src.skill_hub.agents.extractor import ExtractorAgent
from src.skill_hub.agents.anonymizer import AnonymizerAgent
from src.skill_hub.contributors import ContributorRegistry
from src.skill_hub.output import skill_to_markdown, save_markdown
from src.skill_hub.mcpify import export_yamls
from src.skill_hub.log_readers import (
    FolderLogReader,
    ClaudeCodeLogReader,
    VSCodeCopilotChatLogReader,
    LogReader,
)
from src.skill_hub.models import CopilotLog
from src.skill_hub.storage.personal import PersonalSkillCatalog

load_dotenv()


class _MultiSourceLogReader(LogReader):
    """複数 LogReader の結果を結合する。"""
    def __init__(self, readers: list[LogReader]):
        self.readers = readers

    def read(self) -> list[CopilotLog]:
        out: list[CopilotLog] = []
        for r in self.readers:
            out.extend(r.read())
        return out


def _build_single_reader(source: str) -> LogReader:
    """単一ソース表記から LogReader を組み立てる。

    Formats:
      claude_code                              → ~/.claude/projects/
      claude_code+/p1:/p2                      → 複数ディレクトリ
      claude_code@<project_filter>             → デフォルトパス + フィルタ
      claude_code+/p1:/p2@<project_filter>     → 複数 + フィルタ
      vscode_copilot                           → OS 既定の workspaceStorage を全走査
      vscode_copilot+/custom/workspaceStorage  → カスタムパス
      vscode_copilot@<workspace_filter>        → ワークスペース名フィルタ
      vscode_copilot+/path@<filter>            → 両方
      /abs/path or ./rel/path or *.json        → FolderLogReader
    """
    source = source.strip()

    def _parse_config(prefix: str) -> tuple[str | None, str | None]:
        """prefix の直後の +path / @filter を切り出す。"""
        rest = source[len(prefix):]
        path = None
        filt = None
        if rest.startswith("+"):
            rest = rest[1:]
            if "@" in rest:
                path, filt = rest.split("@", 1)
            else:
                path = rest
        elif rest.startswith("@"):
            filt = rest[1:]
        return (path or None, filt or None)

    if source.startswith("claude_code"):
        path, filt = _parse_config("claude_code")
        return ClaudeCodeLogReader(
            projects_dir=path or "~/.claude/projects",
            project_filter=filt,
        )
    if source.startswith("vscode_copilot"):
        path, filt = _parse_config("vscode_copilot")
        return VSCodeCopilotChatLogReader(
            workspace_storage_dir=path,
            workspace_filter=filt,
        )
    return FolderLogReader(source)


def build_log_reader():
    """LOG_SOURCE 環境変数からログ入力を組み立てる。

    単一: LOG_SOURCE=claude_code
    複数: LOG_SOURCE=claude_code,vscode_copilot  (カンマ区切り)
    未設定: data/synthetic_logs.json
    """
    raw = os.environ.get("LOG_SOURCE", "").strip()
    if not raw:
        return FolderLogReader(str(Path(__file__).parent / "data" / "synthetic_logs.json"))
    sources = [s for s in (s.strip() for s in raw.split(",")) if s]
    if len(sources) == 1:
        return _build_single_reader(sources[0])
    return _MultiSourceLogReader([_build_single_reader(s) for s in sources])


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
    # main.py runs the extraction pipeline locally — always personal mode.
    # Org-mode population happens via the Azure Function aggregator.
    catalog = PersonalSkillCatalog()
    registry = ContributorRegistry()

    # Step 1: Extract
    print("\n[Step 1] Extracting skill patterns...")
    extractor = ExtractorAgent(client=client, model=deployment, registry=registry)
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
