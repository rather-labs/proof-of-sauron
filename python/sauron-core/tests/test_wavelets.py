# temporary this will be replaced by the fixture helper
import pytest
import numpy as np
from core.features.wavelets import WaveletAnalyzer


@pytest.fixture
def wavelet_analyzer():
    return WaveletAnalyzer(wavelet='db1', level=3)

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

def test_wavelet_metrics_computation(wavelet_analyzer: WaveletAnalyzer, sample_tile: np.ndarray):
    """Test wavelet metrics computation"""
    metrics = wavelet_analyzer.compute_wavelet_metrics(sample_tile)

    # Check basic structure
    assert isinstance(metrics, dict)
    assert len(metrics) == 0
    

def test_wavelet_metrics_values(wavelet_analyzer: WaveletAnalyzer, sample_tile: np.ndarray):
    """Test wavelet metrics values"""
    pass


