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

@pytest.fixture
def rectangle_image():
    return Image.new('RGB', (256, 512))

@pytest.fixture
def tile_array(request, rectangle_image):
    return np.array(rectangle_image)

def test_initialization(extractor):
    """Test that the TileExtractor initializes with correct parameters"""
    
    assert extractor.tile_size == 64

def test_compute_tile_dimensions(extractor, square_image):
    """Test that the tile dimensions are calculated correctly"""

    n_cols, n_rows, tile_width, tile_height = extractor.compute_tile_dimensions(square_image)
    

    assert (n_cols, n_rows) == (4,4)
    assert tile_width, tile_height == (64, 64)
    
@pytest.mark.parametrize("row,col,expected_position", [
    (0, 0, (0, 0, 64, 64)),         # top-left
    (4, 2, (128, 256, 192, 320)),   # middle
    (7, 3, (192, 448, 256, 512))    # bottom-right
])
def test_rectangle_tile_positions(extractor, rectangle_image, row, col, expected_position, tile_array):
    """Test extraction of top-left tile"""

    n_cols, n_rows, tile_width, tile_height = extractor.compute_tile_dimensions(rectangle_image)
    
    tile = extractor.extract_tile(tile_array, row, col, tile_width, tile_height)
    assert tile['position'] == expected_position

def test_extract_tile_rectangle(extractor, rectangle_image):
    """Test that a single tile is extracted correctly from a rectangle image"""
    
    img_array = np.array(rectangle_image)
    n_cols, n_rows, tile_width, tile_height = extractor.compute_tile_dimensions(rectangle_image)
        
    # Verify dimensions
    assert n_cols == 4  # 256/64 = 4
    assert n_rows == 8  # 512/64 = 8
    assert tile_width == 64  # 256/4
    assert tile_height == 64  # 512/8