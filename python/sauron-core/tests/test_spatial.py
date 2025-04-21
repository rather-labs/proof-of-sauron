from core.features.spatial import SpatialAnalyzer
from tests.fixtures import *

@pytest.fixture
def analyzer():
    return SpatialAnalyzer()

def test_spatial_metrics_computation(analyzer):
    """Test spatial metrics computation"""