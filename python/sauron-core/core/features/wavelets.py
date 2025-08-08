
import numpy as np
from typing import Dict
import pywt

class WaveletAnalyzer:

    def __init__(self, wavelet: str = 'db1', level: int = 3):
        """Initialize the wavelet analyzer with specified wavelet and decomposition level"""
        self.wavelet = wavelet
        self.level = level

    def compute_wavelet_metrics(self, tile: np.ndarray) -> Dict[str, float]:
        """Compute wavelet-based texture metrics with enhanced AI detection sensitivity"""
        try:
            # Convert to grayscale if needed
            if len(tile.shape) == 3:
                tile = np.mean(tile, axis=2)

            # Check dimensions
            if len(tile.shape) != 2 or min(tile.shape) < 4:  # Need at least 4x4 for wavelet
                return {}

            # Compute wavelet decomposition
            max_possible_level = self._get_max_possible_level(tile.shape)
            effective_level = min(self.level, max_possible_level)
            coeffs = pywt.wavedec2(tile, self.wavelet, level=effective_level)

            metrics = {}

            # Analyze each level with enhanced sensitivity for AI detection
            level_energies = []
            for i in range(1, len(coeffs)):
                h, v, d = coeffs[i]
                # Calculate directional energy ratios (more sensitive to AI artifacts)
                h_energy = np.mean(np.abs(h))
                v_energy = np.mean(np.abs(v))
                d_energy = np.mean(np.abs(d))

                # Calculate average energy
                level_energy = (h_energy + v_energy + d_energy) / 3

                # Calculate directional imbalance (higher in AI-generated images)
                dir_ratio = max(h_energy, v_energy, d_energy) / (min(h_energy, v_energy, d_energy) + 1e-10)

                # Enhance the wavelet coefficient with directional awareness
                # This makes the algorithm more sensitive to the regular patterns in AI images
                enhanced_energy = level_energy * (1.0 + 0.2 * dir_ratio)

                metrics[f'wavelet_l{i}'] = self._normalize(enhanced_energy)
                level_energies.append(enhanced_energy)

            # Overall wavelet energy (weighted by level importance)
            if level_energies:
                # Higher weight for higher frequency components (more important for AI detection)
                weights = [1.0, 1.5, 2.0][:len(level_energies)]
                weighted_sum = sum(e * w for e, w in zip(level_energies, weights))
                metrics['wavelet_total'] = self._normalize(weighted_sum / sum(weights))
            else:
                metrics['wavelet_total'] = 0.0

            return metrics

        except Exception as e:
            print(f"Error computing wavelet metrics: {str(e)}")
            return {}

    def _normalize(self, value: float) -> float:
        """Normalize value to [0,1] range"""
        return 1 / (1 + np.exp(-value * 10))

    def _get_max_possible_level(self, image_shape) -> int:
        """Calculate the maximum possible decomposition level for an image."""
        return pywt.dwt_max_level(min(image_shape), self.wavelet)
