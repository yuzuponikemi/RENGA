"""Skill catalog storage backends.

Mode selection via env var ``RENGA_MODE``:
  - ``personal`` (default): local JSON at ``catalog/skills.json``
  - ``org``               : Cosmos DB (requires ``azure-cosmos`` extra)

Use ``make_catalog()`` to obtain a catalog conforming to ``SkillCatalogProtocol``.
"""
import os

from .base import SkillCatalogProtocol


def make_catalog() -> SkillCatalogProtocol:
    mode = os.environ.get("RENGA_MODE", "personal").lower()
    if mode == "org":
        from .cosmos import CosmosSkillCatalog
        return CosmosSkillCatalog()
    from .personal import PersonalSkillCatalog
    return PersonalSkillCatalog()


__all__ = ["SkillCatalogProtocol", "make_catalog"]
