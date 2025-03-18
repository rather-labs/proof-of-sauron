import pytest
import numpy as np
from PIL import Image
from core.analyzer.tile_extractor import TileExtractor

@pytest.fixture
def extractor():
    return TileExtractor(tile_size=64)

@pytest.fixture
def square_image():
    return Image.new('RGB', (256, 256))    

def test_initialization(extractor):
    """Test that the TileExtractor initializes with correct parameters"""
    
    assert extractor.tile_size == 64

def test_compute_tile_dimensions(extractor):
    """Test that the tile dimensions are calculated correctly"""
    
    n_cols, n_rows, tile_width, tile_height = extractor.compute_tile_dimensions(256, 256)

    assert n_cols == 4
    assert n_rows == 4
    assert tile_width == 64
    assert tile_height == 64
    

def test_extract_tile(square_image):
    """Test that a single tile is extracted correctly"""
    
    img_array = np.array(square_image)
    extractor = TileExtractor(tile_size=64)
    tile = extractor.extract_tile(img_array, 0, 0, 64, 64)
    assert tile['row'] == 0
    assert tile['col'] == 0
    assert tile['position'] == (0, 0, 64, 64)