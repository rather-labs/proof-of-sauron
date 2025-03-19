import numpy as np
from PIL import Image
from typing import Dict
from scipy.stats import entropy


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
        gray_tile = np.array(tile.convert('L'))
        metrics = dict()

        metrics['entropy'] = self.compute_entropy(gray_tile)
        print(metrics)

        return metrics
    
    def compute_entropy(self, tile):
        """Compute the entropy of an image tile in grey"""
        
        # Entropy (information content)
        hist = np.histogram(tile, bins=256, range=(0, 256))[0]
        hist = hist / hist.sum() # Normalize

        # Normalize by maximum possible entropy (log2(256) = 8)
        entr = entropy(hist, base=2) / 8 # Normalize to [0,1]
        
        return entr