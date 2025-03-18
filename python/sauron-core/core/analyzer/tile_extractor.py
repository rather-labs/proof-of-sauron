from PIL import Image
import numpy as np
import math

class TileExtractor:
    def __init__(self, tile_size=64):
        self.tile_size = tile_size

    def compute_tile_dimensions(self, img):
        """Calculate tile grid dimensions based on image size"""
        
        img_width, img_height = img.size

        n_cols = max(1, img_width // self.tile_size)
        n_rows = max(1, img_height // self.tile_size)
        
        tile_width = img_width // n_cols
        tile_height = img_height // n_rows
        
        return n_cols, n_rows, tile_width, tile_height

    def extract_tile(self, img_array, row, col, tile_width, tile_height):
        """Extract a single tile from the image array"""
        
        left = col * tile_width
        top = row * tile_height
        right = left + tile_width
        bottom = top + tile_height
        
        tile = img_array[top:bottom, left:right]
        
        return {
            'row': row,
            'col': col,
            'position': (left, top, right, bottom),
        }
    