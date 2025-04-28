import pytest
import numpy as np
from core.features.texture import TextureAnalyzer, compute_histogram
from tests.fixtures import square_image

@pytest.fixture
def analyzer():
    return TextureAnalyzer()

def test_compute_texture_divergence(analyzer, square_image):
     # Create a list of tiles for testing
    tiles = [square_image, square_image.copy()]  # Two identical images
    metrics = analyzer.compute_texture_divergence(tiles)
    
    # Assert that it returns a dictionary (basic test)
    assert isinstance(metrics, dict)

def test_compute_histogram(analyzer):
    """Test histogram computation"""
    
    arr = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    hist = compute_histogram(arr)

    assert isinstance(hist, np.ndarray)
    assert np.isclose(np.sum(hist), 1.0)  # Checks normalization
    assert not np.any(np.isnan(hist))  # Checks for NaN values

def test_texture_features_computation(analyzer, square_image):
    """Test texture features computation"""

    metrics = analyzer.compute_texture_features(square_image)
    
    assert isinstance(metrics, dict)
        
    # Uniform image should have low entropy
    assert metrics['global_entropy'] < 0.3
    
    # Should have low variation between regions
    assert metrics['region_entropy_var'] < 0.01
    assert metrics['region_divergence_mean'] < 0.01

def test_preprocess_image(analyzer):
    """Test image preprocessing"""

    # Test with different input types
    rgb_image = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
    processed_rgb = analyzer._preprocess_image(rgb_image)
    assert processed_rgb.shape == (64, 64)
    assert processed_rgb.dtype == np.float32
    assert np.all((processed_rgb >= 0) & (processed_rgb <= 1))

    # Grayscale image
    gray_image = np.random.randint(0, 255, (64, 64), dtype=np.uint8)
    processed_gray = analyzer._preprocess_image(gray_image)
    assert processed_gray.shape == (64, 64)
    assert np.all((processed_gray >= 0) & (processed_gray <= 1))

    # Invalid input
    assert analyzer._preprocess_image(None) is None
    assert analyzer._preprocess_image([]) is None
