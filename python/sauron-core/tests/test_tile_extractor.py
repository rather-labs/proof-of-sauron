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

def test_initialization(extractor):
    """Test that the TileExtractor initializes with correct parameters"""
    
    assert extractor.tile_size == 64

def test_compute_tile_dimensions(extractor, square_image):
    """Test that the tile dimensions are calculated correctly"""

    n_cols, n_rows, tile_width, tile_height = extractor.compute_tile_dimensions(square_image)

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

def test_extract_tile_rectangle(extractor, rectangle_image):
    """Test that a single tile is extracted correctly from a rectangle image"""
    
    img_array = np.array(rectangle_image)
    n_cols, n_rows, tile_width, tile_height = extractor.compute_tile_dimensions(rectangle_image)
        
    # Verify dimensions
    assert n_cols == 4  # 256/64 = 4
    assert n_rows == 8  # 512/64 = 8
    assert tile_width == 64  # 256/4
    assert tile_height == 64  # 512/8

def test_rectangle_top_letf_tile(extractor, rectangle_image):
    """Test extraction of top-left tile"""

    img_array = np.array(rectangle_image)
    n_cols, n_rows, tile_width, tile_height = extractor.compute_tile_dimensions(rectangle_image)
    
    top_left = extractor.extract_tile(img_array, 0, 0, tile_width, tile_height)
    assert top_left['position'] == (0, 0, 64, 64)

def test_rectangle_middle_tile(extractor, rectangle_image):
    """Test extraction of middle tile"""
    img_array = np.array(rectangle_image)
    n_cols, n_rows, tile_width, tile_height = extractor.compute_tile_dimensions(rectangle_image)
    
    middle = extractor.extract_tile(img_array, 4, 2, tile_width, tile_height)
    assert middle['position'] == (128, 256, 192, 320)

def test_rectangle_bottom_right_tile(extractor, rectangle_image):
    """Test extraction of bottom-right tile"""
    img_array = np.array(rectangle_image)
    n_cols, n_rows, tile_width, tile_height = extractor.compute_tile_dimensions(rectangle_image)
    
    bottom_right = extractor.extract_tile(img_array, 7, 3, tile_width, tile_height)
    assert bottom_right['position'] == (192, 448, 256, 512)