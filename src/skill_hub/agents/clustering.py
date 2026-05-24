"""
Deterministic embedding-based clustering for prompt logs.

Supported strategies (in order of sophistication):
  baseline  TF-IDF char n-gram → TruncatedSVD(64) → HDBSCAN
  step1     baseline + cosine-similarity noise reassignment
  step2     TF-IDF char n-gram → UMAP(10) → HDBSCAN + reassign
  step3     multilingual-E5 → UMAP(10) → HDBSCAN + reassign

Default strategy used by ExtractorAgent: step1 (safe; no heavy deps at import time).
step2/step3 require umap-learn; step3 also requires sentence-transformers.
"""

from __future__ import annotations

import warnings
import time
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sklearn.cluster import HDBSCAN

STRATEGIES = ("baseline", "step1", "step2", "step3")


@dataclass
class ClusterResult:
    labels: list[int]
    n_clusters: int
    n_noise: int
    noise_rate: float
    elapsed_s: float
    strategy: str

    def summary(self) -> str:
        return (
            f"[{self.strategy}] clusters={self.n_clusters} "
            f"noise={self.n_noise} ({self.noise_rate:.1%}) "
            f"time={self.elapsed_s:.1f}s"
        )


class EmbeddingClusterer:
    def __init__(
        self,
        min_cluster_size: int = 3,
        strategy: str = "step1",
        noise_threshold: float = 0.30,
    ):
        if strategy not in STRATEGIES:
            raise ValueError(f"strategy must be one of {STRATEGIES}")
        self.min_cluster_size = min_cluster_size
        self.strategy = strategy
        self.noise_threshold = noise_threshold

    # ── public ────────────────────────────────────────────────────

    def fit(self, texts: list[str]) -> list[int]:
        return self.fit_detailed(texts).labels

    def fit_detailed(self, texts: list[str]) -> ClusterResult:
        t0 = time.perf_counter()
        n = len(texts)
        if n < self.min_cluster_size:
            labels = [-1] * n
            self._last_embedding = None
        else:
            labels = self._dispatch(texts)

        elapsed = time.perf_counter() - t0
        unique = [l for l in labels if l >= 0]
        n_clusters = len(set(unique)) if unique else 0
        n_noise = labels.count(-1)

        return ClusterResult(
            labels=labels,
            n_clusters=n_clusters,
            n_noise=n_noise,
            noise_rate=n_noise / n if n else 0.0,
            elapsed_s=elapsed,
            strategy=self.strategy,
        )

    @property
    def last_embedding(self) -> np.ndarray | None:
        """The embedding matrix used in the last fit_detailed() call."""
        return getattr(self, "_last_embedding", None)

    # ── strategy dispatch ─────────────────────────────────────────

    def _dispatch(self, texts: list[str]) -> list[int]:
        if self.strategy == "baseline":
            X = self._tfidf_matrix(texts)
            X_red = self._svd_reduce(X)
            self._last_embedding = X_red
            return self._hdbscan(X_red)

        if self.strategy == "step1":
            X = self._tfidf_matrix(texts)
            X_red = self._svd_reduce(X)
            self._last_embedding = X_red
            labels = self._hdbscan(X_red)
            return self._reassign_noise(X_red, labels)

        if self.strategy == "step2":
            X = self._tfidf_matrix(texts)
            X_red = self._umap_reduce(X.toarray().astype(np.float32))
            self._last_embedding = X_red
            labels = self._hdbscan(X_red)
            return self._reassign_noise(X_red, labels)

        if self.strategy == "step3":
            X_e5 = self._e5_embed(texts)
            X_red = self._umap_reduce(X_e5)
            self._last_embedding = X_red
            labels = self._hdbscan(X_red)
            return self._reassign_noise(X_red, labels)

        raise ValueError(self.strategy)

    # ── embedding layers ──────────────────────────────────────────

    def _tfidf_matrix(self, texts: list[str]):
        vec = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 4),
            max_features=5000,
            sublinear_tf=True,
        )
        return vec.fit_transform(texts)

    def _svd_reduce(self, X) -> np.ndarray:
        n = X.shape[0]
        n_components = min(64, X.shape[1] - 1, n - 1)
        if n_components < 2:
            return normalize(X.toarray())
        svd = TruncatedSVD(n_components=n_components, random_state=42)
        return normalize(svd.fit_transform(X))

    def _umap_reduce(self, X: np.ndarray, n_components: int = 10) -> np.ndarray:
        from umap import UMAP

        n = X.shape[0]
        n_neighbors = min(15, n - 1)
        n_components = min(n_components, n - 1)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            reducer = UMAP(
                n_components=n_components,
                n_neighbors=n_neighbors,
                random_state=42,
                low_memory=False,
            )
            return reducer.fit_transform(X)

    def _e5_embed(self, texts: list[str]) -> np.ndarray:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("intfloat/multilingual-e5-small")
        prefixed = ["query: " + t for t in texts]
        embeddings = model.encode(prefixed, batch_size=64, show_progress_bar=False)
        return normalize(np.array(embeddings))

    # ── clustering + noise reassignment ──────────────────────────

    def _hdbscan(self, X: np.ndarray) -> list[int]:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            labels = HDBSCAN(
                min_cluster_size=self.min_cluster_size,
                min_samples=1,
                metric="euclidean",
                copy=True,
            ).fit_predict(X)
        return labels.tolist()

    def _reassign_noise(self, X: np.ndarray, labels: list[int]) -> list[int]:
        unique_labels = sorted(set(l for l in labels if l >= 0))
        if not unique_labels:
            return labels

        # Compute per-cluster centroid (mean of normalized vectors → re-normalize)
        label_arr = np.array(labels)
        centroids = np.vstack([
            normalize(X[label_arr == l].mean(axis=0, keepdims=True))
            for l in unique_labels
        ])  # shape: (n_clusters, dim)

        new_labels = list(labels)
        noise_indices = [i for i, l in enumerate(labels) if l == -1]
        if not noise_indices:
            return new_labels

        noise_vecs = X[noise_indices]          # (n_noise, dim)
        sims = noise_vecs @ centroids.T        # cosine sim (both normalized)

        for pos, i in enumerate(noise_indices):
            best_idx = int(np.argmax(sims[pos]))
            if sims[pos, best_idx] >= self.noise_threshold:
                new_labels[i] = unique_labels[best_idx]

        return new_labels
