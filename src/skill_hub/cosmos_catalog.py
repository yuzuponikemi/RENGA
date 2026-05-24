"""Cosmos DB バックエンド。SkillCatalog と同じインターフェース。
環境変数 CATALOG_BACKEND=cosmos のとき api.py / main.py が自動選択する。
"""
import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from .models import ExtractedSkill, SkillStatus

CONTAINER_NAME = "skills"


class CosmosSkillCatalog:
    def __init__(self):
        url = os.environ["COSMOS_ENDPOINT"]
        key = os.environ["COSMOS_KEY"]
        db_name = os.environ.get("COSMOS_DB", "skill-hub")
        self.client = CosmosClient(url, key)
        db = self.client.create_database_if_not_exists(id=db_name)
        self.container = db.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/category"),
            offer_throughput=400,
        )

    def save(self, skill: ExtractedSkill) -> None:
        item = skill.model_dump()
        item["id"] = skill.skill_id  # Cosmos requires "id" field
        self.container.upsert_item(item)

    def increment_usage(self, skill_id: str) -> None:
        items = list(self.container.query_items(
            query="SELECT * FROM c WHERE c.skill_id = @id",
            parameters=[{"name": "@id", "value": skill_id}],
            enable_cross_partition_query=True,
        ))
        if items:
            item = items[0]
            item["usage_count"] = item.get("usage_count", 0) + 1
            self.container.upsert_item(item)

    def add_contributor(self, skill_id: str, handle: str) -> None:
        items = list(self.container.query_items(
            query="SELECT * FROM c WHERE c.skill_id = @id",
            parameters=[{"name": "@id", "value": skill_id}],
            enable_cross_partition_query=True,
        ))
        if items:
            item = items[0]
            handles = item.get("contributor_handles", [])
            if handle not in handles:
                handles.append(handle)
            item["contributor_handles"] = handles
            self.container.upsert_item(item)

    def load_all(self) -> list[ExtractedSkill]:
        items = list(self.container.query_items(
            query="SELECT * FROM c WHERE IS_DEFINED(c.skill_id)",
            enable_cross_partition_query=True,
        ))
        return [ExtractedSkill(**{k: v for k, v in i.items() if not k.startswith("_") and k != "id"})
                for i in items]

    def get_public(self) -> list[ExtractedSkill]:
        return [s for s in self.load_all() if s.status == SkillStatus.PUBLIC]

    def clear(self) -> None:
        items = list(self.container.query_items(
            query="SELECT c.id, c.category FROM c WHERE IS_DEFINED(c.skill_id)",
            enable_cross_partition_query=True,
        ))
        for item in items:
            self.container.delete_item(item=item["id"], partition_key=item["category"])

    def stats(self) -> dict:
        all_skills = self.load_all()
        return {
            "total": len(all_skills),
            "public": sum(1 for s in all_skills if s.status == SkillStatus.PUBLIC),
            "pending": sum(1 for s in all_skills if s.status == SkillStatus.PENDING),
            "total_usage": sum(s.usage_count for s in all_skills),
        }
