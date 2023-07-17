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
#  met.language_confusion_annotation
######################################

ref = Annotation(uri=URI)
ref[Segment(0, 10)] = "A"
ref[Segment(9, 11)] = "B"
hyp = Annotation(uri=URI)
hyp[Segment(0, 4)] = "A"
hyp[Segment(3, 8)] = "B"
hyp[Segment(8, 11)] = "A"
language_annotation = Annotation(uri=URI)
language_annotation[Segment(0, 4)] = "ENG"
language_annotation[Segment(4, 7.5)] = "SPA"
language_annotation[Segment(7.5, 11)] = "ENG"
test = EnglishSpanishErrorRate(
    uri=URI, reference=ref, hypothesis=hyp, language_map=language_annotation
)
result = test.language_confusion_annotation()

answer = Annotation(uri=URI)
answer[Segment(4, 7.5)] = "SPA"
answer[Segment(7.5, 8)] = "ENG"
answer[Segment(10, 11)] = "ENG"


if isinstance(result, Annotation) and result == answer and result.uri == ref.uri:
    print("PASS: language_confusion_annotation")
    sys.exit(0)
else:
    print("FAIL: language_confusion_annotation")
    sys.exit(1)
