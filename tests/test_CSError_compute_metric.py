import pytest
import math

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.cs_error import CSError  # noqa: E402

URI = "test bench"


class TestLanguageMetric:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        """
        Set up anything that needs to be run before each test here.
        """
        self.URI = "test bench"
        self.components = {
            "english_conf_error": 10,
            "english_total": 100,
            "spanish_conf_error": 7,
            "spanish_total": 50,
            "english_miss_error": 7,
            "spanish_miss_error": 1,
        }
        self.answer = {
            "english_conf_error_rate": 0.1,
            "spanish_conf_error_rate": 0.14,
            "english_miss_error_rate": 0.07,
            "spanish_miss_error_rate": 0.02,
            "english_error_rate": 0.17,
            "spanish_error_rate": 0.16,
        }

    def test_compute_metric(self):
        """
        Test the compute_metric method of the CSError class.
        """
        test = CSError(uri=self.URI)
        result = test.compute_metric(self.components)
        for k, v in result.items():
            assert math.isclose(result[k], self.answer[k], rel_tol=1e-9), f"FAIL: {k} not equal"
