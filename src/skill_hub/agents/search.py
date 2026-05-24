"""Embedding-based skill search index.

Encodes each skill as a dense vector (name + description + template_prompt)
using multilingual-E5-small and does cosine similarity at query time.
This replaces the naive "send all catalog to LLM" pattern in the recommender.
"""
import warnings
import numpy as np
from sentence_transformers import SentenceTransformer
from ..models import ExtractedSkill

_MODEL_NAME = "intfloat/multilingual-e5-small"
_PASSAGE_PREFIX = "passage: "
_QUERY_PREFIX = "query: "


class EmbeddingSearchIndex:
    def __init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._model = SentenceTransformer(_MODEL_NAME)
        self._skill_ids: list[str] = []
        self._matrix: np.ndarray | None = None

    def build(self, skills: list[ExtractedSkill]) -> None:
        if not skills:
            self._skill_ids = []
            self._matrix = None
            return
        texts = [
            _PASSAGE_PREFIX + f"{s.name} {s.description} {s.template_prompt}"
            for s in skills
        ]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            embs = self._model.encode(texts, batch_size=32, show_progress_bar=False,
                                      normalize_embeddings=True)
        self._skill_ids = [s.skill_id for s in skills]
        self._matrix = np.array(embs, dtype=np.float32)

    def search(self, query: str, top_k: int = 5) -> list[str]:
        if self._matrix is None or len(self._skill_ids) == 0:
            return []
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            q_emb = self._model.encode(
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
