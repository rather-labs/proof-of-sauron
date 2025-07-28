import numpy as np
import pandas as pd
from typing import Dict, List
from sklearn.preprocessing import StandardScaler
import logging

from core.utils.math import safe_sigmoid
logger = logging.getLogger(__name__)

class StatisticalAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()

    def compute_aggregate_metrics(self, tile_metrics: List[Dict]) -> Dict[str, float]:
        """Analyze statistical patterns focusing on natural vs AI characteristics"""
        if not tile_metrics:
            print("No valid metrics to analyze")
            return {'ai_score': 0.5}  # Neutral score when no data

        try:
            # Convert to dataframe and handle missing values
            df = pd.DataFrame(tile_metrics)
            df = df.fillna(0)  # Replace NaN with 0

            # Basic input validation
            if df.empty or len(df.columns) < 2:
                print("Insufficient data for analysis")
                return {'ai_score': 0.5}

            # Replace infinite values with large finite numbers
            df = df.replace([np.inf, -np.inf], [1e10, -1e10])

            # Core analysis components
            region_metrics = self._analyze_region_patterns(df)
            texture_metrics = self._analyze_texture_patterns(df)
            gradient_metrics = self._analyze_gradient_patterns(df)

            # Combine all metrics
            metrics = {
                **region_metrics,
                **texture_metrics,
                **gradient_metrics
            }

            # Handle extreme values in metrics
            for key in metrics:
                if np.isnan(metrics[key]) or np.isinf(metrics[key]):
                    metrics[key] = 0.0
                else:
                    # Clip extreme values to reasonable range
                    metrics[key] = float(np.clip(metrics[key], -1e10, 1e10))

            # Compute final score
            metrics['ai_score'] = self._compute_ai_probability(metrics)

            return metrics

        except Exception as e:
            print(f"Error in aggregate metrics computation: {str(e)}")
            return {'ai_score': 0.5}

    def _analyze_region_patterns(self, df: pd.DataFrame) -> Dict[str, float]:
        """Analyze regional patterns"""
        metrics = {}
        try:
            region_features = [
                'region_entropy_var',
                'region_mean_var',
                'region_std_var',
                'region_divergence_mean',
                'region_divergence_var'
            ]

            for feature in region_features:
                if feature in df.columns:
                    values = df[feature].values
                    if len(values) > 0:
                        # Handle extreme values
                        finite_values = values[np.isfinite(values)]
                        if len(finite_values) > 0:
                            metrics[f'{feature}_mean'] = float(np.mean(finite_values))
                            metrics[f'{feature}_std'] = float(np.std(finite_values))
                        else:
                            metrics[f'{feature}_mean'] = 0.0
                            metrics[f'{feature}_std'] = 0.0

        except Exception as e:
            print(f"Error in region pattern analysis: {str(e)}")

        return metrics

    def _analyze_texture_patterns(self, df: pd.DataFrame) -> Dict[str, float]:
        """Analyze texture patterns"""
        metrics = {}
        try:
            texture_features = [
                'texture_kl_relative_var',
                'texture_js_relative_var',
                'texture_wasserstein_relative_var'
            ]

            for feature in texture_features:
                if feature in df.columns:
                    values = df[feature].values
                    if len(values) > 0:
                        # Handle extreme values
                        finite_values = values[np.isfinite(values)]
                        if len(finite_values) > 0:
                            metrics[f'{feature}_mean'] = float(np.mean(finite_values))
                            # Higher values indicate AI generation
                            metrics[f'{feature}_ai_score'] = safe_sigmoid(np.mean(finite_values), 5, 0.5)
                        else:
                            metrics[f'{feature}_mean'] = 0.0
                            metrics[f'{feature}_ai_score'] = 0.5

        except Exception as e:
            logger.error(f"Error in texture pattern analysis: {str(e)}")

        return metrics

    def _analyze_gradient_patterns(self, df: pd.DataFrame) -> Dict[str, float]:
        """Analyze gradient patterns"""
        metrics = {}
        try:
            gradient_features = [
                'gradient_entropy_var',
                'gradient_mean_var',
                'gradient_var_mean'
            ]

            for feature in gradient_features:
                if feature in df.columns:
                    values = df[feature].values
                    if len(values) > 0:
                        # Handle extreme values
                        finite_values = values[np.isfinite(values)]
                        if len(finite_values) > 0:
                            metrics[f'{feature}_mean'] = float(np.mean(finite_values))
                            # More gradient variation indicates AI
                            metrics[f'{feature}_ai_score'] = safe_sigmoid(np.mean(finite_values), 5, 0.3)
                        else:
                            metrics[f'{feature}_mean'] = 0.0
                            metrics[f'{feature}_ai_score'] = 0.5

        except Exception as e:
            logger.error(f"Error in gradient pattern analysis: {str(e)}")

        return metrics

    def _compute_ai_probability(self, metrics: Dict[str, float]) -> float:
        """Compute AI probability with corrected interpretation"""
        try:
            weights = {
                # Region variation (higher in AI images)
                'region_entropy_var_mean': 0.45,      # Higher variance suggests AI
                'region_mean_var_mean': 0.35,         # Higher variance suggests AI
                'region_std_var_mean': 0.3,           # Higher variance suggests AI

                # Texture patterns (relative variance higher in AI)
                'texture_kl_relative_var_mean': 0.5,     # Key discriminator
                'texture_js_relative_var_mean': 0.45,    # Key discriminator
                'texture_wasserstein_relative_var_mean': 0.4,  # Secondary feature

                # Direct AI scores from pattern analysis
                'texture_kl_relative_var_ai_score': 0.5,
                'texture_js_relative_var_ai_score': 0.45,
                
                #'gradient_entropy_var_ai_score': 0.4,
                #'gradient_mean_var_ai_score': 0.35

                # Gradient patterns (higher in AI images) 
                'gradient_entropy_var_mean': 0.20,     # Higher entropy suggests AI
                'gradient_mean_var_mean': 0.15,        # Higher mean suggests AI
                'gradient_var_mean_mean': 0.12         # Higher variance suggests AI                
            }

            # Compute weighted score
            score = 0.0
            weight_sum = 0.0

            for metric, weight in weights.items():
                if metric in metrics:
                    value = metrics[metric]
                    if not np.isnan(value) and not np.isinf(value):
                        # Clip extreme values
                        value = np.clip(value, -1e10, 1e10)
                        # All weights are positive now - higher values indicate AI
                        score += value * weight
                        weight_sum += weight

            # Normalize score
            if weight_sum > 0:
                score = score / weight_sum

            # Convert to probability with increased sensitivity (steeper sigmoid)
            # Increased from 12 to 15 for steeper curve
            return float(np.clip(safe_sigmoid(score, 15, 0.45), 0, 1))

        except Exception as e:
            logger.error(f"Error computing AI probability: {str(e)}")
            return 0.5