import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Optional

class SpatialAnalyzer:
    def compute_spatial_metrics(self, tile):
        """
        Compute spatial distribution  metrics for a given tile,
        performing gradient computation, texture uniformity, and inter-pixel correlation
        """
        
        metrics = {
            'texture_uniformity_h': 0.0,
            'texture_uniformity_v': 0.0
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



        except Exception as e:
            raise Exception(f"Error in spatial metrics: {str(e)}")
        
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
            print(f"Error in autocorrelation: {str(e)}")
            return 0.0
