# temporary this will be replaced by the fixture helper
import pytest
import numpy as np
from core.features.wavelets import WaveletAnalyzer


@pytest.fixture(params=("l", 3))
def wavelet_analyzer(l=3):
    return WaveletAnalyzer(wavelet='db1', level=l)

#testing fixture, to be removed later
@pytest.fixture
def sample_tile():
    """Create a simple test image for wavelet analysis."""
    # Simple 64x64 grayscale image with a gradient
    tile = np.zeros((64, 64), dtype=np.float32)

    # Add a simple gradient from top to bottom
    for i in range(64):
        tile[i, :] = i / 64.0

    return tile

# the end game of fixture parameterization to test the wavelet metrics against different well known patterns
@pytest.fixture(params=[
    ('horizontal', 64, 0.9),  # Expected high horizontal energy
    ('vertical', 64, 0.9),    # Expected high vertical energy
    ('diagonal', 64, 0.8),    # Expected high diagonal energy
    ('smooth', 64, 0.1),      # Low frequency content
    ('checker', 16, 0.95),    # High frequency pattern
    ('random', 64, 0.5),      # Random noise
])
def synthetic_image(request):
    pattern, size, _ = request.param
    if pattern == 'horizontal':
        img = np.zeros((size, size))
        img[:, size//2:] = 1
    elif pattern == 'vertical':
        img = np.zeros((size, size))
        img[size//2:, :] = 1
    elif pattern == 'diagonal':
        img = np.eye(size)
    elif pattern == 'smooth':
        x = np.linspace(0, 1, size)
        img = np.outer(x, x)
    elif pattern == 'checker':
        img = np.indices((size, size)).sum(axis=0) % 2
    elif pattern == 'random':
        img = np.random.rand(size, size)
    return img, request.param[2]

def test_directional_sensitivity(wavelet_analyzer, synthetic_image):
    """Test if wavelet metrics respond appropriately to directional patterns"""

    img, expected_energy = synthetic_image
    metrics = wavelet_analyzer.compute_wavelet_metrics(img)

    if 'horizontal' in synthetic_image[0]:
        # Should show higher energy in horizontal coefficients
        assert metrics['wavelet_l1'] > metrics['wavelet_l2']
        assert metrics['wavelet_total'] > expected_energy
    elif 'vertical' in synthetic_image[0]:
        # Should show higher energy in vertical coefficients
        assert metrics['wavelet_l1'] > metrics['wavelet_l3']
    elif 'diagonal' in synthetic_image[0]:
        # Should show higher energy in diagonal coefficients
        assert metrics['wavelet_l1'] > 0.7

@pytest.mark.parametrize("requested_level", [5, 10]) # Levels higher than possible for 8x8
def test_multilevel_decomposition(sample_tile, requested_level):
    """
    Test that WaveletAnalyzer correctly handles levels exceeding the image maximum.
    It should compute metrics only up to the maximum possible level.
    """
    wavelet = 'db1' # Use a specific wavelet for consistency
    analyzer = WaveletAnalyzer(wavelet=wavelet, level=requested_level)

    expected_levels = min(requested_level, analyzer._get_max_possible_level(sample_tile.shape))

    # Compute metrics using the analyzer
    metrics = analyzer.compute_wavelet_metrics(sample_tile)

    # Verify the number of computed level-specific metrics
    level_metric_keys = [keys for keys in metrics if keys.startswith('wavelet_l')]

    assert len(level_metric_keys) == expected_levels
    assert f'wavelet_l{expected_levels}' in metrics
    assert f'wavelet_l{expected_levels + 1}' not in metrics
    assert 'wavelet_total' in metrics