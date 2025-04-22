import pytest
import numpy as np
from core.features.texture import TextureAnalyzer

@pytest.fixture
def analyzer():
    return TextureAnalyzer()

def test_compute_texture_divergence(analyzer):
    assert analyzer is None



