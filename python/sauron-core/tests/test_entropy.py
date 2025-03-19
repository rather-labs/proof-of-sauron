import pytest
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
from core.features.entropy import EntropyAnalyzer

TEST_DATA_DIR = Path(__file__).parent / "data"

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

@pytest.fixture
def uniform_image():
    return Image.new('RGB', (64, 64), (255, 255, 255))

@pytest.fixture
def analizer():
    return EntropyAnalyzer()

def _compute_image_entropy(image, analyzer):
    image = image.convert('L')
    image_array = np.array(image)
    return analyzer.compute_entropy(image_array)

@pytest.mark.parametrize("x, center, steepness, expected", [
    (0, 0.5, 10, 1 / (1 + np.exp(5))),
    (0.5, 0.5, 10, 0.5),
    (1, 0.5, 10, 1 / (1 + np.exp(-5)))
])
def test_normalized_sigmoid(x, center, steepness, expected, analizer):
    assert np.isclose(analizer.normalized_sigmoid(x, center, steepness), expected, atol=1e-5)


def test_compute__entropy_uniform_image(analizer, uniform_image):
    """ Test that the entropy is computed correctly in a uniform image"""
    entropy = _compute_image_entropy(uniform_image, analizer)
    assert entropy == 0


def test_compute_entropy_real_image(analizer, real_image):
    """ Test that the entropy is computed correctly in a real image"""
    entropy = _compute_image_entropy(real_image, analizer)
    assert 0.5 <= entropy <= 1

def test_compute_entropy_fake_image(analizer, fake_image):
    """ Test that the entropy is computed correctly in a real image"""
    entropy = _compute_image_entropy(fake_image, analizer)
    assert 0.5 <= entropy <= 1