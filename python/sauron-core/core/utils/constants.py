import math

# Angles in radians
ANGLE_0_DEG = 0.0
ANGLE_45_DEG = math.pi / 4
ANGLE_90_DEG = math.pi / 2
ANGLE_135_DEG = 3 * math.pi / 4

# Common orientation lists
ORIENTATIONS_DEFAULT = [ANGLE_0_DEG, ANGLE_45_DEG, ANGLE_90_DEG, ANGLE_135_DEG]
ORIENTATIONS_FINE = [i * math.pi / 8 for i in range(8)]  # 8 orientations (0°, 22.5°, 45°, ... 157.5°)

# Default parameters
DEFAULT_HISTOGRAM_BINS = 50
DEFAULT_WINDOW_SIZE = 9
DEFAULT_TILE_SIZE = 128
DEFAULT_EPSILON = 1e-10

# FFT parameters
FFT_HF_THRESHOLD = 0.25  # High-frequency threshold (fraction of image size)

# Sensitivity multipliers for different metrics
SENSITIVITY = {
    'texture_kl': 1.25,
    'texture_js': 1.35,
    'texture_wasserstein': 1.4,
}