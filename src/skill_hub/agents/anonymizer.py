import json
from openai import OpenAI
from ..models import ExtractedSkill

ANONYMIZE_PROMPT = """あなたはプロンプトテンプレートの匿名化・一般化の専門家です。

以下のスキルとそのインスタンスを確認し、特定の固有情報が残っていれば抽象的な変数に置き換えてください。

## ルール
- 会社名・組織名 → {{会社名}} や {{顧客企業名}}
- 人物名 → {{担当者名}} や {{上司名}}
- 固有のシステム名・プロジェクト名 → {{システム名}} や {{プロジェクト名}}
- 具体的な数値・日付 → {{数値}} や {{日付}}
- 黒塗りではなく「あなたの〇〇」「指定した〇〇」のように読み手が理解できる形に
- インスタンスの filled_prompt は具体性を残しつつ、個人を特定できる情報のみ除去

## 入力スキル
{skill_json}

## 出力
以下のキーのJSONのみ返してください:
- template_prompt: 匿名化・一般化後のテンプレート
- variables: 更新後の変数名リスト
- variable_descriptions: 各変数の説明（匿名化済み）
- example_use_cases: より汎用的に書き直したシーン例（3つ）
- instances: 各インスタンスの filled_prompt と variable_values を匿名化したもの
  [{{"name": "...", "filled_prompt": "...", "variable_values": {{...}}, "source_prompt": "..."}}]

変更不要な場合も必ず同じ形式で返してください。JSONのみ、コードブロック不要。"""


class AnonymizerAgent:
    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model

    def anonymize(self, skill: ExtractedSkill) -> ExtractedSkill:
        skill_data = {
            "name": skill.name,
            "description": skill.description,
            "template_prompt": skill.template_prompt,
            "variables": skill.variables,
            "variable_descriptions": skill.variable_descriptions,
            "example_use_cases": skill.example_use_cases,
            "instances": [
                {
                    "name": inst.name,
                    "filled_prompt": inst.filled_prompt,
                    "variable_values": inst.variable_values,
                    "source_prompt": inst.source_prompt,
                }
                for inst in skill.instances
            ],
        }
        prompt = ANONYMIZE_PROMPT.format(
            skill_json=json.dumps(skill_data, ensure_ascii=False, indent=2)
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        if not raw:
            return skill.model_copy(update={"anonymized": True})
        data = json.loads(raw)

        from ..models import SkillInstance
        updated_instances = []
        for orig, anon in zip(skill.instances, data.get("instances", [])):
            updated_instances.append(orig.model_copy(update={
                "filled_prompt": anon.get("filled_prompt", orig.filled_prompt),
                "variable_values": anon.get("variable_values", orig.variable_values),
                "source_prompt": anon.get("source_prompt", orig.source_prompt),
            }))

        return skill.model_copy(update={
            "template_prompt": data["template_prompt"],
            "variables": data["variables"],
            "variable_descriptions": data.get("variable_descriptions", skill.variable_descriptions),
            "example_use_cases": data["example_use_cases"],
            "instances": updated_instances if updated_instances else skill.instances,
            "anonymized": True,
        })

    def run(self, skills: list[ExtractedSkill]) -> list[ExtractedSkill]:
        result = []
        for skill in skills:
            print(f"  [Anonymizer] {skill.name}...")
            try:
                anonymized = self.anonymize(skill)
                result.append(anonymized)
            except Exception as e:
                print(f"    ⚠ 匿名化失敗（元スキルを使用）: {e}")
                result.append(skill)
        return result
