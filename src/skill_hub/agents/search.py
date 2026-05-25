"""Embedding-based skill search index.

Encodes each skill as a dense vector (name + description + template_prompt)
using multilingual-E5-small and does cosine similarity at query time.
This replaces the naive "send all catalog to LLM" pattern in the recommender.
Falls back gracefully when sentence-transformers is not installed (API-only deploy).
"""
import warnings
from typing import TYPE_CHECKING

try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    _EMBEDDING_AVAILABLE = True
except ImportError:
    _EMBEDDING_AVAILABLE = False
    np = None  # type: ignore[assignment]
    SentenceTransformer = None  # type: ignore[assignment,misc]

from ..models import ExtractedSkill

_MODEL_NAME = "intfloat/multilingual-e5-small"
_PASSAGE_PREFIX = "passage: "
_QUERY_PREFIX = "query: "


class EmbeddingSearchIndex:
    def __init__(self):
        self._model = None
        self._skill_ids: list[str] = []
        self._matrix = None

    def _get_model(self):
        if not _EMBEDDING_AVAILABLE:
            return None
        if self._model is None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self._model = SentenceTransformer(_MODEL_NAME)
        return self._model

    def build(self, skills: list[ExtractedSkill]) -> None:
        if not skills or not _EMBEDDING_AVAILABLE:
            self._skill_ids = []
            self._matrix = None
            return
        texts = [
            _PASSAGE_PREFIX + " ".join(filter(None, [
                s.name, s.description, s.template_prompt,
                " ".join(s.triggers),
            ]))
            for s in skills
        ]
        model = self._get_model()
        if model is None:
            return
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            embs = model.encode(texts, batch_size=32, show_progress_bar=False,
                                normalize_embeddings=True)
        self._skill_ids = [s.skill_id for s in skills]
        self._matrix = np.array(embs, dtype=np.float32)

    def search(self, query: str, top_k: int = 5) -> list[str]:
        if self._matrix is None or len(self._skill_ids) == 0 or not _EMBEDDING_AVAILABLE:
            return []
        model = self._get_model()
        if model is None:
            return []
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            q_emb = model.encode(
                [_QUERY_PREFIX + query], normalize_embeddings=True, show_progress_bar=False
            )[0]
        sims = self._matrix @ q_emb
        k = min(top_k, len(self._skill_ids))
        top_indices = np.argpartition(sims, -k)[-k:]
        top_indices = top_indices[np.argsort(sims[top_indices])[::-1]]
        return [self._skill_ids[i] for i in top_indices]

    @property
    def is_built(self) -> bool:
        return self._matrix is not None
