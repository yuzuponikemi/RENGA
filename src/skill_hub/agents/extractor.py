import json
import os
import re
from openai import OpenAI
from ..models import CopilotLog, ExtractedSkill, SkillInstance, SkillStatus
from .clustering import EmbeddingClusterer

K_THRESHOLD = 3          # PUBLIC になるために必要なユニークユーザー数
K_PROMPT_THRESHOLD = 3   # ユーザー数が揃わない場合のフォールバック（プロンプト数）

# ────────────────────────────────────────────────────────────────
# Step 1: タスク型プロンプト判定
# 「〜して」「〜を作って」のような命令形はタスク。
# 「なぜ」「どう思う」「説明して」のような議論・質問は除外。
# ────────────────────────────────────────────────────────────────
_TASK_VERBS = re.compile(
    r"(して|してください|作って|作成して|変換して|整理して|まとめて|抽出して|修正して|"
    r"書いて|生成して|翻訳して|要約して|分析して|チェックして|レビューして|調査して|"
    r"実装して|追加して|削除して|更新して|保存して|実行して|確認して|教えて|説明して|"
    r"summarize|extract|write|create|convert|translate|fix|review|generate|analyze|"
    r"explore|investigate|implement|add|delete|update|save|run|execute|check|explain|"
    r"search|find|list|show|display|build|deploy|test|refactor|migrate|install)",
    re.IGNORECASE,
)
_DISCUSSION_PATTERNS = re.compile(
    r"^(なぜ|どう|どのよう|なに|何が|何を|どちら|いつ|誰が|"
    r"why|what|how|which|when|who|is |are |can |could |should |do you|think)",
    re.IGNORECASE,
)


def is_task_prompt(text: str) -> bool:
    if _DISCUSSION_PATTERNS.search(text.strip()):
        return False
    return bool(_TASK_VERBS.search(text))


# ────────────────────────────────────────────────────────────────
# Step 2a: 埋め込みベースクラスタリング（決定論的）
# TF-IDF char n-gram → TruncatedSVD → HDBSCAN
# k は自動検出。LLM はクラスタの「命名」だけを担当する。
# ────────────────────────────────────────────────────────────────

# Step 2b: クラスタ命名（LLM はここだけ関与）
NAME_PROMPT = """以下のプロンプト群は同じ作業パターンのものです。
このグループを表す「作業の本質的な名前」を日本語15文字以内で付けてください。

プロンプト例（先頭3件）:
{samples_json}

出力はJSON:
{{"task_type": "名前（15文字以内）", "description": "共通する作業構造（1文）"}}
JSONのみ、コードブロック不要。"""


# ────────────────────────────────────────────────────────────────
# Step 3: クラスタからスキルテンプレートを抽出
# ────────────────────────────────────────────────────────────────
EXTRACTION_PROMPT = """あなたはAI利用ログからスキルテンプレートを抽出する専門家です。

以下は同じ種類の作業をした複数のユーザーのプロンプトです。

作業タイプ: {task_type}
プロンプト群:
{prompts_json}

## タスク1: 抽象テンプレート（スキル定義）を作成
固有名詞・ファイル名・会社名などを {{変数名}} に抽象化して、誰でも再利用できる汎用テンプレートを作ってください。

## タスク2: 具体インスタンスを生成
上記プロンプト群から代表的なもの2〜3件を選び、テンプレートの {{変数名}} を実際の値で埋めた具体例を作ってください。
インスタンスは「このスキルを使ってみたい人がすぐコピペして使える」レベルの具体性にしてください。

出力はJSON形式:
- name: スキルの短い名前（日本語、20文字以内）
- description: スキルの説明（何をするスキルか、50文字以内）
- template_prompt: 汎用プロンプトテンプレート（{{変数名}} 形式）
- variables: テンプレート内の変数名リスト
- variable_descriptions: 各変数の説明と具体例 {{"変数名": "何を書くか（例: 〇〇）"}}
- example_use_cases: 活用シーン例（3つ）
- instances: 具体インスタンスのリスト（2〜3件）
  [{{"name": "このインスタンスの短い名前（15文字以内）",
    "filled_prompt": "{{変数名}} をすべて実際の値に置き換えたプロンプト全文",
    "variable_values": {{"変数名": "実際に埋めた値"}},
    "source_prompt": "元のユーザープロンプト（先頭150文字）"
  }}]

JSONのみ、コードブロック不要。"""


