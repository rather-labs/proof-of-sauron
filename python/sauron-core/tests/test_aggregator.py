import pytest
from core.analysis.aggregator import AggregatorAnalyzer

@pytest.fixture
def analyzer():
    return AggregatorAnalyzer()

def test_analyze_tile_batch(analyzer):
    assert analyzer is not None