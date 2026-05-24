import json
from pathlib import Path
from .models import ExtractedSkill, SkillStatus


class SkillCatalog:
    """Local JSON catalog. Cosmos DB 移行時はこのクラスだけ差し替える。"""

    def __init__(self, path: str = "catalog/skills.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load_raw(self) -> list[dict]:
        if not self.path.exists():
            return []
        with open(self.path) as f:
            return json.load(f)

    def save(self, skill: ExtractedSkill) -> None:
        skills = self._load_raw()
        existing_ids = {s["skill_id"] for s in skills}
        if skill.skill_id not in existing_ids:
            skills.append(skill.model_dump())
        else:
            skills = [skill.model_dump() if s["skill_id"] == skill.skill_id else s for s in skills]
        with open(self.path, "w") as f:
            json.dump(skills, f, ensure_ascii=False, indent=2)

    def increment_usage(self, skill_id: str) -> None:
        skills = self._load_raw()
        for s in skills:
            if s["skill_id"] == skill_id:
                s["usage_count"] = s.get("usage_count", 0) + 1
                break
        with open(self.path, "w") as f:
            json.dump(skills, f, ensure_ascii=False, indent=2)

    def add_contributor(self, skill_id: str, handle: str) -> None:
        skills = self._load_raw()
        for s in skills:
            if s["skill_id"] == skill_id:
                handles = s.get("contributor_handles", [])
                if handle not in handles:
                    handles.append(handle)
                s["contributor_handles"] = handles
                break
        with open(self.path, "w") as f:
            json.dump(skills, f, ensure_ascii=False, indent=2)

    def load_all(self) -> list[ExtractedSkill]:
        return [ExtractedSkill(**s) for s in self._load_raw()]

    def get_public(self) -> list[ExtractedSkill]:
        return [s for s in self.load_all() if s.status == SkillStatus.PUBLIC]

    def clear(self) -> None:
        with open(self.path, "w") as f:
            json.dump([], f)

    def stats(self) -> dict:
        all_skills = self.load_all()
        return {
            "total": len(all_skills),
            "public": sum(1 for s in all_skills if s.status == SkillStatus.PUBLIC),
            "pending": sum(1 for s in all_skills if s.status == SkillStatus.PENDING),
            "total_usage": sum(s.usage_count for s in all_skills),
        }
