from core.features.spatial import SpatialAnalyzer
from tests.fixtures import *

@pytest.fixture
def analyzer():
    return SpatialAnalyzer()

def test_spatial_metrics_computation(analyzer, square_tile):
    """Test spatial metrics computation"""

    metrics = analyzer.compute_spatial_metrics(square_tile)
    assert set(metrics.keys()) == {
        'texture_uniformity_h',
        'texture_uniformity_v',
        'correlation_h',
        'correlation_v'
    }
    
    assert metrics['texture_uniformity_h'] != 0.0
    assert metrics['texture_uniformity_v'] != 0.0
