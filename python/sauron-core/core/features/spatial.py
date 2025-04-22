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

        except Exception as e:
            raise Exception(f"Error in spatial metrics: {str(e)}")
        
        return metrics