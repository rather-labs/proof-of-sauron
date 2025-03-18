from PIL import Image
import numpy as np
import math

class TileExtractor:
    def __init__(self, tile_size=64):
        
        self.tile_size = tile_size

    def compute_tiles(self, img, constant=1.0):
        width, height = img.size 
        min_dim = min(height, width)
        # log_dim = np._to_num(math.log(min_dim))
    
        # Efficient tile size
        
        
        # Compute the number of cols and rows
        n_cols = max(1, width // self.tile_size)
        n_rows = max(1, height // self.tile_size)
        
        # Compute tile ratios
        tile_width = width // n_cols
        tile_height = height // n_rows
        
#how to test this functions ?