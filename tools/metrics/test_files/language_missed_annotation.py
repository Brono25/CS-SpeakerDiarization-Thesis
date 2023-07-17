import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import matplotlib.pyplot as plt
import test_files.utils as u

from pyannote.core import Annotation, Segment
from language_metrics import EnglishSpanishErrorRate


URI = "test bench"


#######################################
#  met.language_missed_annotation
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
test = EnglishSpanishErrorRate(
    uri=URI, reference=ref, hypothesis=hyp, language_map=language_annotation
)
result = test.language_missed_annotation()

answer = Annotation(uri=URI)
answer[Segment(2, 3)] = "ENG"
answer[Segment(3, 5)] = "SPA"
answer[Segment(6, 7)] = "SPA"
answer[Segment(7, 8)] = "ENG"
answer[Segment(12, 15)] = "ENG"

if isinstance(result, Annotation) and result == answer and result.uri == ref.uri:
    print("PASS: language_missed_annotation")
    sys.exit(0)
else:
    print("FAIL: language_missed_annotation")
    sys.exit(1)
