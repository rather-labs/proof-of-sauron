import numpy as np

def safe_sigmoid(x, multiplier=5, midpoint=0.5):
    """
    Compute sigmoid function safely to avoid overflow warnings.
    This function scales the input to avoid overflow and underflow issues.
    """
    z = multiplier * (x - midpoint)
    # For large negative values, return 0
    if z < -100:
        return 0.0
    # For large positive values, return 1
    if z > 100:
        return 1.0
    # Otherwise use the standard formula
    return float(1.0 / (1.0 + np.exp(-z)))