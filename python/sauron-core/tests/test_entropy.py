from core.features.entropy import EntropyAnalyzer
from tests.fixtures import *

@pytest.fixture
def uniform_image():
    return Image.new('RGB', (64, 64), (255, 255, 255))

@pytest.fixture
def analyzer():
    return EntropyAnalyzer()

def _compute_image_entropy(image, analyzer):
    image = image.convert('L')
    image_array = np.array(image)
    return analyzer.compute_entropy(image_array)

@pytest.mark.parametrize("x, center, steepness, expected", [
    (0, 0.5, 10, 1 / (1 + np.exp(5))),
    (0.5, 0.5, 10, 0.5),
    (1, 0.5, 10, 1 / (1 + np.exp(-5)))
])
def test_normalized_sigmoid(x, center, steepness, expected, analyzer):
    assert np.isclose(analyzer.normalized_sigmoid(x, center, steepness), expected, atol=1e-5)

def test_compute__entropy_uniform_image(analyzer, uniform_image):
    """ Test that the entropy is computed correctly in a uniform image"""
    entropy = _compute_image_entropy(uniform_image, analyzer)
    assert entropy == 0

def test_compute_entropy_real_image(analyzer, real_image):
    """ Test that the entropy is computed correctly in a real image"""
    entropy = _compute_image_entropy(real_image, analyzer)
    assert 0.5 <= entropy <= 1

def test_compute_local_entropy_uniform(analyzer, uniform_image):
    """Test local entropy on a uniform image (should be 0)"""

    window_size = 5

    mean_local_entropy = analyzer.compute_local_entropy(uniform_image, window_size=window_size)
    # For a uniform image, the entropy of every window should be 0
    assert np.isclose(mean_local_entropy, 0.0)
