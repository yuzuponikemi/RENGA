"""Aggregator の純粋ロジック。azure.functions に依存しない。

E2E テストはこちらを直接 import する。
function_app.py が Azure Function の Timer/HTTP トリガーから _aggregate() を呼ぶ。
"""
import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import httpx
from azure.cosmos import CosmosClient, exceptions


_client: CosmosClient | None = None


def _cosmos() -> tuple:
    """Return (skills, mappings, events) containers (lazy init)."""
    global _client
    if _client is None:
        _client = CosmosClient(
            os.environ["COSMOS_ENDPOINT"],
            os.environ["COSMOS_KEY"],
        )
    db = _client.get_database_client(os.environ.get("COSMOS_DB", "skill-hub"))
    return (
        db.get_container_client("skills"),
        db.get_container_client("contributor_mappings"),
        db.get_container_client("usage_events"),
    )


# ── Source fetch ─────────────────────────────────────────────────────────

def _fetch_skills_json(source: str) -> list[dict]:
    """Fetch catalog/skills.json from a source.

    Source format:
      - "owner/repo"           → GitHub raw fetch
      - "/abs/path.json"        → local file
      - "./relative/path.json"  → local file
    """
    if source.startswith(("/", ".")) or source.endswith(".json"):
        path = Path(source).expanduser()
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            logging.warning(f"Failed to read {path}: {e}")
            return []

    token = os.environ.get("RENGA_GITHUB_TOKEN", "")
    branch = os.environ.get("RENGA_GITHUB_BRANCH", "main")
    url = f"https://raw.githubusercontent.com/{source}/{branch}/catalog/skills.json"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        r = httpx.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.warning(f"Failed to fetch {url}: {e}")
        return []


# ── Merge logic ──────────────────────────────────────────────────────────

def _content_hash(template_prompt: str) -> str:
    return "sha256:" + hashlib.sha256(template_prompt.encode("utf-8")).hexdigest()


def _find_by_hash(skills_container, content_hash: str, category: str) -> dict | None:
    try:
        items = list(skills_container.query_items(
            query="SELECT * FROM c WHERE c.content_hash = @h",
            parameters=[{"name": "@h", "value": content_hash}],
            partition_key=category,
        ))
        return items[0] if items else None
    except exceptions.CosmosResourceNotFoundError:
        return None


def _merge(existing: dict, incoming: dict) -> dict:
    """既存スキルに新規貢献者を追記。"""
    handles = list({*existing.get("contributor_handles", []),
                    *incoming.get("contributor_handles", [])})
    src = existing.get("source_count", 0) + incoming.get("source_count", 0)
    existing["contributor_handles"] = handles
    existing["unique_user_count"] = len(handles)
    existing["source_count"] = src
    existing["last_updated_at"] = datetime.now(timezone.utc).isoformat()
    # k=3 に達したら public 昇格
    if len(handles) >= 3 and existing.get("status") != "public":
        existing["status"] = "public"
    # インスタンスは name で重複除去しながらマージ
    seen = {i.get("name") for i in existing.get("instances", [])}
    for inst in incoming.get("instances", []):
        if inst.get("name") not in seen:
            existing.setdefault("instances", []).append(inst)
            seen.add(inst.get("name"))
    return existing


def _prepare_new(incoming: dict, content_hash: str) -> dict:
    """Cosmos に新規 insert する skill ドキュメントを整形。"""
    now = datetime.now(timezone.utc).isoformat()
    doc = dict(incoming)
    doc["id"] = incoming["skill_id"]  # Cosmos の id
    doc["content_hash"] = content_hash
    doc["first_published_at"] = now
    doc["last_updated_at"] = now
    if incoming.get("contributor_handles"):
        doc["first_contributor"] = incoming["contributor_handles"][0]
    doc.setdefault("derived_from", [])
    doc.setdefault("derived_to", [])
    doc.setdefault("lineage_depth", 0)
    doc.setdefault("usage_by_team", {})
    return doc


# ── Core aggregate routine ───────────────────────────────────────────────

def _aggregate() -> dict:
    local = [s.strip() for s in os.environ.get("RENGA_LOCAL_CATALOG_PATHS", "").split(",") if s.strip()]
    repos = [r.strip() for r in os.environ.get("RENGA_GITHUB_REPOS", "").split(",") if r.strip()]
    sources = local or repos
    if not sources:
        return {"status": "skipped",
                "reason": "neither RENGA_LOCAL_CATALOG_PATHS nor RENGA_GITHUB_REPOS set"}

    skills_c, _, _ = _cosmos()
    stats = {"sources": len(sources), "fetched": 0, "merged": 0, "inserted": 0, "errors": 0}

    for source in sources:
        skills = _fetch_skills_json(source)
        if not skills:
            continue
        stats["fetched"] += len(skills)

        for incoming in skills:
            try:
                category = incoming.get("category", "uncategorized")
                content_hash = _content_hash(incoming["template_prompt"])
                existing = _find_by_hash(skills_c, content_hash, category)
                if existing:
                    merged = _merge(existing, incoming)
                    skills_c.upsert_item(merged)
                    stats["merged"] += 1
                else:
                    new_doc = _prepare_new(incoming, content_hash)
                    skills_c.upsert_item(new_doc)
                    stats["inserted"] += 1
            except Exception as e:
                logging.error(f"Failed to process skill from {source}: {e}")
                stats["errors"] += 1

    return {"status": "ok", **stats}
