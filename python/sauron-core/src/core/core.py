from PIL import Image
from pathlib import Path
from analyzer.tile_extractor import TileExtractor
from email.mime import image


class SauronCore:
    
    def __init__(self, tile_size=64):
        self.tile_size = TileExtractor(tile_size)
    
    def process_image(self):
        try:
            current_path = Path(__file__).parent.parent
            image_path = current_path.parent.parent / "assets" / "real.jpeg"

            if not image_path.exists():
                raise FileNotFoundError(f"File not found: {image_path}")

            # Open an image file
            img = Image.open(image_path)
            print(f"Successfully opened image: {img}")
        
        except Exception as e:
            print(f"Error: {e}")

def main():
    core = SauronCore(tile_size=128)
    core.process_image()

if __name__ == "__main__":
    main()