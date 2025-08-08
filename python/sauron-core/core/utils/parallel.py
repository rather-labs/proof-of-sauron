from joblib import Parallel, delayed
from typing import Callable, List, Any, Dict
import multiprocessing
import numpy as np

def process_tile_batch(batch: List[np.ndarray], analyzers: List[Callable]) -> List[Dict[str, float]]:
    """Process a batch of tiles with multiple analyzers"""
    results = []
    for tile in batch:
        tile_metrics = {}
        for analyzer in analyzers:
            try:
                metrics = analyzer(tile)
                tile_metrics.update(metrics)
            except Exception as e:
                print(f"Error in analyzer: {str(e)}")
        results.append(tile_metrics)
    return results

class ParallelProcessor:
    def __init__(self, n_jobs: int = None, backend: str = 'multiprocessing'):
        self.n_jobs = n_jobs or max(1, multiprocessing.cpu_count() - 1)
        self.backend = backend

    def process(self, func: Callable, items: List[Any]) -> List[Any]:
        """Process items in parallel using joblib"""
        return Parallel(n_jobs=self.n_jobs)(
            delayed(func)(item) for item in items
        )

    def process_batched(self, func: Callable, items: List[Any], batch_size: int = 100) -> List[Any]:
        """Process items in parallel with batching"""
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = self.process(func, batch)
            results.extend(batch_results)
        return results

    def process_tiles(self, tiles: List[np.ndarray],
                     analyzers: List[Callable],
                     batch_size: int = 4) -> List[Dict[str, float]]:
        """Process image tiles in parallel with multiple analyzers"""

        # Split tiles into batches
        batches = [
            tiles[i:i + batch_size]
            for i in range(0, len(tiles), batch_size)
        ]

        # Process batches in parallel
        results = Parallel(n_jobs=self.n_jobs, backend=self.backend)(
            delayed(process_tile_batch)(batch, analyzers) for batch in batches
        )

        # Flatten results
        return [
            metric
            for batch_result in results
            for metric in batch_result
        ]

        def compute_pairwise_divergence(self, histograms: List[np.ndarray],
                                  divergence_func: Callable,
                                  batch_size: int = 10) -> List[float]:
            """Compute pairwise divergences in parallel"""
            # Split into batches
            n_hists = len(histograms)
            batches = [
                histograms[i:i + batch_size]
                for i in range(0, n_hists, batch_size)
            ]

            # Compute divergences between batches
            all_divergences = []
            for i in range(len(batches)):
                batch_results = Parallel(n_jobs=self.n_jobs)(
                    delayed(compute_batch_divergences)(
                        batches[i], batches[j], divergence_func
                    )
                    for j in range(i + 1, len(batches))
                )
                all_divergences.extend([d for batch in batch_results for d in batch])

            return all_divergences