def _strip_fences(text: str) -> str:
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()


class ExtractorAgent:
    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model

    # ── public API ──────────────────────────────────────────────

    def run(self, logs: list[CopilotLog], min_cluster_size: int = K_THRESHOLD) -> list[ExtractedSkill]:
        # 1. タスク型に絞る
        task_logs = self._filter_task_logs(logs)
        print(f"  [Filter] {len(logs)} → {len(task_logs)} task-type logs")

        if len(task_logs) < min_cluster_size:
            print("  [Filter] タスク型ログが少なすぎます（k=3 未満）")
            return []

        # 2. 埋め込みベースでクラスタを自動検出（決定論的）
        texts = [log.prompt for log in task_logs]
        strategy = os.environ.get("CLUSTER_STRATEGY", "step2")
        clusterer = EmbeddingClusterer(min_cluster_size=min_cluster_size, strategy=strategy)
        labels = clusterer.fit(texts)

        # label=-1 はノイズ（どのクラスタにも属さない）
        unique_labels = sorted(set(l for l in labels if l >= 0))
        print(f"  [Cluster] {len(unique_labels)} cluster(s) found (noise: {labels.count(-1)})")

        # 3. クラスタごとにLLMで命名 → スキル抽出
        skills = []
        for label in unique_labels:
            indices = [i for i, l in enumerate(labels) if l == label]
            cluster_logs = [task_logs[i] for i in indices]
            if len(cluster_logs) < min_cluster_size:
                continue

            try:
                task_type, description = self._name_cluster(cluster_logs)
            except Exception as e:
                print(f"    ⚠ クラスタ命名失敗: {e}")
                task_type, description = f"クラスタ{label}", ""

            unique_u = len({l.user_id for l in cluster_logs})
            print(f"  [Extractor] 「{task_type}」: {len(cluster_logs)} logs, {unique_u} users → extracting skill...")
            try:
                skill = self._extract_skill(task_type, cluster_logs)
                skills.append(skill)
            except Exception as e:
                print(f"    ⚠ スキル抽出失敗: {e}")

        return skills

    # ── private ─────────────────────────────────────────────────

    def _filter_task_logs(self, logs: list[CopilotLog]) -> list[CopilotLog]:
        return [
            log for log in logs
            if log.accepted
            and log.follow_up_count <= 1
            and is_task_prompt(log.prompt)
        ]

    def _name_cluster(self, logs: list[CopilotLog]) -> tuple[str, str]:
        samples = [log.prompt[:200] for log in logs[:3]]
        prompt_text = NAME_PROMPT.format(
            samples_json=json.dumps(samples, ensure_ascii=False, indent=2)
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.1,
        )
        raw = _strip_fences(response.choices[0].message.content.strip())
        data = json.loads(raw)
        return data["task_type"], data.get("description", "")

    def _extract_skill(self, task_type: str, logs: list[CopilotLog]) -> ExtractedSkill:
        prompts_data = [log.prompt for log in logs]
        prompt_text = EXTRACTION_PROMPT.format(
            task_type=task_type,
            prompts_json=json.dumps(prompts_data, ensure_ascii=False, indent=2),
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.3,
        )
        raw = _strip_fences(response.choices[0].message.content.strip())
        data = json.loads(raw)
        unique_users = len({log.user_id for log in logs})
        is_public = (unique_users >= K_THRESHOLD
                     or (unique_users == 1 and len(logs) >= K_PROMPT_THRESHOLD))
        skill = ExtractedSkill(
            name=data["name"],
            description=data["description"],
            template_prompt=data["template_prompt"],
            variables=data["variables"],
            variable_descriptions=data.get("variable_descriptions", {}),
            example_use_cases=data["example_use_cases"],
            source_count=len(logs),
            unique_user_count=unique_users,
            category=task_type,
            status=SkillStatus.PUBLIC if is_public else SkillStatus.PENDING,
        )
        for inst in data.get("instances", []):
            skill.instances.append(SkillInstance(
                parent_skill_id=skill.skill_id,
                name=inst.get("name", ""),
                filled_prompt=inst.get("filled_prompt", ""),
                variable_values=inst.get("variable_values", {}),
                source_prompt=inst.get("source_prompt", ""),
            ))
        return skill
