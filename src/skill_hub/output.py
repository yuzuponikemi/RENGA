from pathlib import Path
from .models import ExtractedSkill


def skill_to_markdown(skill: ExtractedSkill) -> str:
    status_badge = "✅ 公開中" if skill.status.value == "public" else "🔒 審査中"

    # ── Layer 1: 抽象テンプレート ──────────────────────────────────
    vars_section = "\n".join(
        f"- `{{{{{v}}}}}`: {skill.variable_descriptions.get(v, '（説明を追記）')}"
        for v in skill.variables
    )
    use_cases_section = "\n".join(f"- {uc}" for uc in skill.example_use_cases)

    # ── Layer 2: 具体インスタンス ──────────────────────────────────
    instances_md = ""
    if skill.instances:
        parts = []
        for i, inst in enumerate(skill.instances, 1):
            val_lines = "\n".join(
                f"  - `{k}`: {v}" for k, v in inst.variable_values.items()
            )
            source_preview = inst.source_prompt[:120].replace("\n", " ")
            parts.append(
                f"### インスタンス {i}: {inst.name}\n\n"
                f"> 元プロンプト: *{source_preview}*\n\n"
                f"**変数の値**\n{val_lines}\n\n"
                f"**実際のプロンプト**\n```\n{inst.filled_prompt}\n```"
            )
        instances_md = "\n\n---\n\n".join(parts)
    else:
        instances_md = "*（インスタンスなし）*"

    return f"""# 🔷 スキル定義: {skill.name}

**説明**: {skill.description}
**ステータス**: {status_badge} | **ソース数**: {skill.source_count} 件 | **カテゴリ**: {skill.category}

---

## テンプレートプロンプト（抽象）

```
{skill.template_prompt}
```

## 変数一覧

{vars_section}

## 活用シーン

{use_cases_section}

---

# 🔶 具体インスタンス

{instances_md}
"""


def save_markdown(skill: ExtractedSkill, output_dir: str = "output/skills") -> Path:
    dir_path = Path(output_dir)
    dir_path.mkdir(parents=True, exist_ok=True)
    safe_category = skill.category.replace("/", "_").replace("\\", "_").replace(":", "_")
    filename = f"{safe_category}_{skill.skill_id[:8]}.md"
    path = dir_path / filename
    path.write_text(skill_to_markdown(skill), encoding="utf-8")
    return path
