"""Personal mode: local JSON catalog at ``catalog/skills.json``.

This is a thin wrapper that re-exports the long-standing ``SkillCatalog`` so it
conforms to ``SkillCatalogProtocol`` without changing existing call sites.
"""
from ..catalog import SkillCatalog as PersonalSkillCatalog

__all__ = ["PersonalSkillCatalog"]
