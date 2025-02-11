from PIL import Image
from pathlib import Path

def main():

    try:
        current_path = Path(__file__).parent
        image_path = current_path.parent / "assets" / "real.jpeg"

        if not image_path.exists():
            raise FileNotFoundError(f"File not found: {image_path}")

        # Open an image file
        img = Image.open(image_path)
        print(f"Successfully opened image: {img}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()