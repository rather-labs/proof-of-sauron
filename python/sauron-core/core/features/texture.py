import numpy as np
from PIL import Image
import logging

from core.features.entropy import EntropyAnalyzer
from core.features.spatial import SpatialAnalyzer
from core.features.noise import NoiseAnalyzer

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
            
             # --- Compute Features using Component Analyzers ---
            
            # Spatial Features
            spatial_metrics = self.spatial_analyzer.compute_spatial_metrics(gray_tile)
            metrics.update(spatial_metrics) # Adds spatial keys directly

            # Noise Features
            noise_metrics = self.noise_analyzer.compute_noise_metrics(gray_tile)
            metrics.update(noise_metrics) # Adds noise keys directly

            # Entropy Features
            metrics['entropy_global'] = self.entropy_analyzer.compute_entropy(gray_tile) 
            metrics['entropy_local_mean'] = self.entropy_analyzer.compute_local_entropy(gray_tile)

            # Texture Features
            advanced_metrics = self._compute_texture_features(gray_tile)
            metrics.update(advanced_metrics) # Adds texture keys directly

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
            self._normalize_percentiles(tile_list)
                
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
        
    def _normalize_percentiles(tile_list, epsilon=1e-10):
        """Normalize array to [0, 1] range using percentiles."""
        p1, p99 = np.percentile(tile_list, (1, 99))
        norm_factor = max(p99 - p1, epsilon)

        # Avoid division by zero 
        return np.clip((tile_list - p1) / norm_factor, 0, 1)

    def _convert_to_grayscale(tile):
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