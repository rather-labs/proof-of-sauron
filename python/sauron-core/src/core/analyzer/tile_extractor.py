from PIL import Image
import math

class TileExtractor:
    def __init__(self, tile_size=64):
        self.tile_size = tile_size
