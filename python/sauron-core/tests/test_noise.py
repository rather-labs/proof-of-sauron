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

def test_normalization(analyzer):
    """Test _normalize function"""
    assert analyzer._normalize(0, 1) == 0.5
    assert analyzer._normalize(1000, 1) > 0.99
    assert analyzer._normalize(-1000, 1) < 0.01




