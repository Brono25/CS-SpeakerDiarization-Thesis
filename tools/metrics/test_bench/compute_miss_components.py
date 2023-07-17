import sys
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import utils as u
import matplotlib.pyplot as plt
import test_bench.utils as u
from pyannote.core import Annotation, Segment, Timeline
from metrics import EnglishSpanishErrorRate


URI = "test bench"

#######################################
#       met.compute_miss_components
######################################
ref = Annotation(uri=URI)
ref[Segment(0, 10)] = "A"
ref[Segment(5, 6)] = "B"
ref[Segment(9, 20)] = "B"
hyp = Annotation(uri=URI)
hyp[Segment(0, 2)] = "A"
hyp[Segment(8, 12)] = "A"
hyp[Segment(15, 20)] = "B"
language_annotation = Annotation(uri=URI)
language_annotation[Segment(0, 3)] = "ENG"
language_annotation[Segment(3, 7)] = "SPA"
language_annotation[Segment(5, 5.5)] = "SPA"
language_annotation[Segment(5.5, 6)] = "ENG"
language_annotation[Segment(7, 10)] = "ENG"
language_annotation[Segment(9, 11)] = "SPA"
language_annotation[Segment(11, 16)] = "ENG"
language_annotation[Segment(16, 20)] = "SPA"

answer = {
    "english_miss_error": 5,
    "english_total": 10,
    "spanish_miss_error": 3,
    "spanish_total": 8,
}
test = EnglishSpanishErrorRate(
    uri=URI, reference=ref, hypothesis=hyp, language_map=language_annotation
)
result = test.compute_miss_components()

for k in result.keys():
    if result[k] != answer[k]:
        print("FAIL: compute_miss_components")
        break
else:
    print("PASS: compute_miss_components")
