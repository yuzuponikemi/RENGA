"""Auto-MCPify: 抽出スキル → Copilot Studio トピック YAML を自動生成する。"""
import yaml
from pathlib import Path
from .models import ExtractedSkill


def skill_to_copilot_yaml(skill: ExtractedSkill) -> dict:
    """Copilot Studio Power Virtual Agents トピック形式に変換する。"""
    trigger_phrases = [skill.description] + skill.example_use_cases[:2]

    actions = []
    for var in skill.variables:
        actions.append({
            "kind": "Question",
            "id": f"ask_{var}",
            "prompt": f"{var}を入力してください",
            "variable": f"Topic.{var}",
        })

    filled_prompt = skill.template_prompt
    for var in skill.variables:
        filled_prompt = filled_prompt.replace(f"{{{var}}}", f"{{{{Topic.{var}}}}}")

    actions.append({
        "kind": "SendMessage",
        "id": "send_result",
        "message": f"以下のプロンプトをCopilotに貼り付けてください：\n\n{filled_prompt}",
    })

    return {
        "kind": "AdaptiveDialog",
        "id": f"skill_{skill.skill_id[:8]}",
        "name": skill.name,
        "description": skill.description,
        "triggerPhrases": trigger_phrases,
        "actions": actions,
        "metadata": {
            "source_count": skill.source_count,
            "category": skill.category,
            "generated_by": "skill-hub-agent",
        },
    }


def export_yamls(skills: list[ExtractedSkill], output_dir: str = "output/copilot_topics") -> list[Path]:
    dir_path = Path(output_dir)
    dir_path.mkdir(parents=True, exist_ok=True)
    paths = []
    for skill in skills:
        data = skill_to_copilot_yaml(skill)
        safe_category = skill.category.replace("/", "_").replace("\\", "_").replace(":", "_")
        filename = f"{safe_category}_{skill.skill_id[:8]}.yaml"
        path = dir_path / filename
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        paths.append(path)
    return paths
