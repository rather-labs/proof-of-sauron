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