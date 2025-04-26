import numpy as np
from PIL import Image
import logging

from core.features.entropy import EntropyAnalyzer
from core.features.spatial import SpatialAnalyzer
from core.features.noise import NoiseAnalyzer

from scipy.stats import entropy, wasserstein_distance
from scipy.spatial.distance import jensenshannon

from core.constants import ORIENTATIONS_DEFAULT, DEFAULT_EPSILON

logger = logging.getLogger(__name__)


def compute_histogram(arr, epsilon = 1e-10):
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

    def compute_texture_features(self, tile):
        """Analyze texture patterns focusing on natural vs AI characteristics"""
        try:
            metrics = dict()
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
            region_stats = []
            region_hists = []

            for region in regions:
                hist = compute_histogram(region.flatten(), self.epsilon)
                region_hists.append(hist)
                region_stats.append({
                    'entropy': self.entropy_analyzer.compute_entropy(hist),
                    'mean': np.mean(region),
                    'std': np.std(region)
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
                    div_kl = self.entropy_analyzer.compute_entropy(region_hists[i], region_hists[j])
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

    def compute_texture_divergence(self, tiles):
        pass

    def _preprocess_image(self,tile):
        """Convert image to normalized grayscale (0-1 range)."""
        try:
            # Convert to grayscale numpy array
            gray_tile = self._convert_to_grayscale(tile)
            if gray_tile is None:
                return None
                
            # Normalize using percentiles
            self._normalize_percentiles(gray_tile)
            return gray_tile
                
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
        
    def _normalize_percentiles(self, tile_list):
        """Normalize array to [0, 1] range using percentiles."""
        p1, p99 = np.percentile(tile_list, (1, 99))
        norm_factor = max(p99 - p1, self.epsilon)

        # Avoid division by zero 
        return np.clip((tile_list - p1) / norm_factor, 0, 1)

    def _convert_to_grayscale(self, tile):
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