import pytest
import numpy as np
from core.features.texture import TextureAnalyzer

@pytest.fixture
def analyzer():
    return TextureAnalyzer()

def test_compute_texture_divergence(analyzer, uniform_image):
    assert analyzer is None

def test_compute_histogram(analyzer):
    """Test histogram computation"""
    
    arr = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    hist = analyzer.compute_histogram(arr)

    assert isinstance(hist, np.ndarray)
    assert np.isclose(np.sum(hist), 1.0)  # Checks normalization
    assert not np.any(np.isnan(hist))  # Checks for NaN values

def test_texture_features_computation(analyzer, uniform_image):
    """Test texture features computation"""

    metrics = analyzer.compute_texture_features(uniform_image)

    arr = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    features = analyzer.compute_texture_features(arr)

def test_preprocess_image(texture_analyzer):
    """Test image preprocessing"""
    # Test with different input types
    # RGB image
    rgb_image = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
    processed_rgb = texture_analyzer._preprocess_image(rgb_image)
    assert processed_rgb.shape == (64, 64)
    assert processed_rgb.dtype == np.float32
    assert np.all((processed_rgb >= 0) & (processed_rgb <= 1))

    # Grayscale image
    gray_image = np.random.randint(0, 255, (64, 64), dtype=np.uint8)
    processed_gray = texture_analyzer._preprocess_image(gray_image)
    assert processed_gray.shape == (64, 64)
    assert np.all((processed_gray >= 0) & (processed_gray <= 1))

    # Invalid input
    assert texture_analyzer._preprocess_image(None) is None
    assert texture_analyzer._preprocess_image([]) is None
