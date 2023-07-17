import sys
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import utils as u
import matplotlib.pyplot as plt
import test_bench.utils as u
from pyannote.core import Annotation, Segment, Timeline
from metrics import EnglishSpanishErrorRate
import math

URI = "test bench"
#######################################
#       met.compute_metric
######################################
components = {
    "english_conf_error": 10,
    "english_total": 100,
    "spanish_conf_error": 7,
    "spanish_total": 50,
    "english_miss_error": 7,
    "spanish_miss_error": 1,
}
test = EnglishSpanishErrorRate(uri=URI)
result = test.compute_metric(components)
answer = {
    "english_conf_error_rate":  0.1,
    "spanish_conf_error_rate":   0.14,
    "english_miss_error_rate":   0.07,
    "spanish_miss_error_rate":  0.02,
    "english_error_rate": 0.17,
    "spanish_error_rate": 0.16
}
for k, v in result.items():

    if not math.isclose(result[k], answer[k], rel_tol=1e-9):
        print("FAIL: compute_metric")
        sys.exit(1)
else:
    print("PASS: compute_metric")
    sys.exit(0)
