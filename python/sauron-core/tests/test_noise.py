import pytest
import numpy as np
from PIL import Image
from core.features.noise import NoiseAnalyzer

@pytest.fixture
def analyzer():
    return NoiseAnalyzer()


@pytest.fixture
def uniform_image():
    """Create uniform test image"""
    return np.full((64, 64), 128, dtype=np.uint8)

@pytest.fixture
def random_image():
    """Create random noise image"""
    np.random.seed(42)
    return np.random.randint(0, 256, (64, 64), dtype=np.uint8)

def test_normalize(analyzer):
    """Test _normalize function"""
    assert analyzer._normalize(0, 1) == 0.5
    assert analyzer._normalize(1000, 1) > 0.99
    assert analyzer._normalize(-1000, 1) < 0.01

def test_create_hf_mask(analyzer):
    """Test high frecuency mask creation"""
    height, width = 64, 64
    mask = analyzer._create_hf_mask(height, width)

    #Check mask shape and type
    assert mask.shape == (height, width)
    assert mask.dtype == bool

    #Check mask structure
    center_x, center_y = width // 2, height // 2
    assert not mask[center_y, center_x] #Center should be False
    assert mask[0, 0] #Top-left should be True

@pytest.mark.parametrize("image_fixture, expected_noise", [
    ("uniform_image", {"hf_energy": (0.0, 0.1), "noise_variance": (0.0, 0.5)}),
    ("random_image", {"hf_energy": (0.4, 0.5), "noise_variance": (0.4, 1.0)}),
    ("gradient_image", {"hf_energy": (0.1, 0.5), "noise_variance": (0.1, 0.5)})
])
def test_compute_noise_metrics(analyzer, request, image_fixture, expected_noise):
    """Test noise metrics computation"""
   
    image = 
    metrics = analyzer.compute_noise_metrics(image)
