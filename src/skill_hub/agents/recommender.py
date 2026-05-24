import json
from openai import OpenAI
from ..catalog import SkillCatalog
from ..models import ExtractedSkill
from .search import EmbeddingSearchIndex

RECOMMEND_PROMPT = """あなたはAIスキルの推薦エンジンです。

ユーザーが「{user_query}」と聞いています。
以下の候補スキルから、最も適切なスキルを最大3件選んで推薦してください。

候補スキル:
{catalog_json}

出力はJSON配列で、各要素に以下を含めてください:
- skill_id: スキルのID
- name: スキル名
- reason: このスキルを推薦する理由（1文）
- adapted_prompt: ユーザーの状況に合わせてカスタマイズしたプロンプト例

関連するスキルがなければ空配列を返してください。JSONのみ、コードブロック不要。"""

_TOP_K = 8


class RecommenderAgent:
    def __init__(self, client: OpenAI, model: str, catalog: SkillCatalog,
                 index: EmbeddingSearchIndex | None = None):
        self.client = client
        self.model = model
        self.catalog = catalog
        self._index = index

    def _get_index(self, public_skills: list[ExtractedSkill]) -> EmbeddingSearchIndex:
        if self._index is not None and self._index.is_built:
            return self._index
        idx = EmbeddingSearchIndex()
        idx.build(public_skills)
        return idx

    def recommend(self, user_query: str) -> list[dict]:
        public_skills = self.catalog.get_public()
        if not public_skills:
            return []

        skill_map = {s.skill_id: s for s in public_skills}
        index = self._get_index(public_skills)
        top_ids = index.search(user_query, top_k=_TOP_K)
        candidates = [skill_map[sid] for sid in top_ids if sid in skill_map]

        catalog_data = [
            {
                "skill_id": s.skill_id,
                "name": s.name,
                "description": s.description,
                "template_prompt": s.template_prompt,
                "example_use_cases": s.example_use_cases,
            }
            for s in candidates
        ]
        prompt = RECOMMEND_PROMPT.format(
            user_query=user_query,
            catalog_json=json.dumps(catalog_data, ensure_ascii=False, indent=2),
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        return json.loads(raw)
