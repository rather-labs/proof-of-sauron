
from core.features.texture import TextureAnalyzer
from core.features.wavelets import WaveletAnalyzer
from core.features.spatial import SpatialAnalyzer
from typing import List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class AggregatorAnalyzer:
    def analyze_tile_batch(batch: List[Dict]) -> List[Dict]:
        results = []

        analyzers = {
            'texture', TextureAnalyzer(),
            'wavelet', WaveletAnalyzer(),
            'spatial', SpatialAnalyzer(),
        }

        for tile_data in batch:
            try:
                tile_img = np.array(tile_data['tile'])
                tile_metrics = {}

                for analyzer in analyzers.values():
                    tile_metrics.update(analyzer.compute_metrics(tile_img))
                    
                # Add tile position
                tile_metrics['position'] = tile_data['position']
                results.append(tile_metrics)

            except Exception as e:
                logger.debug(f"Error processing tile: {str(e)}")
                results.append({})

        return results