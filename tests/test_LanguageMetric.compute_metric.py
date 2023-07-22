import os
import sys
import math

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import unittest
import math

from pyannote.core import Annotation, Segment
from language_metric import LanguageMetric


class TestLanguageMetric(unittest.TestCase):
    def setUp(self):
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
        Test the compute_metric method of the LanguageMetric class.
        """
        test = LanguageMetric(uri=self.URI)
        result = test.compute_metric(self.components)
        for k, v in result.items():
            self.assertTrue(
                math.isclose(result[k], self.answer[k], rel_tol=1e-9),
                f"FAIL: {k} not equal",
            )


if __name__ == "__main__":
    unittest.main()
