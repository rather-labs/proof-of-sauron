import numpy as np
from PIL import Image
from typing import Dict
from scipy.stats import entropy
from scipy.ndimage import uniform_filter

class EntropyAnalyzer:
    def normalized_sigmoid(self, x , center=0.5, steepness=10):
        """
        Normalize values to [0, 1] using a sigmoid function
        center represent the middle point of the sigmoid function
        steepness represent how sharply the function transition between 0 and 1
        """
        return 1 / (1 + np.exp(-steepness * (x - center)))

    def compute_texture_metrics(self, tile):
        """Compute multiple texture metrics for a tile, (numpy array)"""

        # Convert to grayscale, tile is an image array
        tile = np.array(tile.convert('L'))

        metrics = dict()

        correlation_h, correlation_v = self.compute_inter_pixel_correlation(tile)
        metrics['entropy'] = self.compute_entropy(tile)
        metrics['correlation_h'] = correlation_h
        metrics['correlation_v'] = correlation_v

        return metrics

    def compute_entropy(self, tile):
        """Compute the entropy of an image tile in grey"""

        # Entropy (information content)
        hist = np.histogram(tile, bins=256, range=(0, 256))[0]
        hist = hist / hist.sum() # Normalize

        # Normalize by maximum possible entropy (log2(256) = 8)
        return entropy(hist, base=2) / 8 # Normalize to [0,1]

    def compute_local_entropy(self, tile, window_size=9):
        """
        Compute the average local Shannon entropy using sliding window
        The entropy is calculated for each window,
        and the mean of these entropy values (normalized to [0, 1])
        """

        if isinstance(tile, Image.Image):
            tile = np.array(tile.convert('L'))

        local_entropy = np.zeros_like(tile, dtype=float)

        half = window_size // 2
        rows, cols = tile.shape

        for i in range(half, rows - half):
            for j in range(half, cols - half):

                # Extract a subregion from the tile using slicing [start:end, start:end]
                window = tile[
                    i-half: i+half+1,
                    j-half: j+half+1
                ]

                # Calculate the entropy of the current window and store it the position (i,j)
                local_entropy[i,j] = self.compute_entropy(window)

        return np.mean(local_entropy)