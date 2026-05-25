"""Storage protocol shared by personal (local JSON) and org (Cosmos) backends."""
from typing import Protocol, runtime_checkable

from ..models import ExtractedSkill


@runtime_checkable
class SkillCatalogProtocol(Protocol):
    """Common interface for skill catalog storage backends.

    Personal-mode (local JSON) supports the full read/write surface.
    Org-mode (Cosmos) is read-only for skills from the individual PC's perspective;
    writes happen only through the Azure Function aggregator. The exceptions are
    ``increment_usage`` which appends to ``usage_events`` and is allowed.
    """

    def save(self, skill: ExtractedSkill) -> None:
        """Persist a skill. Org mode raises NotImplementedError."""

    def load_all(self) -> list[ExtractedSkill]:
        """Return every skill, regardless of status."""

    def get_public(self) -> list[ExtractedSkill]:
        """Return only skills with status=PUBLIC."""

    def increment_usage(self, skill_id: str) -> None:
        """Record a usage event for the skill."""

    def add_contributor(self, skill_id: str, handle: str) -> None:
        """Attach an anonymous contributor handle. Org mode raises NotImplementedError."""

    def clear(self) -> None:
        """Wipe the catalog. Org mode raises NotImplementedError."""

    def stats(self) -> dict:
        """Return summary counts (total / public / pending / total_usage)."""
