from pathlib import Path
import yaml
from .models import ExtractedSkill


def _frontmatter(skill: ExtractedSkill) -> str:
    meta = {
        "name": skill.name,
        "skill_id": skill.skill_id,
        "version": "1.0.0",
        "category": skill.category,
        "status": skill.status.value,
        "source_count": skill.source_count,
        "unique_user_count": skill.unique_user_count,
        "variables": skill.variables,
        "triggers": skill.triggers,
    }
    return "---\n" + yaml.dump(meta, allow_unicode=True, sort_keys=False, default_flow_style=False).rstrip() + "\n---"


def skill_to_markdown(skill: ExtractedSkill) -> str:
    status_badge = "✅ 公開中" if skill.status.value == "public" else "🔒 審査中"

    vars_section = "\n".join(
        f"- `{{{{{v}}}}}`: {skill.variable_descriptions.get(v, '（説明を追記）')}"
        for v in skill.variables
    ) or "*（変数なし）*"

    use_cases_section = "\n".join(f"- {uc}" for uc in skill.example_use_cases)

    triggers_section = ""
    if skill.triggers:
        triggers_section = "\n## トリガーフレーズ\n\n" + "\n".join(
            f"- `{t}`" for t in skill.triggers
        ) + "\n"

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

    body = f"""# {skill.name}

**説明**: {skill.description}
**ステータス**: {status_badge} | **ソース数**: {skill.source_count} 件 | **ユニークユーザー**: {skill.unique_user_count} 人 | **カテゴリ**: {skill.category}

---

## テンプレートプロンプト

```
{skill.template_prompt}
```

## 変数一覧

{vars_section}

## 活用シーン

{use_cases_section}
{triggers_section}
---

## 具体インスタンス

{instances_md}
"""
    return _frontmatter(skill) + "\n\n" + body


def save_markdown(skill: ExtractedSkill, output_dir: str = "output/skills") -> Path:
    safe_name = skill.name.replace("/", "・").replace("\\", "・").replace(":", "：")
    skill_dir = Path(output_dir) / f"{safe_name}_{skill.skill_id[:8]}"
    skill_dir.mkdir(parents=True, exist_ok=True)
    path = skill_dir / "SKILL.md"
    path.write_text(skill_to_markdown(skill), encoding="utf-8")
    return path
