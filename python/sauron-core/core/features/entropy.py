import numpy as np
from PIL import Image
from typing import Dict
from scipy.stats import entropy


class EntropyAnalyzer:
    def normalized_sigmoid(self, x , center=0.5, steepness=10):
        """
        Normalize values to [0, 1] using a sigmoid function
        center represent the middle point of the sigmoid function
        steepness represent how sharply the function transition between 0 and 1
        """
        return 1 / (1 + np.exp(-steepness * (x - center)))
    
    