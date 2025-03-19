import pytest
import numpy as np
import pandas as pd
from PIL import Image
from core.features.entropy import EntropyAnalyzer

def _load_test_image(image_path):
    return Image.open(image_path)

@pytest.fixture
def test_image():
    return _load_test_image("real.jpeg")

@pytest.fixture
def analizer():
    return EntropyAnalyzer()

@pytest.mark.parametrize("x, center, steepness, expected", [
    (0, 0.5, 10, 1 / (1 + np.exp(5))),
    (0.5, 0.5, 10, 0.5),
    (1, 0.5, 10, 1 / (1 + np.exp(-5)))
])
def test_normalized_sigmoid(x, center, steepness, expected, analizer):
    assert np.isclose(analizer.normalized_sigmoid(x, center, steepness), expected, atol=1e-5)