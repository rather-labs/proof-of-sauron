import pytest
import numpy as np
import pandas as pd
from PIL import Image

from core.tiler import TileExtractor
from tests.fixtures import square_image, rectangle_image, tile_array

@pytest.fixture
def extractor():
    return TileExtractor(tile_size=64)

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

@pytest.mark.parametrize("image,expected_tiles", [
    ('square_image', 16),    # 4x4 grid = 16 tiles
    ('rectangle_image', 32)  # 4x8 grid = 32 tiles
])
def test_compute_tiles(extractor, request, image, expected_tiles):
    """Test compute_tiles functionality"""
    # Get image fixture
    test_image = request.getfixturevalue(image)
    
    # Get tiles
    tiles = extractor.compute_tiles(test_image)
    
    # Test number of tiles
    assert len(tiles) == expected_tiles
    
    # Test tile structure
    first_tile = tiles[0]
    assert 'row' in first_tile
    assert 'col' in first_tile
    assert 'position' in first_tile

def test_compute_tiles_dataframe(extractor, square_image):
    """Test compute_tiles DataFrame output"""
    df = extractor.compute_tiles(square_image, dataFrame=True)
    
    # Verify DataFrame structure
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == {'row', 'col', 'position'}
    assert len(df) == 16  # 4x4 grid