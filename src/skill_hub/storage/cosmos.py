"""Org mode: Cosmos DB-backed catalog.

Requires the ``org`` extra: ``uv sync --extra org``.

Environment variables:
  COSMOS_ENDPOINT  — Cosmos DB account URL
  COSMOS_KEY       — Master or read-only key (use the read-only key on individual PCs)
  COSMOS_DB        — Database name (default: ``skill-hub``)
  USER_HANDLE      — Caller's anonymous handle (e.g. ``#A1``), used when appending usage_events
  RENGA_CLIENT_CONTEXT — ``mcp`` / ``copilot_studio`` / ``api`` (default ``mcp``)

The individual PC has *read-only* access to ``skills`` and *append-only* access to
``usage_events``. All other writes (``contributor_mappings``, ``contributor_reports``,
``gift_events``) happen through the Azure Function aggregator.

Container layout: see ``docs/db_schema.md``.
"""
import os
import uuid
from datetime import datetime, timezone

from ..models import ExtractedSkill, SkillStatus

_SKILLS_CONTAINER = "skills"
_EVENTS_CONTAINER = "usage_events"

# Fields that exist in Cosmos but not in ``ExtractedSkill``; stripped on read.
_COSMOS_ONLY_FIELDS = (
    "embedding",
    "content_hash",
    "derived_from",
    "derived_to",
    "lineage_depth",
    "usage_by_team",
    "first_contributor",
    "first_published_at",
    "last_updated_at",
    "last_used_at",
)


class CosmosSkillCatalog:
    """Cosmos-backed catalog. Conforms to ``SkillCatalogProtocol``."""

    def __init__(self) -> None:
        try:
            from azure.cosmos import CosmosClient
        except ImportError as e:
            raise RuntimeError(
                "azure-cosmos is required for org mode. Install with: uv sync --extra org"
            ) from e

        url = os.environ["COSMOS_ENDPOINT"]
        key = os.environ["COSMOS_KEY"]
        db_name = os.environ.get("COSMOS_DB", "skill-hub")
        client = CosmosClient(url, key)
        db = client.get_database_client(db_name)
        self._skills = db.get_container_client(_SKILLS_CONTAINER)
        self._events = db.get_container_client(_EVENTS_CONTAINER)

    # ─ SkillCatalogProtocol ──────────────────────────────────────────

    def save(self, skill: ExtractedSkill) -> None:
        raise NotImplementedError(
            "Org-mode catalog is read-only from individual PCs. "
            "Skills are aggregated by the Azure Function via GitHub."
        )

    def load_all(self) -> list[ExtractedSkill]:
        items = list(self._skills.query_items(
            query="SELECT * FROM c WHERE IS_DEFINED(c.skill_id)",
            enable_cross_partition_query=True,
        ))
        return [_doc_to_skill(d) for d in items]

    def get_public(self) -> list[ExtractedSkill]:
        items = list(self._skills.query_items(
            query="SELECT * FROM c WHERE c.status = 'public'",
            enable_cross_partition_query=True,
        ))
        return [_doc_to_skill(d) for d in items]

    def increment_usage(self, skill_id: str) -> None:
        event = {
            "id": str(uuid.uuid4()),
            "event_type": "skill_used",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "skill_id": skill_id,
            "context": os.environ.get("RENGA_CLIENT_CONTEXT", "mcp"),
            "user_handle": os.environ.get("USER_HANDLE", "#anon"),
        }
        self._events.create_item(event)

    def add_contributor(self, skill_id: str, handle: str) -> None:
        raise NotImplementedError(
            "Contributors are managed by the Azure Function aggregator."
        )

    def clear(self) -> None:
        raise NotImplementedError(
            "Org-mode catalog cannot be cleared from individual PCs."
        )

    def stats(self) -> dict:
        all_skills = self.load_all()
        return {
            "total": len(all_skills),
            "public": sum(1 for s in all_skills if s.status == SkillStatus.PUBLIC),
            "pending": sum(1 for s in all_skills if s.status == SkillStatus.PENDING),
            "total_usage": sum(s.usage_count for s in all_skills),
        }


def _doc_to_skill(doc: dict) -> ExtractedSkill:
    clean = {k: v for k, v in doc.items() if not k.startswith("_") and k != "id"}
    for f in _COSMOS_ONLY_FIELDS:
        clean.pop(f, None)
    return ExtractedSkill(**clean)
