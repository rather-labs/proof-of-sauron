
from core.features.texture import TextureAnalyzer
from core.features.wavelets import WaveletAnalyzer
from core.features.spatial import SpatialAnalyzer
from typing import List, Dict
import logging
import numpy as np
from PIL import Image

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
    
    @Cache()
    def analyze_image(image_path: str, max_tiles: int = 32, batch_size: int = 2) -> Dict:
        """Analyze an image with parallel processing and caching"""
        try:
            start.time = time.time()
            logger.info(f"Analyzing image: {image_path}...")

            # Load image
            img = _load_image(image_path)
             # Check for early noise detection
            early_result = _check_early_noise_detection(img)

            if early_result:
                early_result['processing_time'] = time.time() - start_time
                return early_result

        except Exception as e:
            logger.error(f"Critical error in image analysis: {str(e)}")
            return {'ai_score': 0.5, 'error': str(e)}

    def _load_image(image_path: str) -> Image:
        """Load and validate an image from the given path."""
        try:
            img = Image.open(image_path)
            logger.info(f"Successfully loaded image: size={img.size}, mode={img.mode}")
            return img
        except Exception as e:
            logger.error(f"Failed to load image {image_path}: {str(e)}")
            raise

    def _check_early_noise_detection(img) -> Optional[Dict]:
        return None