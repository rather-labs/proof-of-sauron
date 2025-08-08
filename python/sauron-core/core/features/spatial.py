import logging
import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Optional
from scipy.ndimage import minimum_filter, maximum_filter
from scipy.stats import wasserstein_distance, entropy


# logger at module level
logger = logging.getLogger(__name__)

class SpatialAnalyzer:
    def compute_spatial_metrics(self, tile):
        """
        Compute spatial distribution  metrics for a given tile,
        performing gradient computation, texture uniformity, and inter-pixel correlation
        """

        metrics = {
            'texture_uniformity_h': 0.0,
            'texture_uniformity_v': 0.0,
            'correlation_h': 0.0,
            'correlation_v': 0.0,
            'contrast_variance': 0.0
        }

        try:
            if isinstance(tile, Image.Image):
                # Convert to grayscale
                gray_tile = np.array(tile.convert('L'))
            elif isinstance(tile, np.ndarray):
                gray_tile = tile
            else:
                raise ValueError("Input 'tile' must be a PIL Image or a 2D NumPy array.")

            # Local texture uniformity patterns
            gradient_h = np.diff(gray_tile, axis=1)
            gradient_v = np.diff(gray_tile, axis=0)

            # Compute gradient histograms
            hist_h, _ = np.histogram(gradient_h.flatten(), bins=50, density=True)
            hist_v, _ = np.histogram(gradient_v.flatten(), bins=50, density=True)

            # Texture uniformity measures
            metrics['texture_uniformity_h'] = np.std(hist_h)
            metrics['texture_uniformity_v'] = np.std(hist_v)

            # Inter-pixel correlation
            metrics['correlation_h'] = self._compute_autocorrelation(gradient_h)
            metrics['correlation_v'] = self._compute_autocorrelation(gradient_v)

            # Local contrast variations
            window_size = 9
            local_contrast = self._compute_local_contrast(gray_tile, window_size)
            metrics['contrast_variance'] = float(np.var(local_contrast))

        except Exception as e:
            print(f"Error in spatial metrics: {str(e)}")

        return metrics

    def compute_inter_tile_divergence(self, tiles):
        """Compute statistical divergence between tiles"""
        metrics = {}
        n_tiles = len(tiles)

        # Convert tiles to grayscale
        gray_tiles = [np.mean(t, axis=2) if len(t.shape) == 3 else t for t in tiles]

        # Compute pairwise divergences
        divergences = []
        for i in range(n_tiles):
            for j in range(i + 1, n_tiles):
                # Gradient histograms
                hist_i, _ = np.histogram(gray_tiles[i], bins=50, density=True)
                hist_j, _ = np.histogram(gray_tiles[j], bins=50, density=True)

                # Wasserstein distance between histograms
                div = wasserstein_distance(hist_i, hist_j)
                divergences.append(div)

        # Statistical measures of divergence
        metrics['texture_divergence_mean'] = np.mean(divergences)
        metrics['texture_divergence_std'] = np.std(divergences)

        return metrics


    def _compute_autocorrelation(self, signal):
        """
        Compute the normalized auto-correlation of a given flattened signal
        Calculates the average of normalized correlations for lags k=1 to n-1.

        https://numpy.org/doc/2.2/reference/generated/numpy.correlate.html
        """
        try:
            signal_flatten = signal.flatten()
            n = len(signal_flatten)

            if n <= 1:
                return 0.0

            # Center the signal
            # y[n] = x[n] - mean(x)
            y = signal_flatten - np.mean(signal_flatten)

            # Compute correlation for non negative lags
            # r[k] = sum(y[n] * y[n+k]) for k=0 to n-1
            r = np.correlate(y, y, mode='full')[n-1:]

            if r[0] == 0:
                return 0.0

            # Average of normalized correlations for signal lags k=1 to n-1
            # r[0] is the sum of squares of y (proportional to variance)
            # Sum r[1:] / r[0] and divide by the number of terms (n - 1)
            # Ensure n-1 is not zero, already handled by the n <= 1 check
            average_normalized_correlation = float(np.sum(r[1:] / r[0]) / (n - 1))

            return average_normalized_correlation

        except Exception as e:
            logger.error(f"Error in autocorrelation: {str(e)}")
            return 0.0

    def _compute_local_contrast(self, tile, window_size=9):
        """
        Compute the average local contrast using sliding window
        The contrast is calculated for each window,
        and the mean of these contrast values (normalized to [0, 1])

        https://en.wikipedia.org/w/index.php?title=Contrast_(vision)#Michelson_contrast
        """

        image_float = tile.astype(np.float32)
        local_min = minimum_filter(image_float, size=window_size, mode='reflect')
        local_max = maximum_filter(image_float, size=window_size, mode='reflect')

        # epsilon is added to avoid division by zero
        epsilon = 1e-6

        # Michelson Contrast is defined as:
        # c = ( max - min ) / ( max - min + epsilon )
        numerator = local_max - local_min
        denominator = local_max + local_min + epsilon
        contrast = numerator / denominator

        # Normalize contrast to [0, 1]
        local_contrast = np.clip(contrast, 0, 1)

        return local_contrast