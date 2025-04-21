import pytest
import numpy as np
from PIL import Image
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / "data"

@pytest.fixture
def uniform_image():
    """Create uniform test image"""
    return np.full((64, 64), 128, dtype=np.uint8)

@pytest.fixture
def square_image():
    return Image.new('RGB', (256, 256))

@pytest.fixture
def rectangle_image():
    return Image.new('RGB', (256, 512))

@pytest.fixture
def tile_array(request, rectangle_image):
    return np.array(rectangle_image)

@pytest.fixture
def random_image():
    """Create random noise image"""
    np.random.seed(42)
    return np.random.randint(0, 256, (64, 64), dtype=np.uint8)

@pytest.fixture
def gradient_image():
    """Create gradient image"""
    x = np.linspace(0, 255, 64, dtype=np.uint8)
    return np.tile(x, (64, 1))

@pytest.fixture
def real_image():

    image_path = TEST_DATA_DIR / "real.jpeg"
    if not image_path.exists():
        raise FileNotFoundError(f"File not found: {image_path}")
    return Image.open(image_path)

@pytest.fixture
def fake_image():

    image_path = TEST_DATA_DIR / "fake.jpeg"
    if not image_path.exists():
        raise FileNotFoundError(f"File not found: {image_path}")
    return Image.open(image_path)
