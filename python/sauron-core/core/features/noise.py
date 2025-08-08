import numpy as np
from scipy.fft import fft2, fftshift
from typing import Dict

class NoiseAnalyzer:
    def __init__(self):
        self.fft_cache = {}

    def compute_noise_metrics(self, tile) -> Dict[str, float]:
        """Compute various noise-related metrics"""
        # Convert to grayscale if needed
        if len(tile.shape) > 2:
            tile = np.mean(tile, axis=2)

        # Compute FFT
        fft = np.abs(fftshift(fft2(tile)))

        # High frequency energy
        h, w = fft.shape
        hf_mask = self._create_hf_mask(h, w)
        hf_energy = np.mean(fft[hf_mask])

        # Noise variation
        noise_var = np.var(np.diff(tile.flatten()))

        return {'hf_energy': self._normalize(hf_energy, 1e5),
            'noise_variance': self._normalize(noise_var, 1000)}


    def _create_hf_mask(self, height, width) -> np.ndarray:
        """Create high frequency mask"""
        y, x = np.ogrid[-height//2:height//2, -width//2:width//2]
        dist_from_center = np.sqrt(x*x + y*y)
        mask = dist_from_center > min(height, width) // 4
        return mask

    def _normalize(self, value: float, scale: float) -> float:
        """Normalize value to [0,1] range"""
        return 1 / (1 + np.exp(-value/scale))
