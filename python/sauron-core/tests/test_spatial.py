import pytest
import numpy as np
from core.features.spatial import SpatialAnalyzer

@pytest.fixture
def analyzer():
    return SpatialAnalyzer()

def test_spatial_metrics_computation(analyzer):
    """Test spatial metrics computation"""
    # Create a SpatialAnalyzer instance
    