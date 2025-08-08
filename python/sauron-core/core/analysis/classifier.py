import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from typing import Dict

class AIImageClassifier:
    """Classifier for detecting AI-generated images using SVM"""

    def __init__(self):
        self.classifier = SVC(probability=True)
        self.scaler = StandardScaler()
        self.feature_columns = [
            'entropy', 'correlation_h', 'correlation_v',
            'noise', 'wavelet_total', 'contrast'
        ]

    def prepare_features(self, metrics: Dict[str, float]) -> np.ndarray:
        """Convert metrics dictionary to feature vector"""
        features = [metrics[col] for col in self.feature_columns]
        return np.array(features).reshape(1, -1)

    def predict_probability(self, metrics: Dict[str, float]) -> float:
        """Predict probability of AI-generated image"""
        features = self.prepare_features(metrics)
        scaled_features = self.scaler.transform(features)
        return self.classifier.predict_proba(scaled_features)[0][1]