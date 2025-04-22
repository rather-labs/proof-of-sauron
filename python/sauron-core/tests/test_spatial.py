from core.features.spatial import SpatialAnalyzer
from tests.fixtures import *

@pytest.fixture
def analyzer():
    return SpatialAnalyzer()

def test_spatial_metrics_keys(analyzer, square_tile):
    """Test that all expected metric keys are present."""
    metrics = analyzer.compute_spatial_metrics(square_tile)
    keys = {
        'texture_uniformity_h',
        'texture_uniformity_v',
        'correlation_h',
        'correlation_v',
        'contrast_variance',
    }
    
    assert metrics is not None
    assert isinstance(metrics, dict)
    assert set(metrics.keys()) == keys

def test_spatial_metrics_computation(analyzer, square_tile):
    """Test spatial metrics computation"""

    metrics = analyzer.compute_spatial_metrics(square_tile)

    assert metrics['texture_uniformity_h'] != 0.0
    assert metrics['texture_uniformity_v'] != 0.0
    assert metrics['correlation_h'] == 0.0
    assert metrics['correlation_v'] == 0.0
    assert metrics['contrast_variance'] == 0.0

def test_spatial_metrics_gradient(analyzer, gradient_image):
    """Test metrics on a gradient image."""
    metrics = analyzer.compute_spatial_metrics(gradient_image)
    
    # Horizontal gradient should have zero vertical texture uniformity
    # But non-zero horizontal uniformity
    assert metrics['texture_uniformity_h'] > 0.5
    # The gradient is constant, so histogram should have just one value
    assert metrics['texture_uniformity_v'] > 0.1
    
    # Horizontal gradient has perfect correlation horizontally
    # (each row has same gradient pattern)
    assert abs(metrics['correlation_h']) > 0.0
    
    # There should be some contrast variation in a gradient
    assert metrics['contrast_variance'] == 0.0