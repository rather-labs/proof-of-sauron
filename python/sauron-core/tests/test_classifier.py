import pytest
import numpy as np
from core.analysis.classifier import AIImageClassifier

def test_classifier_initialization():
    """Test classifier initialization"""
    classifier = AIImageClassifier()
    assert classifier.classifier is not None
    assert classifier.scaler is not None
    assert len(classifier.feature_columns) > 0

def test_prepare_features():
    """Test feature preparation"""
    classifier = AIImageClassifier()

    # Test with valid metrics
    metrics = {
        'entropy': 0.5,
        'correlation_h': 0.3,
        'correlation_v': 0.4,
        'noise': 0.2,
        'wavelet_total': 0.6,
        'contrast': 0.7
    }

    features = classifier.prepare_features(metrics)
    assert isinstance(features, np.ndarray)
    assert features.shape == (1, len(classifier.feature_columns))

    # Test missing features handling
    incomplete_metrics = {'entropy': 0.5}
    with pytest.raises(KeyError):
        classifier.prepare_features(incomplete_metrics)

    # Test with invalid values
    invalid_metrics = {
        'entropy': np.nan,
        'correlation_h': np.inf,
        'correlation_v': -np.inf,
        'noise': 'invalid',
        'wavelet_total': None,
        'contrast': []
    }
    with pytest.raises(ValueError):
        classifier.prepare_features(invalid_metrics)

def test_predict_probability():
    """Test probability prediction"""
    classifier = AIImageClassifier()
    np.random.seed(42)  # For reproducibility

    # Create synthetic training data
    X_train = np.random.rand(100, len(classifier.feature_columns))
    y_train = np.random.randint(0, 2, 100)

    # Fit the classifier and scaler
    classifier.scaler.fit(X_train)
    classifier.classifier.fit(classifier.scaler.transform(X_train), y_train)

    # Test with various input ranges
    test_cases = [
        # Clear natural image case
        {
            'entropy': 0.1,
            'correlation_h': 0.1,
            'correlation_v': 0.1,
            'noise': 0.1,
            'wavelet_total': 0.1,
            'contrast': 0.1
        },
        # Clear AI-generated case
        {
            'entropy': 0.9,
            'correlation_h': 0.9,
            'correlation_v': 0.9,
            'noise': 0.9,
            'wavelet_total': 0.9,
            'contrast': 0.9
        },
        # Borderline case
        {
            'entropy': 0.5,
            'correlation_h': 0.5,
            'correlation_v': 0.5,
            'noise': 0.5,
            'wavelet_total': 0.5,
            'contrast': 0.5
        }
    ]

    for metrics in test_cases:
        prob = classifier.predict_probability(metrics)
        assert isinstance(prob, float)
        assert 0 <= prob <= 1

def test_classifier_with_extreme_values():
    """Test classifier with extreme input values"""
    classifier = AIImageClassifier()

    # Train with extreme values
    np.random.seed(42)
    X_train = np.random.rand(100, len(classifier.feature_columns)) * 2 - 1  # Range [-1, 1]
    y_train = np.random.randint(0, 2, 100)

    classifier.scaler.fit(X_train)
    classifier.classifier.fit(classifier.scaler.transform(X_train), y_train)

    # Test with extreme values
    extreme_metrics = {
        'entropy': 100.0,
        'correlation_h': -100.0,
        'correlation_v': 1000.0,
        'noise': -1000.0,
        'wavelet_total': 10000.0,
        'contrast': -10000.0
    }

    prob = classifier.predict_probability(extreme_metrics)
    assert isinstance(prob, float)
    assert 0 <= prob <= 1  # Should still give valid probability

def test_classifier_feature_importance():
    """Test relative importance of features"""
    classifier = AIImageClassifier()

    # Train with controlled data
    np.random.seed(42)
    X_train = np.random.rand(1000, len(classifier.feature_columns))
    # Create synthetic labels where entropy is the most important feature
    y_train = (X_train[:, 0] > 0.5).astype(int)

    classifier.scaler.fit(X_train)
    classifier.classifier.fit(classifier.scaler.transform(X_train), y_train)

    # Test with high entropy vs low entropy
    high_entropy = {
        'entropy': 0.9,
        'correlation_h': 0.1,
        'correlation_v': 0.1,
        'noise': 0.1,
        'wavelet_total': 0.1,
        'contrast': 0.1
    }

    low_entropy = {
        'entropy': 0.1,
        'correlation_h': 0.9,
        'correlation_v': 0.9,
        'noise': 0.9,
        'wavelet_total': 0.9,
        'contrast': 0.9
    }

    # High entropy should give higher probability
    prob_high = classifier.predict_probability(high_entropy)
    prob_low = classifier.predict_probability(low_entropy)
    assert prob_high > prob_low