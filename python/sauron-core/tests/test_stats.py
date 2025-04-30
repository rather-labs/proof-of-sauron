import pytest
import numpy as np
import pandas as pd
from core.analysis.stats import StatisticalAnalyzer

def test_stats_analyzer_initialization():
    """Test statistical analyzer initialization"""
    analyzer = StatisticalAnalyzer()
    assert analyzer.scaler is not None

def test_compute_aggregate_metrics():
    """Test aggregate metrics computation"""
    analyzer = StatisticalAnalyzer()

    # Test with valid metrics
    tile_metrics = [
        {
            'texture_kl_relative_var': 0.3,
            'texture_js_relative_var': 0.2,
            'texture_wasserstein_relative_var': 0.1,
            'region_entropy_var': 0.4,
            'region_mean_var': 0.3,
            'region_std_var': 0.2,
            'gradient_entropy_var': 0.5,
            'gradient_mean_var': 0.4
        }
    ]

    metrics = analyzer.compute_aggregate_metrics(tile_metrics)
    assert isinstance(metrics, dict)
    assert 'ai_score' in metrics
    assert 0 <= metrics['ai_score'] <= 1

def test_analyze_region_patterns():
    """Test region pattern analysis"""
    analyzer = StatisticalAnalyzer()

    # Create test data
    df = pd.DataFrame({
        'region_entropy_var': [0.3, 0.4, 0.5],
        'region_mean_var': [0.2, 0.3, 0.4],
        'region_std_var': [0.1, 0.2, 0.3]
    })

    metrics = analyzer._analyze_region_patterns(df)
    assert isinstance(metrics, dict)
    assert len(metrics) > 0

    # Check value ranges
    for value in metrics.values():
        assert isinstance(value, float)
        assert not np.isnan(value)

def test_error_handling():
    """Test error handling in statistical analysis"""
    analyzer = StatisticalAnalyzer()

    # Test with empty input
    metrics = analyzer.compute_aggregate_metrics([])
    assert metrics['ai_score'] == 0.5  # Should return neutral score

    # Test with invalid metrics
    invalid_metrics = [
        {'invalid_key': np.nan},
        {'another_invalid': np.inf}
    ]
    result = analyzer.compute_aggregate_metrics(invalid_metrics)
    assert 0 <= result['ai_score'] <= 1  # Should handle invalid input gracefully

def test_gradual_metric_changes():
    """Test how metrics change with gradual input changes"""
    analyzer = StatisticalAnalyzer()

    # Create series of increasingly AI-like metrics
    base_metrics = {
        'texture_kl_relative_var': 0.1,
        'texture_js_relative_var': 0.1,
        'texture_wasserstein_relative_var': 0.1,
        'region_entropy_var': 0.1,
        'region_mean_var': 0.1,
        'region_std_var': 0.1,
        'gradient_entropy_var': 0.1,
        'gradient_mean_var': 0.1
    }

    scores = []
    for i in range(10):
        factor = i / 10
        metrics = {k: v + factor for k, v in base_metrics.items()}
        result = analyzer.compute_aggregate_metrics([metrics])
        scores.append(result['ai_score'])

    # Scores should increase monotonically
    assert all(scores[i] <= scores[i+1] for i in range(len(scores)-1))

def test_metric_influence():
    """Test the influence of different metrics on the final score"""
    analyzer = StatisticalAnalyzer()

    base_metrics = {
        'texture_kl_relative_var': 0.5,
        'texture_js_relative_var': 0.5,
        'texture_wasserstein_relative_var': 0.5,
        'region_entropy_var': 0.5,
        'region_mean_var': 0.5,
        'region_std_var': 0.5,
        'gradient_entropy_var': 0.5,
        'gradient_mean_var': 0.5
    }

    base_score = analyzer.compute_aggregate_metrics([base_metrics])['ai_score']

    # Test each metric's influence
    metric_influences = {}
    for key in base_metrics:
        high_metrics = base_metrics.copy()
        high_metrics[key] = 0.9
        high_score = analyzer.compute_aggregate_metrics([high_metrics])['ai_score']

        metric_influences[key] = high_score - base_score

    # Ensure texture metrics have significant influence
    assert metric_influences['texture_kl_relative_var'] > 0
    assert metric_influences['texture_js_relative_var'] > 0

def test_extreme_values():
    """Test handling of extreme metric values"""
    analyzer = StatisticalAnalyzer()

    extreme_metrics = [
        {
            'texture_kl_relative_var': 1000.0,
            'texture_js_relative_var': -1000.0,
            'texture_wasserstein_relative_var': np.inf,
            'region_entropy_var': -np.inf,
            'region_mean_var': 1e6,
            'region_std_var': -1e6,
            'gradient_entropy_var': 1e9,
            'gradient_mean_var': -1e9
        }
    ]

    result = analyzer.compute_aggregate_metrics(extreme_metrics)
    assert 0 <= result['ai_score'] <= 1  # Should still give valid probability

def test_sparse_metrics():
    """Test handling of sparse or partially missing metrics"""
    analyzer = StatisticalAnalyzer()

    sparse_metrics = [
        {
            'texture_kl_relative_var': 0.5,
            'region_entropy_var': 0.5
        },
        {
            'texture_js_relative_var': 0.5,
            'gradient_entropy_var': 0.5
        }
    ]

    result = analyzer.compute_aggregate_metrics(sparse_metrics)
    assert 0 <= result['ai_score'] <= 1  # Should handle partial metrics