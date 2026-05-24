"""
Clustering strategy benchmark — no LLM calls.

Runs all 4 strategies on the actual Claude Code logs and compares:
  - n_clusters, n_noise, noise_rate
  - silhouette score in each strategy's own embedding space (fair comparison)
  - elapsed time

Usage:
  uv run python scripts/benchmark_clustering.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

import numpy as np
from sklearn.metrics import silhouette_score

from src.skill_hub.agents.extractor import is_task_prompt
from src.skill_hub.agents.clustering import EmbeddingClusterer, STRATEGIES
from src.skill_hub.log_readers import ClaudeCodeLogReader


def load_task_prompts() -> list[str]:
    reader = ClaudeCodeLogReader()
    logs = reader.read()
    task_logs = [
        log for log in logs
        if log.accepted and log.follow_up_count <= 1 and is_task_prompt(log.prompt)
    ]
    print(f"Loaded {len(logs)} logs → {len(task_logs)} task-type prompts\n")
    return [log.prompt for log in task_logs]


def compute_silhouette(X: np.ndarray, labels: list[int]) -> float | None:
    """Silhouette score in the strategy's own embedding space. Excludes noise."""
    label_arr = np.array(labels)
    valid = [l for l in set(labels) if l >= 0 and (label_arr == l).sum() > 1]
    if len(valid) < 2:
        return None
    mask = label_arr >= 0
    X_sub = X[mask]
    y_sub = label_arr[mask]
    sample_size = min(500, len(y_sub))
    try:
        return float(silhouette_score(X_sub, y_sub, metric="euclidean",
                                      sample_size=sample_size, random_state=42))
    except Exception:
        return None


def run_benchmark(prompts: list[str]) -> list[dict]:
    results = []
    for strategy in STRATEGIES:
        print(f"── Strategy: {strategy} {'─'*40}")
        clusterer = EmbeddingClusterer(min_cluster_size=3, strategy=strategy)
        result = clusterer.fit_detailed(prompts)

        X_emb = clusterer.last_embedding
        sil = compute_silhouette(X_emb, result.labels) if X_emb is not None else None
        sil_str = f"{sil:.4f}" if sil is not None else "N/A"

        print(f"  {result.summary()}")
        print(f"  silhouette (own space) = {sil_str}\n")

        results.append({
            "strategy": strategy,
            "n_clusters": result.n_clusters,
            "n_noise": result.n_noise,
            "noise_rate": result.noise_rate,
            "silhouette": sil,
            "elapsed_s": result.elapsed_s,
        })
    return results


def print_table(results: list[dict], n_total: int) -> None:
    header = (f"{'Strategy':<12} {'Clusters':>8} {'Noise':>7} {'Noise%':>7} "
              f"{'Silhouette':>11} {'Time(s)':>8}")
    sep = "─" * len(header)
    print("\n" + sep)
    print(header)
    print(sep)
    for r in results:
        sil = f"{r['silhouette']:.4f}" if r["silhouette"] is not None else "   N/A"
        print(
            f"{r['strategy']:<12} {r['n_clusters']:>8} {r['n_noise']:>7} "
            f"{r['noise_rate']:>6.1%} {sil:>11} {r['elapsed_s']:>8.1f}"
        )
    print(sep)
    print(f"Total prompts: {n_total}\n")

    print("── 解釈のポイント ──────────────────────────────────")
    print("  silhouette: -1〜1。高いほどクラスタ内密度が高く境界が明確。")
    print("  各戦略は自分の埋め込み空間で計算（TF-IDF vs UMAP vs E5）。")
    print("  noise=0 は再配置済みを意味する（純粋なノイズ除去ではない）。\n")

    ranked = sorted(
        [r for r in results if r["silhouette"] is not None],
        key=lambda r: (-r["silhouette"], r["noise_rate"]),
    )
    if ranked:
        best = ranked[0]
        print(f"★ Best (silhouette): {best['strategy']}"
              f"  silhouette={best['silhouette']:.4f}, noise={best['noise_rate']:.1%}")
        print()
        print("Ranking:")
        for rank, r in enumerate(ranked, 1):
            print(f"  {rank}. {r['strategy']:<12} sil={r['silhouette']:.4f}  "
                  f"noise={r['noise_rate']:.1%}  time={r['elapsed_s']:.1f}s")


if __name__ == "__main__":
    prompts = load_task_prompts()
    results = run_benchmark(prompts)
    print_table(results, len(prompts))
