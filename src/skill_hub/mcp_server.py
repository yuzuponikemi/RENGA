"""Skill Hub MCP Server

Claude Code から直接スキルカタログを検索・取得できるMCPサーバー。

起動方法:
  uv run python -m src.skill_hub.mcp_server

.mcp.json への登録:
  {
    "mcpServers": {
      "skill-hub": {
        "command": "uv",
        "args": ["run", "python", "-m", "src.skill_hub.mcp_server"],
        "cwd": "/path/to/RENGA"
      }
    }
  }
"""
import sys
import warnings
from mcp.server.fastmcp import FastMCP
from .storage import make_catalog
from .agents.search import EmbeddingSearchIndex

mcp = FastMCP("SkillHub")

_catalog = make_catalog()
_index = EmbeddingSearchIndex()
_skill_map: dict = {}


def _ensure_index() -> None:
    if _index.is_built:
        return
    skills = _catalog.get_public()
    if not skills:
        return
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _index.build(skills)
    _skill_map.update({s.skill_id: s for s in skills})
    print(f"[skill-hub] Index built: {len(skills)} public skills", file=sys.stderr)


@mcp.tool()
def search_skills(query: str, top_k: int = 5) -> str:
    """AIプロンプトスキルをセマンティック検索する。

    やりたいことを自然言語で渡すと、カタログから最も関連するスキルテンプレートを返す。

    Args:
        query: 検索クエリ（例: "コードをレビューしたい", "設計書からコードを生成したい"）
        top_k: 返す件数（デフォルト5）
    """
    _ensure_index()
    if not _index.is_built:
        return "スキルカタログが空です。先にパイプラインを実行してください。"

    ids = _index.search(query, top_k=top_k)
    if not ids:
        return "関連するスキルが見つかりませんでした。"

    lines = [f"## 「{query}」に関連するスキル ({len(ids)}件)\n"]
    for i, sid in enumerate(ids, 1):
        s = _skill_map.get(sid)
        if not s:
            continue
        lines.append(f"### {i}. {s.name}  `{s.skill_id[:8]}`")
        lines.append(f"**カテゴリ**: {s.category}  |  **利用回数**: {s.usage_count}  |  **ソース数**: {s.source_count}")
        lines.append(f"**説明**: {s.description}")
        if s.triggers:
            lines.append(f"**トリガー**: " + " / ".join(f"`{t}`" for t in s.triggers))
        lines.append(f"**テンプレート**:")
        lines.append(f"```")
        lines.append(s.template_prompt)
        lines.append(f"```")
        if s.variables:
            var_descs = [
                f"- `{{{{{v}}}}}`: {s.variable_descriptions.get(v, v)}"
                for v in s.variables
            ]
            lines.append("**変数**:")
            lines.extend(var_descs)
        lines.append("")

    return "\n".join(lines)


@mcp.tool()
def get_skill(skill_id: str) -> str:
    """スキルIDを指定してスキルの詳細（具体的なインスタンス例を含む）を取得する。

    search_skills で見つけたスキルの完全な情報と、実際の使用例を確認できる。

    Args:
        skill_id: スキルID（先頭8文字でも可）
    """
    _ensure_index()

    # 前方一致で検索（先頭8文字指定に対応）
    matched = [s for sid, s in _skill_map.items() if sid.startswith(skill_id)]
    if not matched:
        return f"スキルID `{skill_id}` が見つかりませんでした。search_skills で検索してください。"

    s = matched[0]
    lines = [
        f"# {s.name}",
        f"**ID**: `{s.skill_id}`",
        f"**カテゴリ**: {s.category}",
        f"**説明**: {s.description}",
        f"**ソース数**: {s.source_count}人が類似パターンを使用",
        f"**利用回数**: {s.usage_count}",
        "",
        "## プロンプトテンプレート",
        "```",
        s.template_prompt,
        "```",
        "",
    ]

    if s.variables:
        lines.append("## 変数の説明")
        for v in s.variables:
            desc = s.variable_descriptions.get(v, "")
            lines.append(f"- `{{{{{v}}}}}`: {desc}")
        lines.append("")

    if s.example_use_cases:
        lines.append("## 活用シーン")
        for uc in s.example_use_cases:
            lines.append(f"- {uc}")
        lines.append("")

    if s.instances:
        lines.append("## 具体的な使用例")
        for inst in s.instances:
            lines.append(f"### {inst.name}")
            lines.append("```")
            lines.append(inst.filled_prompt)
            lines.append("```")
            lines.append("")

    return "\n".join(lines)


@mcp.tool()
def list_skill_categories() -> str:
    """スキルカタログのカテゴリ一覧と各カテゴリのスキル数を返す。

    どんな種類のスキルがあるかを把握するのに使う。
    """
    _ensure_index()
    if not _skill_map:
        return "スキルカタログが空です。"

    from collections import Counter
    counts = Counter(s.category for s in _skill_map.values())
    lines = [f"## スキルカテゴリ一覧 (全{len(_skill_map)}スキル)\n"]
    for cat, n in sorted(counts.items(), key=lambda x: -x[1]):
        lines.append(f"- **{cat}**: {n}件")
    return "\n".join(lines)
