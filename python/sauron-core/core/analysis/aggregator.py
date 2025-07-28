import logging
import numpy as np
from PIL import Image
from time import time
from core.utils.cache import Cache
from typing import List, Dict, Optional, Tuple
from core.features.texture import TextureAnalyzer
from core.features.wavelets import WaveletAnalyzer
from core.features.spatial import SpatialAnalyzer
from core.features.noise import NoiseAnalyzer

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
    def analyze_image(self, image_path: str, max_tiles: int = 32, batch_size: int = 2) -> Dict:
        """Analyze an image with parallel processing and caching"""
        try:
            start_time = time.time()
            logger.info(f"Analyzing image: {image_path}...")

            # Load image
            img = self._load_image(image_path)
             # Check for early noise detection
            early_result = self._check_early_noise_detection(img)

            if early_result:
                early_result['processing_time'] = time.time() - start_time
                return early_result

            tile_size = self._calculate_adaptive_tile_size(img.size)
            tiles = self._extract_and_limit_tiles(img, tile_size, max_tiles)
            tile_metrics, tile_arrays = self._process_tile_batches(tiles, batch_size)

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
        noise_detector = NoiseAnalyzer()
        noise_result = noise_detector.predict(img)
        noise_prob = float(noise_result.get('noise_probability', 0))
    
        if noise_prob > 0.7:
            logger.info(
                f"Early detection: Synthetic noise pattern detected "
                f"(probability: {noise_result['noise_probability']:.1%})"
            )
            return {
                'ai_score': 0.95,
                'classification': 'Synthetic Noise / Texture',
                'noise_detection': noise_result,
                'early_exit': True
            }
        return None

    # TBD
    def _calculate_adaptive_tile_size(img_size: Tuple[int, int], base_tile_size: int = 128) -> int:
        return 0
    
    def _extract_and_limit_tiles(img: Image, tile_size: int, max_tiles: int) -> List[Dict]:
        return []
    
    def _process_tile_batches(tiles: List[Dict], batch_size: int) -> Tuple[List[Dict], List[np.ndarray]]:
        return ()