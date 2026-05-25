from enum import Enum
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field


class SkillStatus(str, Enum):
    PENDING = "pending"   # source_count < k_threshold
    PUBLIC = "public"     # k>=3 gate passed, visible in catalog


class CopilotLog(BaseModel):
    user_id: str
    timestamp: str
    prompt: str
    response: str
    accepted: bool
    follow_up_count: int
    task_category: str


class SkillInstance(BaseModel):
    """抽象スキルの具体インスタンス。変数を実際の値で埋めた即使用可能なプロンプト。"""
    instance_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_skill_id: str
    name: str                         # 例: "factfullポッドキャスト→homupe記事"
    filled_prompt: str                # テンプレートの変数を実際の値に置き換えた完全プロンプト
    variable_values: dict[str, str]   # {"入力ソース": "factfull ポッドキャストデータ", ...}
    source_prompt: str                # このインスタンスを生んだ元のユーザープロンプト


class ExtractedSkill(BaseModel):
    skill_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    template_prompt: str
    variables: list[str]
    variable_descriptions: dict[str, str] = Field(default_factory=dict)  # 各変数の説明と使用例
    example_use_cases: list[str]
    instances: list[SkillInstance] = Field(default_factory=list)          # 具体インスタンス群
    source_count: int
    unique_user_count: int = 1
    triggers: list[str] = Field(default_factory=list)
    category: str = ""
    status: SkillStatus = SkillStatus.PENDING
    anonymized: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    usage_count: int = 0
    contributor_handles: list[str] = Field(default_factory=list)
