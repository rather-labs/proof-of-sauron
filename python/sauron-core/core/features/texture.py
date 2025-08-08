import numpy as np
from PIL import Image
from typing import Dict, List, Optional

from core.features.entropy import EntropyAnalyzer
from core.features.spatial import SpatialAnalyzer
from core.features.noise import NoiseAnalyzer

import logging

from scipy.stats import entropy, wasserstein_distance
from scipy.spatial.distance import jensenshannon

from core.utils.constants import ORIENTATIONS_DEFAULT, DEFAULT_EPSILON
from core.utils.cache import Cache

logger = logging.getLogger(__name__)


def compute_histogram(arr: np.ndarray, epsilon: float = 1e-10) -> np.ndarray:
    """Compute normalized histogram with proper binning"""
    hist, _ = np.histogram(arr, bins=50, range=(0, 1), density=True)
    hist = hist + epsilon
    hist = hist / np.sum(hist)
    return hist

class TextureAnalyzer:
    def __init__(self):
        self.noise_analyzer = NoiseAnalyzer()
        self.entropy_analyzer = EntropyAnalyzer()
        self.spatial_analyzer = SpatialAnalyzer()

        # Predefined angles for texture analysis
        self.orientation = [ORIENTATIONS_DEFAULT]
        self.epsilon = DEFAULT_EPSILON

        logger.info("TextureAnalyzer initialized")

    @Cache()
    def compute_texture_features(self, tile: Image.Image) -> Dict[str, float]:
        """Analyze texture patterns focusing on natural vs AI characteristics"""
        try:
            metrics: Dict[str, float] = dict()
            gray_tile = self._preprocess_image(tile)
            if gray_tile is None:
                return metrics

            # Spatial Features
            spatial_metrics = self.spatial_analyzer.compute_spatial_metrics(gray_tile)
            metrics.update(spatial_metrics) # Adds spatial keys directly

            # Noise Features
            noise_metrics = self.noise_analyzer.compute_noise_metrics(gray_tile)
            metrics.update(noise_metrics) # Adds noise keys directly

            # Entropy Features
            metrics['global_entropy'] = self.entropy_analyzer.compute_entropy(gray_tile)
            metrics['entropy_local_mean'] = self.entropy_analyzer.compute_local_entropy(gray_tile)

            # Analyze sub-regions for natural variation
            regions = self._split_into_regions(gray_tile, 3)  # Split into 3x3 regions
            region_stats: List[Dict[str, float]] = []
            region_hists: List[np.ndarray] = []

            for region in regions:
                hist = compute_histogram(region.flatten(), self.epsilon)
                region_hists.append(hist)
                region_stats.append({
                    'entropy': self.entropy_analyzer.compute_entropy(region),
                    'mean': float(np.mean(region)),
                    'std': float(np.std(region))
                })

            # Compute statistics variance across regions
            entropies = [s['entropy'] for s in region_stats]
            means = [s['mean'] for s in region_stats]
            stds = [s['std'] for s in region_stats]

            # Higher values indicate more natural variation
            metrics['region_entropy_var'] = float(np.var(entropies))
            metrics['region_mean_var'] = float(np.var(means))
            metrics['region_std_var'] = float(np.var(stds))

            # Inter-region divergence (higher in natural images)
            divergences = []
            for i in range(len(region_hists)):
                for j in range(i + 1, len(region_hists)):
                    div_kl = entropy(region_hists[i], region_hists[j])
                    div_js = jensenshannon(region_hists[i], region_hists[j])
                    div_w = wasserstein_distance(region_hists[i], region_hists[j])
                    if not np.isnan(div_kl):
                        divergences.extend([div_kl, div_js, div_w])

            if divergences:
                metrics['region_divergence_mean'] = float(np.mean(divergences))
                metrics['region_divergence_var'] = float(np.var(divergences))

            # Gradient analysis
            grad_metrics = self._compute_gradient_features(gray_tile)
            metrics.update(grad_metrics)

            return metrics

        except Exception as e:
            logging.error(f"Error in texture analysis: {e}")

        return None

    def compute_texture_divergence(self, tiles: List[Image.Image]) -> Dict[str, float]:
        """Compute texture divergence metrics between a set of tiles"""
        metrics: Dict[str, float] = {}

        # Need at least 2 tiles to compute divergence
        if len(tiles) < 2:
            return metrics

        try:
            # Preprocess tiles
            processed_tiles = []
            for tile in tiles:
                processed = self._preprocess_image(tile)
                if processed is not None:
                    processed_tiles.append(processed)

            # Need at least 2 valid processed tiles
            if len(processed_tiles) < 2:
                return metrics

            # Compute histograms for each tile
            histograms = [compute_histogram(tile.flatten(), self.epsilon) for tile in processed_tiles]

            # Calculate pairwise divergences between histograms
            div_values: Dict[str, List[float]] = {
                'kl_div': [],
                'js_div': [],
                'wasserstein_dist': []
            }

            for i in range(len(histograms)):
                for j in range(i + 1, len(histograms)):
                    kl = entropy(histograms[i], histograms[j])
                    js = jensenshannon(histograms[i], histograms[j])
                    wd = wasserstein_distance(histograms[i], histograms[j])

                    if not np.isnan(kl) and not np.isinf(kl):
                        div_values['kl_div'].append(kl)
                    if not np.isnan(js) and not np.isinf(js):
                        div_values['js_div'].append(js)
                    if not np.isnan(wd) and not np.isinf(wd):
                        div_values['wasserstein_dist'].append(wd)

            # Calculate aggregate statistics
            for key, values in div_values.items():
                if values:
                    metrics[f"{key}_mean"] = float(np.mean(values))
                    metrics[f"{key}_std"] = float(np.std(values))
                    metrics[f"{key}_max"] = float(np.max(values))

            return metrics

        except Exception as e:
            logger.error(f"Error in texture divergence: {e}")
        return {}  # Return empty dict on error, not None

    def _compute_gradient_features(self, image: np.ndarray) -> Dict[str, float]:
        """Calculate image gradient features for texture analysis."""
        metrics: Dict[str, float] = {}

        try:
            # Compute X and Y gradients using simple differencing
            grad_x = np.diff(image, axis=1)
            grad_y = np.diff(image, axis=0)

            # Compute gradient magnitude (append zeros to match original shape)
            mag_x = np.append(grad_x, np.zeros((image.shape[0], 1), dtype=np.float32), axis=1)
            mag_y = np.append(grad_y, np.zeros((1, image.shape[1]), dtype=np.float32), axis=0)

            # Gradient magnitude
            grad_magnitude = np.sqrt(mag_x**2 + mag_y**2)

            # Extract metrics
            metrics['gradient_mean'] = float(np.mean(grad_magnitude))
            metrics['gradient_std'] = float(np.std(grad_magnitude))
            metrics['gradient_energy'] = float(np.sum(grad_magnitude**2) / grad_magnitude.size)

            # Gradient direction histogram (8 bins)
            dirs = np.arctan2(mag_y, mag_x)
            hist, _ = np.histogram(dirs, bins=8, range=(-np.pi, np.pi))
            hist = hist / np.sum(hist)

            # Gradient direction entropy (normalized)
            metrics['gradient_direction_entropy'] = float(entropy(hist + 1e-10) / np.log(8))

        except Exception as e:
            logger.warning(f"Error computing gradient features: {e}")

        return metrics

    def _preprocess_image(self, tile: Image.Image) -> Optional[np.ndarray]:
        """Convert image to normalized grayscale (0-1 range)."""
        try:
            # Convert to grayscale numpy array
            gray_tile = self._convert_to_grayscale(tile)
            if gray_tile is None:
                return None

            # Normalize using percentiles
            gray_tile = self._normalize_percentiles(gray_tile)
            return gray_tile

        except Exception as e:
            logger.error(f"Error: {e}")
            return None

    def _normalize_percentiles(self, tile_list: np.ndarray) -> np.ndarray:
        """Normalize array to [0, 1] range using percentiles."""
        p1, p99 = np.percentile(tile_list, (1, 99))
        norm_factor = max(p99 - p1, self.epsilon)

        # Avoid division by zero
        return np.float32(np.clip((tile_list - p1) / norm_factor, 0, 1))

    def _convert_to_grayscale(self, tile: Image.Image) -> Optional[np.ndarray]:
        """Convert input to grayscale float32 array."""
        try:
            result = None
            # Handle PIL Image
            if isinstance(tile, Image.Image):
                result = np.array(tile.convert('L'), dtype=np.float32)

            if isinstance(tile, np.ndarray):
                # Already grayscale
                if tile.ndim == 2:
                    result = tile.astype(np.float32)
                elif tile.ndim == 3:
                    result = np.mean(tile, axis=-1).astype(np.float32)

            return result

        except Exception:
            return None

    def _split_into_regions(self, image, n):
        """Split image into n x n regions for comparative analysis."""
        h, w = image.shape
        regions = []
        h_step = h // n
        w_step = w // n

        for i in range(n):
            for j in range(n):
                region = image[i*h_step:(i+1)*h_step, j*w_step:(j+1)*w_step]
                regions.append(region)

        return regions